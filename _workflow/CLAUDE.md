# Beckhoff — the machine in TwinCAT

The Beckhoff realisation of DT_PSA_OPCV — the Digital Twin for Laser Welding & Assembly System (PSA OPCV). **This module is its own git
repository**, cloned into the main repo's root as `Beckhoff/` and gitignored there so the two do not
collide. It owns its TwinCAT projects, its own knowledge base, its own curated reference, its own
skills, and its own committed copy of the machine handoff — so it builds from a standalone clone,
with no Unity and no main repository present. That is the normal case for TwinCAT work.

Read the main repo's [`../CLAUDE.md`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/CLAUDE.md) first — it holds the machine, the twin, and every
rule that is not TwinCAT-specific.

This vendor's Unity scene lives in the **main** repository, not here — the twin is one project and
every vendor scene instances the same prefab. It is
`Unity/Assets/Demo_1/Scenes/VC_Demo_1_Beckhoff_1.unity` there: the shared
`Machine_1` prefab plus this vendor's operator panel, `H_ControlPanel` →
`MAIN.FG_System.H_ControlPanel`, aggregating the eight PackML buttons. It is currently the
**reference scene** for the root pages, which is why Beckhoff's panel is the one they show — marked
`†` there, because it is this vendor's and not the machine's.

```
   TwinCAT_1/PLC/TwinCAT.tsproj          one solution, two PLC projects, one EtherCAT pair
     PLC_1   AmsPort 851   the control program (SPT framework), drives EtherCAT_1
     SIM_1   AmsPort 852   the twin device layer, OC Assistant's output, on EtherCAT_1_SIM
   TwinCAT_1/HMI                          TE2000, bound to PLC_1 as ADS runtime PLC1
```

| Path | What |
|---|---|
| `TwinCAT_1/PLC/PLC_1` | The control program. `Modules/NN FG_xx/` per functional group |
| `TwinCAT_1/PLC/SIM_1` | Twin devices. Unity binds these ADS symbols |
| `TwinCAT_1/PLC/Mapping_PLC.xml` | The importable link file. Its `OwnerA` is `TIPC^PLC_1^PLC_1 Instance` |
| `TwinCAT_1/HMI` | TE2000 panels, `HMI.hmiproj` |
| `_docs/` | Hand-written **user documentation for this platform** — setup, running the machine, how the PLC projects are organised. Everything TwinCAT-specific a human needs |
| `_docs/context/` | **Generated** — what TwinCAT makes of the machine |
| `_docs/reference/` | Hand-written TwinCAT knowledge |
| `_workflow/` | **Published** — how this module is worked on: `CLAUDE.md`, `README.md`, `skills/` (the four TwinCAT skills, read by path), `config/` and `tools/` |
| `_workflow/tools/` | **Published** — `build_wiki.py`, `publish_wiki.py`, `set_module_version.py`. They read only tracked files, and the two workflows in `.github/workflows/` have to run them from a checkout of this repository alone |
| `_workflow/config/handoff/` | The **committed copy** of the main repo's `.machine.json`, plus where it came from. Written by the main repo's `sync_machine.py`; never hand-edit |
| `_private/tools/` | **Gitignored, its own repository.** `tc_model.py`, `plc_io.py`, `hmi_check.py`, `build_plc_knowledge.py` — the generators that read the TwinCAT projects, and nothing else |
| `.github/workflows/wiki.yml` | Publishes this module's wiki on a release or manual dispatch; builds it as a gate on any PR touching `_docs/` |
| `.github/workflows/release.yml` | **This module's own release line.** semantic-release on `master`: previews the version on the PR, then writes `module.json` and `CHANGELOG.md`, tags, publishes, and calls `wiki.yml` |
| `.releaserc.json` | The semantic-release plugin list. **No `@semantic-release/npm`** — there is no `package.json` here, so `module.json` is the version record |
| `module.json` | This module's identity — name, vendor, version, platform. Read by the main repo's compatibility check, and by a ZIP download that has no git metadata. **`version` is written by the release**, never by hand |
| `CHANGELOG.md` | Owned by the release bot. **Never hand-edit** — the next release overwrites it |
| `LICENSE`, `THIRD-PARTY-NOTICES.md` | GPL-3.0 for this module's own work, and what it builds against. **The Beckhoff licences are the user's own** — this repository ships no Beckhoff software and no licence for any, and says so in both files and in `_docs/01-setup.md` |
| `_data/` | Third-party sources — **read only on explicit permission from the user.** Committed on purpose: this repository's `.gitignore` deliberately does not exclude it |

