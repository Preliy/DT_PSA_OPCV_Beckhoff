#!/usr/bin/env python3
"""Render THIS module's documentation into _wiki/, ready to push to its GitHub wiki.

Reads  _docs/*.md                   hand-written setup, usage and architecture
       _docs/context/**.md          GENERATED TwinCAT realisation of the machine
       _docs/reference/*.md         hand-written platform reference
Writes _wiki/*.md, _wiki/_Sidebar.md, _wiki/_Footer.md

Run from the main repo root:  python Beckhoff/_workflow/tools/build_wiki.py [--check]
or from this module:          python _workflow/tools/build_wiki.py [--check]

WHY THIS EXISTS AT ALL. This module used to be published as `Beckhoff-*` pages inside
the main repository's wiki, by the main repository's tooling. That made a self-contained
module unable to publish its own documentation, and made an optional module a hard
dependency of the main repo's publish. A GitHub wiki IS a repository - <repo>.wiki.git -
and this module is its own repository, so it has its own wiki and builds it here.

THE CONTRACT IS SHARED, THE CODE IS NOT. Page naming and link rewriting must agree with
the main repository's builder, because a cross-repo link is computed by ONE builder
using the OTHER's rule - a divergence is a dead wiki link that nothing catches. The rule
is written down once, in the main repo's `_workflow/WIKI-SPEC.md`, and mirrored in this
module's `_workflow/CLAUDE.md`. Implement THAT, not a local habit.

IMAGES ARE NEVER COPIED. A figure link becomes a raw.githubusercontent.com URL into this
repository. The file is still resolved on disk and a missing one still stops the build.

_wiki/ IS GENERATED and swept on every run. Edit the source, never a page in _wiki/.

A LINK THAT CANNOT BE RESOLVED STOPS THE BUILD. In a flat namespace a broken link is
invisible until a reader clicks it, and there is no compiler to catch one.
"""

import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_wiki"
DOCS = ROOT / "_docs"
HANDOFF = ROOT / "_workflow/config/handoff/.handoff.json"

GENERATED_COMMENT = re.compile(r"^<!--\s*GENERATED\s+(?:by|from)\b.*?-->\s*$", re.M | re.S)
SOURCE_COMMENT = re.compile(r"^<!--\s*Sources?:.*?-->\s*$", re.M | re.S)
LINK_RE = re.compile(r"(?<!\\)\[(?P<text>[^\]]*)\]\((?P<target>[^)\s]+)(?P<title>\s+\"[^\"]*\")?\)")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
BLOB_RE = re.compile(r"^(?P<repo>https?://[^\s]+?)/(?:blob|tree)/[^/]+/(?P<path>.+)$")
GITHUB_RE = re.compile(r"^https?://(?:www\.)?github\.com/([^/]+)/([^/]+)/?$")


class WikiError(Exception):
    """Something that would publish a broken page. Stops the build."""


# ----------------------------------------------------------------- this repository


def _git(args, cwd=ROOT):
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                           text=True, timeout=15)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def _json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _normalise(url):
    url = re.sub(r"\.git$", "", (url or "").strip())
    m = re.match(r"^[\w.+-]+@([^:]+):(.+)$", url)
    return f"https://{m.group(1)}/{m.group(2)}" if m else url


MODULE = _json(ROOT / "module.json")

# DECLARED in module.json, never probed from `git remote`. A generated link must not
# name whichever machine happened to build it - and inside a main-repo checkout this
# directory is gitignored rather than a separate clone, so `git remote` here answers
# for the WRONG repository.
SRC_URL = _normalise(MODULE.get("repository"))
if not SRC_URL:
    SRC_URL = ""

# The ref a link into this repository should name: the default branch, not whichever
# feature branch happened to build the wiki.
_head = _git(["symbolic-ref", "--short", "refs/remotes/origin/HEAD"])
SRC_REF = _head[len("origin/"):] if _head.startswith("origin/") else "master"

# This module's reference pages are framework and wiring notes, not behaviour - the
# behaviour contracts are machine-level and live in the main repository. See WIKI-SPEC.
REF_PREFIX = "Reference"
REF_SECTION = "Reference"

# Home is this repository's landing page, which is its README.
OVERRIDES = {"_docs/README.md": "Home"}

