#!/usr/bin/env python3
"""Publish this module's _wiki/ to ITS OWN GitHub wiki repository.

    python Beckhoff/_workflow/tools/publish_wiki.py             dry run - pushes nothing
    python Beckhoff/_workflow/tools/publish_wiki.py --publish   commits and pushes

WHY A DRY RUN BY DEFAULT. Pushing to <repo>.wiki.git publishes to the world in one step
and there is no review between here and a reader. So the default prints exactly what
would change and stops; --publish is a second, deliberate act.

WHY IT REBUILDS. _wiki/ is a gitignored build artifact, so whatever is on disk may be
absent, stale, or left over from another branch.

WHY IT REFUSES UNLESS THIS DIRECTORY IS ITS OWN CHECKOUT. This module is normally cloned
INSIDE a checkout of the main repository, where the directory is gitignored. If it was
never cloned - if it is just a directory in the main repo's working tree - then every
git command run here answers for the MAIN repository, `git remote get-url origin` returns
the main repo's remote, and this tool would happily push a module wiki over the main
project's wiki. That is a one-command, hard-to-undo mistake, so the toplevel is checked
before anything else happens.

WHY IT MIRRORS. Files the wiki has and _wiki/ does not are deleted, not left behind. A
copy that only ever adds leaves deleted pages published forever, still linked from
search results, still wrong.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_wiki as bw  # noqa: E402  - local module, same directory

ROOT = bw.ROOT
WIKI = ROOT / "_wiki"


class Fail(Exception):
    """A refusal. Nothing is pushed."""


def run(args, cwd, check=True):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=180)
    if check and r.returncode != 0:
        raise Fail(f"`{' '.join(args)}` failed:\n{(r.stderr or r.stdout).strip()}")
    return r.stdout.strip()


# ------------------------------------------------------------------------- the gates


def check_own_checkout():
    """This directory must be the root of its own git repository. See the docstring."""
    top = run(["git", "rev-parse", "--show-toplevel"], ROOT, check=False)
    if not top:
        raise Fail(f"{ROOT} is not inside a git repository at all, so there is no "
                   f"remote to publish to.")
    if Path(top).resolve() != ROOT.resolve():
        raise Fail(
            f"{ROOT.name}/ is not its own git checkout - git here answers for "
            f"{Path(top).resolve()}. This module is a SEPARATE repository; publishing "
            f"now would push this module's wiki over that repository's wiki. Clone it "
            f"properly first:\n"
            f"  git clone {bw.SRC_URL or '<the module repository>'} {ROOT.name}")


def origin_url():
    raw = run(["git", "remote", "get-url", "origin"], ROOT, check=False)
    return bw._normalise(raw)


def check_source(allow_dirty):
    """Pages say "Published from <path>" - so those paths must exist on the remote."""
    dirty = run(["git", "status", "--porcelain"], ROOT)
    if dirty and not allow_dirty:
        raise Fail(
            "the working tree has uncommitted changes. Every published page carries a "
            "'Published from ...' link to a committed path, so publishing now puts a 404 "
            "in the header of each one. Commit and push first, or pass --allow-dirty if "
            "you know the changed files are not sources.")
    ahead = run(["git", "rev-list", "--count", "@{u}..HEAD"], ROOT, check=False)
    if ahead and ahead != "0" and not allow_dirty:
        raise Fail(
            f"{ahead} commit(s) are not pushed. The wiki would link to source files that "
            f"are not on the remote yet. Push first, or pass --allow-dirty.")
    return bool(dirty)


def rebuild():
    """Build the wiki fresh, and report what it is made of."""
    found = bw.discover()
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "build_wiki.py")],
                       cwd=ROOT, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise Fail(f"the wiki build refused, so there is nothing to publish:\n"
                   f"{(r.stderr or r.stdout).strip()}")
    print(r.stdout.rstrip())
    return found


# ---------------------------------------------------------------------- the mirror


def mirror(src, dst):
    """Make dst's contents identical to src's, leaving dst/.git alone."""
    keep = {".git"}
    for item in dst.iterdir():
        if item.name in keep:
            continue
        shutil.rmtree(item) if item.is_dir() else item.unlink()
    for item in src.iterdir():
        target = dst / item.name
        shutil.copytree(item, target) if item.is_dir() else shutil.copyfile(item, target)


def main():
    publish = "--publish" in sys.argv
    allow_dirty = "--allow-dirty" in sys.argv

    check_own_checkout()

    # The ACTUAL remote, not the declared URL from module.json. This is a real push: it
    # has to go where this checkout's origin points.
    base = origin_url()
    if not base:
        raise Fail("no git remote 'origin', so there is no wiki to publish to.")
    if bw.SRC_URL and bw.SRC_URL.rstrip("/") != base.rstrip("/"):
        print(f"  note: publishing to {base}.wiki.git (this checkout's origin), while "
              f"generated links name {bw.SRC_URL} (declared in module.json). That is the "
              f"expected state while a repository rename is pending.")

    dirty = check_source(allow_dirty)
    found = rebuild()

    tmp = Path(tempfile.mkdtemp(prefix="module-wiki-"))
    clone = tmp / "wiki"
    try:
        r = subprocess.run(["git", "clone", "--quiet", f"{base}.wiki.git", str(clone)],
                           capture_output=True, text=True, timeout=180)
        if r.returncode != 0:
            raise Fail(
                f"could not clone {base}.wiki.git:\n{(r.stderr or r.stdout).strip()}\n"
                f"If this wiki has never been used, GitHub has not created the repository "
                f"yet - it cannot be initialised from the command line. Create one page in "
                f"the web UI, then re-run this.")

        branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], clone)
        mirror(WIKI, clone)
        run(["git", "add", "-A"], clone)
        stat = run(["git", "diff", "--cached", "--stat"], clone)

        if not stat:
            print("\nwiki already up to date - nothing to publish")
            return 0

        print(f"\n{'-' * 60}\nchanges against the published wiki ({branch}):\n{stat}")

        if not publish:
            print("\nDRY RUN - nothing was pushed.")
            print(f"  staged in {clone}")
            print(f"  publish with: python {Path(__file__).name} --publish")
            return 0

        sha = run(["git", "rev-parse", "--short", "HEAD"], ROOT)
        msg = [f"docs: publish from {sha} ({len(found)} pages)"]
        if dirty:
            msg += ["", "Published from a dirty working tree (--allow-dirty)."]

        run(["git", "commit", "-m", "\n".join(msg)], clone)
        run(["git", "push", "origin", branch], clone)
        print(f"\npublished to {base}/wiki")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (Fail, bw.WikiError) as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        print("Nothing was published.", file=sys.stderr)
        sys.exit(1)