## Run a tool from either root

Every tool anchors on its own file, not on your working directory, so all three work the same from
inside this module or from a main repo checkout above it. The commands here are written
**module-relative**; prefix them with `Beckhoff/` when you are working from the main repo:

```bash
python _private/tools/plc_io.py reconcile
python _private/tools/build_plc_knowledge.py
python _private/tools/hmi_check.py
python _workflow/tools/build_wiki.py            # this module's wiki, into _wiki/
python _workflow/tools/publish_wiki.py          # dry run; --publish pushes it
python _workflow/tools/set_module_version.py    # print module.json's version
```

`publish_wiki.py` **refuses unless this directory is its own git checkout**. Cloned inside a main
repo checkout it usually is; if it was never cloned — if it is just a directory in the main repo's
working tree — then git here answers for the *main* repository, and publishing would push this
module's wiki over the main project's. That check is the only thing standing between the two.

In normal use nobody runs the two wiki commands by hand: `.github/workflows/wiki.yml` publishes on
a release or a manual dispatch, and gates every PR touching `_docs/` with `build_wiki.py --check`.
Nobody runs `set_module_version.py` with an argument by hand either — `.github/workflows/release.yml`
does, through `.releaserc.json`, and commits the result. Run it bare to read the version.

Two tools are the **main repo's** and must run from there: `build_knowledge.py`, which reads the
Unity export, and `sync_machine.py`, which writes this module's handoff snapshot.

Messages print paths relative to whichever checkout is in use — `Beckhoff/TwinCAT_1/…` when this
module sits inside a main repo, `TwinCAT_1/…` when it is cloned alone.

## The knowledge base

`_docs/context/` is generated by `build_plc_knowledge.py` from two inputs: **this module's own
committed copy** of the machine handoff, `_workflow/config/handoff/.machine.json`, and this module's
TwinCAT projects. **Never hand-edit it** — the builder sweeps the directory and deletes anything it
did not write.

The handoff is a byte-identical copy of the main repo's `_docs/context/.machine.json`, written
by `sync_machine.py` **in the main repo** and committed here. It is never read across `../`: the
main repository may not be present at all. See [`_workflow/config/handoff/README.md`](config/handoff/README.md).

| File | Answers |
|---|---|
| `PROVENANCE.md` | How current the type model is, and which build of the twin export it was matched against. **Read first.** |
| `machine.md` | The groups as TwinCAT sees them: module present, process image size, how much is linked |
| `fg-*.md` | Per group: verified control PLC paths, the `SIM_1` POU, the `PLC_1` module, the terminal mapping |
| `devices/*.md` | Per twin device type: which control FB it becomes, its process-image members and channel widths |
| `plc-io.md` | Which terminal channel every signal is on, what is free, and whether the link file and the project agree |
| `.plc-image.json` | The committed type-model snapshot every tool reads instead of the `.tmc` |

Each page links back to its twin-side page in the main repo. **The split is not cosmetic:** what a
group *is* has one answer for the whole machine, what it *becomes* has one answer per platform.

`_workflow/CONTEXT-SPEC.md` in the main repo is the contract for the root pages; this module's
sections are documented in [`_workflow/README.md`](README.md).

## User documentation

`_docs/` is this module's own documentation set, for a human rather than an agent:

| File | Answers |
|---|---|
| `_docs/README.md` | What is here, and what is deliberately elsewhere |
| `_docs/01-setup.md` | Installing TwinCAT, building the solution, connecting the twin |
| `_docs/02-usage.md` | Running the machine: startup order, the operator panel, the web HMI |
| `_docs/03-architecture.md` | Why `PLC_1` and `SIM_1` are separate, and where the boundary runs |

**Every TwinCAT-specific instruction belongs here, not in the main repo's `_docs/`.** The root set
covers the machine and the twin and links out to this one.