ALIASES = {
    "README.md": "Home",
    "CONTRIBUTING.md": None,        # None -> link out to the repo, not into the wiki
}

SECTIONS = ["Getting started", "The machine", REF_SECTION, "Device types"]

DEVICE_DIRS = [DOCS / "context/devices"]


def raw_url(repo, ref, rel):
    """The raw-content URL for a file in a GitHub repository.

    Only github.com. A silently wrong image URL renders as a broken image and nothing
    says why, which is precisely the failure this build exists to refuse on.
    """
    m = GITHUB_RE.match((repo or "").strip())
    if not m:
        raise WikiError(
            f"cannot build a raw-content URL for '{repo}': only github.com repositories "
            f"have a raw.githubusercontent.com address this tool knows how to spell.")
    return f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/{ref}/{rel.lstrip('/')}"


# ------------------------------------------------------------------- page naming
# The contract in the main repo's _workflow/WIKI-SPEC.md. Keep this in step with it.


def _title(stem):
    """fg-01 -> FG_01, plc-io -> PLC-IO, spt-framework -> SPT-Framework."""
    special = {"fg": "FG", "plc": "PLC", "io": "IO", "spt": "SPT", "hmi": "HMI",
               "ads": "ADS", "mil": "MIL", "sil": "SIL", "ui": "UI"}
    parts = [special.get(p.lower(), p.capitalize()) for p in stem.split("-")]
    out = "-".join(parts)
    return re.sub(r"\bFG-(\d\d|System|Transport)\b", r"FG_\1", out)


def _h1_word(path):
    """The first word of a page's H1, or None."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip().split()[0]
    except (OSError, IndexError):
        pass
    return None


def _device_name(stem, device_dirs):
    """A device type's real spelling, taken from the page's own H1.

    The generator lower-cases the file name, so capitalising it gives 'Controlbunker';
    the heading carries the type as the twin spells it. More than one directory is
    consulted when naming a page in the MAIN repository, whose checkout may be absent:
    both knowledge bases derive their device pages from the same .machine.json, so this
    module's own page for the same slug answers the same question. A DISAGREEMENT means
    the two generators have drifted, and stops the build.
    """
    found = []
    for d in device_dirs:
        name = _h1_word(Path(d) / f"{stem}.md")
        if name:
            found.append((d, name))
    if len({n for _, n in found}) > 1:
        detail = "; ".join(f"{Path(d).as_posix()} says {n}" for d, n in found)
        raise WikiError(
            f"the device type '{stem}' is spelled differently in two knowledge bases: "
            f"{detail}. Both are generated from the same .machine.json, so this is "
            f"drift - a cross-repo link built from either spelling is dead in one wiki.")
    return found[0][1] if found else _title(stem)


def page_name(rel, ref_prefix=REF_PREFIX, overrides=None, device_dirs=None):
    """The flat wiki page name for a path relative to the repository that owns it."""
    overrides = OVERRIDES if overrides is None else overrides
    device_dirs = DEVICE_DIRS if device_dirs is None else device_dirs
    if rel in overrides:
        return overrides[rel]
    p = PurePosixPath(rel)
    stem = _title(re.sub(r"^\d+-", "", p.stem))
    if p.parent.name == "devices":
        return f"Device-{_device_name(p.stem, device_dirs)}"
    if p.parts[:2] == ("_docs", "reference"):
        return f"{ref_prefix}-{stem.replace('-Behaviour', '')}"
    if p.parts[:2] == ("_docs", "context"):
        if p.stem == "machine":
            return "Machine"
        if p.stem == "PROVENANCE":
            return "Machine-Provenance"
        return f"Machine-{stem}"
    return stem


def publishable(rel):
    """Does a repo-relative path get a wiki page at all, under the rule above?"""
    p = PurePosixPath(rel)
    if p.suffix != ".md" or not p.parts or p.parts[0] != "_docs":
        return False
    if len(p.parts) == 2:
        return p.stem == "README" or bool(re.match(r"^\d+-", p.stem))
    if len(p.parts) == 3 and p.parts[1] in ("context", "reference"):
        return True
    return len(p.parts) == 4 and p.parts[1:3] == ("context", "devices")


# --------------------------------------------------------------------- discovery


def discover():
    """[(repo-relative source, page name, sidebar section)], in reading order."""
    found = []
    if not (DOCS / "README.md").exists():
        raise WikiError("_docs/README.md is missing - it is this wiki's Home page and "
                        "nothing else can stand in for it.")
    found.append(("_docs/README.md", "Home", "Getting started"))
    for src in sorted(DOCS.glob("[0-9]*.md")):
        rel = f"_docs/{src.name}"
        found.append((rel, page_name(rel), "Getting started"))

    ctx = DOCS / "context"
    if ctx.is_dir():
        # The overview first, then the groups, then the supporting pages - rglob's own
        # alphabetical order puts devices/ first and reads as noise.
        for rel in ["_docs/context/machine.md"]:
            if (ROOT / rel).exists():
                found.append((rel, page_name(rel), "The machine"))
        for f in sorted(ctx.glob("fg-*.md")):
            rel = f.relative_to(ROOT).as_posix()
            found.append((rel, page_name(rel), "The machine"))
        for f in sorted(ctx.glob("*.md")):
            rel = f.relative_to(ROOT).as_posix()
            if f.stem in ("machine", "PROVENANCE") or f.stem.startswith("fg-"):
                continue
            found.append((rel, page_name(rel), "The machine"))
        if (ctx / "PROVENANCE.md").exists():
            found.append(("_docs/context/PROVENANCE.md", "Machine-Provenance",
                          "The machine"))
        for f in sorted((ctx / "devices").glob("*.md")):
            rel = f.relative_to(ROOT).as_posix()
            found.append((rel, page_name(rel), "Device types"))

    for f in sorted((DOCS / "reference").glob("*.md")) if (DOCS / "reference").is_dir() else []:
        rel = f.relative_to(ROOT).as_posix()
        found.append((rel, page_name(rel), REF_SECTION))

    seen = {}
    for rel, page, _ in found:
        if page in seen:
            raise WikiError(f"two sources want the same wiki page '{page}': "
                            f"{seen[page]} and {rel}. The namespace is flat - add an "
                            f"entry to OVERRIDES to separate them.")
        seen[page] = rel
    return found


# ------------------------------------------------------------------- the siblings


def siblings():
    """{repo URL: info} for every repository whose wiki this one may link into.

    DECLARED in the committed handoff sidecar, never probed. That file is how this
    module reaches the main repository at all - it is the one channel across the
    boundary - and it is committed precisely so a standalone clone still knows where
    upstream is.
    """
    h = _json(HANDOFF)
    url = _normalise(h.get("upstreamUrl"))
    if not url:
        return {}
    url = url.rstrip("/")
    # The main repo, if this module happens to be cloned inside a checkout of it. Used
    # ONLY to verify a link that would be emitted either way - never to decide content.
    up = ROOT.parent
    present = (up / "_workflow/config/modules.json").is_file() and (up / "_docs").is_dir()
    return {url: {
        "name": h.get("sourceRepo") or "the main repository",
        "wiki": f"{url}/wiki",
        "dir": up,
        "present": present,
        # The main repo's reference pages ARE behaviour contracts - see WIKI-SPEC.md.
        "refPrefix": "Behaviour",
        "overrides": {"_docs/README.md": "Home"},
        "deviceDirs": ([up / "_docs/context/devices"] if present else []) + DEVICE_DIRS,
    }}


def as_wiki_page(target, sibs, pages, stats):
    """An absolute GitHub URL that some wiki publishes -> the link that reaches it."""
    m = BLOB_RE.match(target)
    if not m:
        return None
    repo = m.group("repo").rstrip("/")
    path, _, anchor = unquote(m.group("path")).partition("#")
    frag = f"#{anchor}" if anchor else ""

    if SRC_URL and repo == SRC_URL.rstrip("/"):
        page = pages.get(path)
        return f"{page}{frag}" if page else None

    s = sibs.get(repo)
    if s is None or not publishable(path):
        return None

    # Verified when the other checkout is here, emitted either way. Refusing on an
    # unverifiable link would make the main repository a build dependency of this
    # module, which is the coupling the per-repository split exists to remove.
    if s["present"]:
        if not (s["dir"] / path).exists():
            raise WikiError(
                f"link into {s['name']} names {path}, which is not in the checkout at "
                f"{s['dir']}. Either the file moved and the link was not updated, or "
                f"that checkout is stale.")
        stats["verified"] += 1
    else:
        stats["unverified"].add(s["name"])

    page = page_name(path, ref_prefix=s["refPrefix"], overrides=s["overrides"],
                     device_dirs=s["deviceDirs"])
    return f"{s['wiki']}/{page}{frag}"


# ---------------------------------------------------------------- link rewriting


def rewrite(text, src_rel, pages, images_root, sibs, stats):
    """Rewrite every link for the flat namespace. Raises on a dead one."""
    src_dir = PurePosixPath(src_rel).parent

    def one(m):
        target, text_, title = m.group("target"), m.group("text"), m.group("title") or ""
        if re.match(r"^(https?:|mailto:|#)", target):
            page = as_wiki_page(target, sibs, pages, stats)
            return f"[{text_}]({page}{title})" if page else m.group(0)

        path_part, _, anchor = target.partition("#")
        if not path_part:                                  # a bare in-page anchor
            return m.group(0)

        resolved = (ROOT / src_dir / unquote(path_part)).resolve()
        try:
            rel = resolved.relative_to(ROOT).as_posix()
        except ValueError:
            raise WikiError(
                f"{src_rel}: link '{target}' points outside this module. A link that "
                f"crosses a repository boundary must be an absolute URL - '../' climbs "
                f"out of this repository and is dead in a standalone clone.")

        # An image -> the copy in THIS repository, addressed directly. Nothing is
        # copied into the wiki, but the file still has to be here: a raw URL to a file
        # that does not exist renders as a broken image and says nothing about why.
        if resolved.suffix.lower() in IMAGE_SUFFIXES:
            if not resolved.is_file() or images_root not in resolved.parents:
                raise WikiError(
                    f"{src_rel}: image '{target}' is not a file in "
                    f"{images_root.relative_to(ROOT).as_posix()}/, so the wiki cannot "
                    f"address it.")
            return f"[{text_}]({raw_url(SRC_URL, SRC_REF, quote(rel, safe='/'))}{title})"

        if rel in ALIASES:
            alias = ALIASES[rel]
            if alias is None:
                return f"[{text_}]({SRC_URL}/blob/{SRC_REF}/{rel}{title})" if SRC_URL \
                    else f"[{text_}]({rel}{title})"
            return f"[{text_}]({alias}{'#' + anchor if anchor else ''}{title})"
        if rel in pages:
            return f"[{text_}]({pages[rel]}{'#' + anchor if anchor else ''}{title})"

        if not resolved.exists():
            raise WikiError(
                f"{src_rel}: link '{target}' resolves to {rel}, which does not exist. "
                f"A dead link in a flat wiki is invisible until someone clicks it.")
        if not SRC_URL:
            raise WikiError(
                f"{src_rel}: link '{target}' points at {rel}, which is not a wiki page, "
                f"and module.json declares no 'repository' to link out to.")
        kind = "tree" if resolved.is_dir() else "blob"
        return f"[{text_}]({SRC_URL}/{kind}/{SRC_REF}/{quote(rel, safe='/')}{title})"

    return LINK_RE.sub(one, text)


# -------------------------------------------------------------------- rendering


def banner(src_rel, generated):
    what = ("This page is **generated from the machine handoff and the TwinCAT "
            "solution**. " if generated else "")
    link = f"{SRC_URL}/blob/{SRC_REF}/{src_rel}" if SRC_URL else src_rel
    return [
        f"> {what}Published from [`{src_rel}`]({link}) — **edit it there, not here.** "
        f"Changes made in the wiki are overwritten on the next sync.",
        "",
    ]


def render(src, src_rel, pages, images_root, sibs, stats):
    text = src.read_text(encoding="utf-8")
    generated = bool(GENERATED_COMMENT.search(text))
    text = GENERATED_COMMENT.sub("", text)
    text = SOURCE_COMMENT.sub("", text)
    text = rewrite(text, src_rel, pages, images_root, sibs, stats).lstrip("\n")

    head = banner(src_rel, generated)
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join([lines[0], ""] + head + lines[1:]).rstrip() + "\n"
    return "\n".join(head + lines).rstrip() + "\n"


def sidebar(found, sibs):
    name = MODULE.get("name") or ROOT.name
    out = [f"### {name}", ""]
    by_section = {}
    for _, page, section in found:
        by_section.setdefault(section, []).append(page)
    order = SECTIONS + [s for s in by_section if s not in SECTIONS]
    for section in order:
        if section not in by_section:
            continue
        out += [f"**{section}**", ""]
        out += [f"- [[{page}]]" for page in by_section[section]]
        out.append("")

    # The one place this wiki names another repository's wiki as a whole, so a reader
    # who landed on the TwinCAT realisation can reach the machine it realises.
    if sibs:
        out += ["**The machine**", ""]
        for info in sibs.values():
            out.append(f"- [What the machine is]({info['wiki']})")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def footer(n_pages):
    name = MODULE.get("name") or ROOT.name
    src = f"[{name}]({SRC_URL})" if SRC_URL else "this module"
    return (f"_Generated from {src} by `_workflow/tools/build_wiki.py` — "
            f"{n_pages} pages. Edit the source there; changes made here are "
            f"overwritten._\n")


# ------------------------------------------------------------------------- main


def build():
    found = discover()
    pages = {rel: page for rel, page, _ in found}
    sibs = siblings()
    stats = {"verified": 0, "unverified": set()}
    images_root = (DOCS / "images").resolve()

    rendered = {f"{page}.md": render(ROOT / rel, rel, pages, images_root, sibs, stats)
                for rel, page, _ in found}
    rendered["_Sidebar.md"] = sidebar(found, sibs)
    rendered["_Footer.md"] = footer(len(found))
    return found, rendered, stats, sibs


def report(found, stats, sibs):
    for section in SECTIONS:
        n = sum(1 for _, _, s in found if s == section)
        if n:
            print(f"  {section}: {n}")
    for s in sorted({s for _, _, s in found if s not in SECTIONS}):
        print(f"  {s}: {sum(1 for _, _, x in found if x == s)}")
    if not sibs:
        print("  no upstream declared in _workflow/config/handoff/.handoff.json - links "
              "into the main repository stay as blob URLs")
        return
    for info in sibs.values():
        where = (f"cross-links verified against {info['dir']}" if info["present"]
                 else "not on disk - cross-links emitted unverified")
        print(f"  upstream wiki: {info['wiki']} ({where})")
    if stats["verified"]:
        print(f"  {stats['verified']} cross-repo link(s) verified")
    if stats["unverified"]:
        print(f"  cross-repo links into {', '.join(sorted(stats['unverified']))} could "
              f"not be verified - that checkout is not here.")


def main():
    check_only = "--check" in sys.argv
    found, rendered, stats, sibs = build()

    if check_only:
        print(f"{len(found)} pages, 0 images copied, every link resolved")
        report(found, stats, sibs)
        return

    OUT.mkdir(parents=True, exist_ok=True)

    # Sweep FIRST, then write. Sweeping afterwards deletes a page this run had just
    # written whenever its name changed only in case: a case-insensitive filesystem
    # keeps the OLD spelling when an existing file is overwritten, so the sweep sees a
    # name that is not in `rendered` and removes the page it was told to publish.
    for f in sorted(OUT.rglob("*"), reverse=True):
        if f.is_file() and f.name not in rendered:
            f.unlink()
            print(f"  removed stale {f.relative_to(OUT).as_posix()}")
        elif f.is_dir() and not any(f.iterdir()):
            f.rmdir()
            print(f"  removed stale {f.relative_to(OUT).as_posix()}/")

    for name, text in rendered.items():
        (OUT / name).write_text(text, encoding="utf-8")

    print(f"wiki written to {OUT.relative_to(ROOT)}")
    print(f"  {len(found)} pages + _Sidebar + _Footer, no images copied")
    print(f"  linking out to {SRC_URL or '(module.json declares no repository)'} "
          f"at ref {SRC_REF}")
    report(found, stats, sibs)
    print("  _wiki/ is a build artifact and is gitignored - "
          "publish with _workflow/tools/publish_wiki.py")


if __name__ == "__main__":
    try:
        main()
    except WikiError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        print("Nothing was written. Fix the source page, do not work around this.",
              file=sys.stderr)
        sys.exit(1)