**This module publishes its own wiki**, at `DT_PSA_OPCV_Beckhoff/wiki`, built from `_docs/` by
`_workflow/tools/build_wiki.py` and pushed by `publish_wiki.py` beside it. It used to be `Beckhoff-*`
pages inside the main repo's wiki, built by the main repo's tooling — which left a self-contained
module unable to publish its own documentation, and made an optional module a hard dependency of the
main repo's publish. The page-naming rule and the cross-repo link rule are a **shared contract**,
stated in the main repo's `_workflow/WIKI-SPEC.md`; the two builders are independent, so a
divergence there is a dead wiki link that nothing catches.

## Curated reference

Hand-written, never generated, TwinCAT-specific:

| File | Answers |
|---|---|
| `_docs/reference/spt-framework.md` | How the SPT framework is meant to be used, the official build order, and which third-party claims about it are wrong |
| `_docs/reference/plc-io-exceptions.md` | Which signals are unlinked on purpose, so a real gap is not hidden by a deliberate one |

Everything in it is checked against the installed libraries. When a source disagrees with the shipped
binary, the binary wins — the published docs document **SPT V4** while this project runs **V3.9**, and
they carry a few outright typos on top of that.

**Behaviour is not here.** Sequences, interlocks, fault codes and the reset model are machine-level
contracts in [`../_docs/reference/`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md), because a
Siemens PLC has to honour the same ones. They were written from *this* module's ST, which is why the
PLC wins whenever the twin's authored prose disagrees.

## Skill routing

**Not auto-discovered — there is no `.claude/` directory. Open the file.** Each skill is ordinary
Markdown under `_workflow/skills/`. `Read` the `SKILL.md` before starting the task and follow it; a
`reference.md` beside it is the deep detail, read on demand. Paths below are module-relative; prefix
them with `Beckhoff/` when working from the main repo.

| Task | Read this file |
|---|---|
| Write or extend a `PLC_1` equipment module | `_workflow/skills/generating-plc-code/SKILL.md` (+ `reference.md`) |
| Read the PLC's own symbols, process image or free channels | `_workflow/skills/exporting-plc-symbols/SKILL.md` |
| Allocate and link PLC I/O to EtherCAT terminals | `_workflow/skills/mapping-plc-io/SKILL.md` (+ `reference.md`) |
| Build or change TE2000 HMI content | `_workflow/skills/building-hmi-elements/SKILL.md` (+ `reference.md`) |

## Hard rules

TwinCAT-specific. The vendor-neutral ones are in [`../CLAUDE.md`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/CLAUDE.md).

- **Never edit the `{region generated code}` block in a `SIM_1` POU.** OC Assistant owns it and
  overwrites it on the next twin regeneration. Only the `Mapping` action is ours.
- **A generated TwinCAT file that is not in the `.plcproj` does not exist**, and this fails silently.
  Every new `.TcPOU`/`.TcGVL`/`.TcDUT` needs a `<Compile Include>` entry, and every new folder a
  `<Folder Include>`.
- **Every POU, method, action, property, getter and setter needs a fresh GUID.** A reused `Id` breaks
  the project in ways TwinCAT reports badly.
- **Read the committed snapshot, not `PLC_1.tmc`.** `_docs/context/.plc-image.json` is the
  default source for every PLC fact: it is committed, deterministic, and needs no TwinCAT. The
  `.tmc` is a git-ignored build artifact whose timestamp is not a usable freshness signal — a
  checkout rewrites source mtimes around it, and a **comment-only edit marks it stale** for a change
  that cannot alter a single type.
- **The snapshot is checked by code digest, not by timestamp.** `tc_model.code_digest()` hashes the
  `PLC_1` sources with every comment stripped, so prose can be rewritten freely and the snapshot
  stays valid; a declaration, member, pragma or located variable changes it. `PROVENANCE.md` carries
  the verdict, and a group page banners itself only when the snapshot is genuinely **behind**.
- **`plc_io.py build` is the only thing that reads the `.tmc`**, because refreshing the snapshot is
  the one job that needs the real type model — and it keeps the strict freshness gate, since that is
  where a stale read would be baked into a committed file. Rebuild in XAE, then run it.
- **A `TcLinkTo` member path (`.Member := …`) resolves on a STRUCT, not on a FUNCTION_BLOCK
  instance.** On an FB instance the compiler accepts it, reports nothing and links nothing —
  `FG_01.TcPOU` carries ten such pragmas that have never produced a link. A single-target pragma
  resolves on any plain located `AT %I*` / `AT %Q*` scalar. A link is real when it appears in the
  tsproj `<Mappings>`; `AutoLink="true"` marks the ones a pragma made.
- **The control PLC path is `MAIN.Machine.<group>.<device>`, not the twin's `MAIN.<group>.…`.** Only
  the first works in a link or an HMI binding, and the second fails silently in both. The verified
  path for every device is in this module's group pages — never derive one by hand.
- **The HMI is bound by ADS *port*, not by project name.** `Server/ADS/ADS.Config.default.json` maps
  runtime alias `PLC1` to port 851, so page bindings read `ADS.PLC1.MAIN.…` and are unaffected by
  what the `.plcproj` is called. Do not "fix" a binding by renaming it after the PLC project.
- **`build_plc_knowledge.py` reads `vendors["Beckhoff"]`, not `groups`.** The top-level `groups` in
  `.machine.json` is the *reference* scene. It happens to be Beckhoff's today, so the two are
  identical — which is exactly why taking the wrong one would go unnoticed until the reference
  moved. Read the vendor entry.
- **Never read a path that climbs out of this repository.** `../_docs/context/.machine.json` and
  `../../../_docs/…` name a repository that is simply not there in a standalone clone — the
  normal case for TwinCAT work. Read `_workflow/config/handoff/.machine.json`, this module's own committed
  copy. Every tool anchors on `tc_model.MODULE` for real paths; `tc_model.ROOT` is for **display
  only** and equals `MODULE` when there is no main repo above.
- **Run git against `MODULE`, never `ROOT`.** This module is its own repository and `ROOT` may be a
  different repo or none. Every git call site here swallows its own failure into `"not committed"`,
  so getting this wrong does not raise — it silently stamps every page as uncommitted, forever.
- **A link into the main repository is an absolute URL.** Built by `up()` from the URL and ref
  recorded in `_workflow/config/handoff/.handoff.json`, so it is deterministic per sync rather than varying
  with whoever's checkout ran the build. This module's `build_wiki.py` maps those URLs to the **main
  repo's wiki pages**, so a reader of this wiki lands on a page rather than a raw Markdown blob. It
  verifies each one when the main repo happens to be the directory above, and emits it either way —
  refusing on an unverifiable link would make the main repo a build dependency of this module.
- **A stale handoff is a banner; a wrong schema is a refusal.** Being an export behind still
  describes a real machine, so `PROVENANCE.md` says so and the build continues. A schema mismatch
  means the fields this generator reads may have moved, and there is nothing safe to build.
- **`module.json`'s `version` is the release bot's, exactly as `CHANGELOG.md` is.** There is no
  `package.json` here, so semantic-release writes the version into `module.json` — through
  `_workflow/tools/set_module_version.py`, called from `.releaserc.json`'s exec step and committed
  by `@semantic-release/git`. Hand-editing it is overwritten by the next release, and worse, it is
  the field the main repo's `check_compatibility.py` fetches over https to decide whether this
  module still pairs with the twin. Every other member of that file is hand-maintained as before.
- **This module releases on its own version line.** Never by a shared number with the main repo:
  it records the version it verified as `tested` in its `modules.json`, and the coupling that
  actually matters is the machine handoff committed here under `_workflow/config/handoff/`. A
  release here publishes nothing there and needs no coordinated bump. **There is no version range
  in either direction** — `requiresMain` was removed from `module.json` because a range admits
  versions that do not exist yet, so it never once fired. A commit subject decides the version the
  same way it does in the main repo: `feat:` minor, `fix:`/`perf:`/`refactor:` patch, `chore:`/`ci:`
  nothing.
- **The `.tmc` files are build artifacts and are git-ignored.** `PLC_1.tmc` and `SIM_1.tmc` are the
  current ones; older `OC_PLC.tmc` / `OC_SIM.tmc` / `PLC.tmc` / `SIM.tmc` files left over from the
  project rename are untracked leftovers, not sources. Never read one.
