# The Beckhoff workflow

The TwinCAT half of the loop: what the four vendor skills leave behind, and where each refuses.

The whole loop — the twin, the export, the behaviour contracts — is in the main repo's
`_workflow/README.md` in the main repo's own private half. This page covers only what is TwinCAT's.

## Where this module plugs in

```
  main repo: _docs/context/.machine.json      written there, schema-versioned
                │  sync_machine.py, run in the main repo
                ▼
  _workflow/config/handoff/.machine.json          COMMITTED HERE, byte-identical
                │  + .handoff.json, which records where it came from
                │  the ONLY thing this module takes from the main repo
                ▼
  build_plc_knowledge.py  +  tc_model.py  ──>  Beckhoff/_docs/context/
                                                PROVENANCE · machine · fg-*.md
                                                devices/ · plc-io.md · .plc-image.json
                │
    ┌───────────┼───────────────────────────┐
    ▼           ▼                           ▼
  generating-   mapping-plc-io          building-hmi-elements
  plc-code      channels ⇄ EtherCAT     pages against the module's
  PLC_1 module  ⇄ SIM_1 Mapping         published HMI structs
```

Nothing here imports the root generator, and nothing here re-parses the Unity export. If a structural
fact is missing from `.machine.json`, the fix is to add it there — in the main repo — not to open
a `<Scene>_Context.json` from this side.

## The sections a vendor group page carries

The main repo's `CONTEXT-SPEC.md` defines the root sections. These are this module's, and they are
fixed in the same way: **a section is always present**, and empty renders as `_None._` rather than
being omitted, so a reader can tell "this group has no module yet" from "the generator did not get
that far".

| # | Section | Source | States |
|---|---|---|---|
| 1 | Header | `.machine.json` + the type model | Twin path, control path, module, served-by, behaviour link |
| 2 | `## Components` | the type model | Every twin device with its **verified** control PLC path, its process-image size and how much is linked |
| 3 | `## SIM_1` | `SIM_1/*.plcproj` | POU path, `.plcproj` registration, what `Mapping` targets and how many lines |
| 4 | `## PLC_1` | module `.TcPOU` | Module path, registration, PackML states implemented, fault codes, HMI struct |
| 5 | `## Mapping` | tsproj `<Mappings>` + `Mapping_PLC.xml` | Every process-image member, its terminal channel, and whether a pragma or the link file made it |

**Degradation, not refusal.** `PLC_1.tmc` is git-ignored and a checkout may have no build at all, so
every page renders from the committed `.plc-image.json` and banners itself when that snapshot is not
the live truth. A page must never look complete while its sections are silently blank.

**Fault codes are read, never invented.** They come from `_FaultCode :=` in the ST. What each one
*means* is behaviour, and lives in the main repo's `reference/` page for that group.

## The gates

**Don't link a signal that isn't in the process image, and don't trust a pragma.**
`plc_io.py reconcile` counts links from the tsproj `<Mappings>`, never from source text — a
member-path `TcLinkTo` on a function block instance compiles, reports nothing and links nothing.
A group whose page shows an empty **PLC_1** section has nothing to link yet.

**Don't reach for the `.tmc`.** Every tool reads the committed `.plc-image.json` snapshot instead —
it needs no TwinCAT and its validity is checked by a comment-stripped code digest rather than by a
timestamp. Only `plc_io.py build` reads the `.tmc`, to refresh that snapshot after an XAE build, and
it keeps the strict freshness gate because that is the one place a stale read gets committed.

**Don't build HMI for a module that doesn't exist.** Components publish their HMI structs only once
the module is generated. `binding.symbolError` is `"Ignore"` in this project, so a binding to a
missing symbol renders a blank control and reports nothing. `hmi_check.py` asserts every binding
against the type model — run it, do not eyeball the page.

**Don't hand-edit `_docs/context/`.** `build_plc_knowledge.py` sweeps the directory and deletes
any `.md` it did not write. `plc-io.md` survives only because it is named in that sweep's keep list;
a new generated page needs the same treatment or it vanishes on the next refresh.

**Don't write a machine-level fact here.** Sequences, interlocks, the reset model and the station
handshake are contracts a Siemens PLC has to honour too. They belong in the main repo's
`_docs/reference/`, and a second copy here is a second source of truth.

## The handoff

`_workflow/config/handoff/.machine.json` is this module's **committed copy** of the machine's structure. It
is a byte-identical copy of the main repo's `_docs/context/.machine.json` — no injected keys, no
reformatting — so a schema check needs no special case and staleness is a plain sha256 compare.

It is a copy rather than a reference because this module has to build from a **standalone clone**:
TwinCAT work needs no Unity, and the main repository is often simply not there. Reading across `../`
would make the module inert in exactly the case it is most used in.

Only the main repo can refresh it, and only you can commit it:

```bash
# in a checkout of the main repo with this module cloned into it
python _private/tools/build_knowledge.py
python _private/tools/sync_machine.py
git -C Beckhoff add _workflow/config/handoff && git -C Beckhoff commit -m "chore: sync machine handoff"
```

A snapshot that is behind is reported three ways and blocks nothing: `sync_machine.py --check` exits
non-zero, the main build prints a line, and `PROVENANCE.md` here carries a banner. A **schema**
mismatch is the exception — the fields this generator reads may have moved, so it refuses.

The directory's existence is what opts this module in. A module without one is skipped by the sync.

## Commands

Written **module-relative**; prefix with `Beckhoff/` from a main repo checkout. Every tool anchors on
its own file, so both work:

```bash
python _private/tools/plc_io.py reconcile              # prove the wiring adds up
python _private/tools/plc_io.py instance --group FG_01 # the PLC Instance variable list
python _private/tools/plc_io.py terminals --free       # what channels are left
python _private/tools/plc_io.py propose --group FG_02  # allocate, then review with a human
python _private/tools/plc_io.py write-mapping --group FG_02
python _private/tools/plc_io.py build                  # snapshot + plc-io.md; needs an XAE build
python _private/tools/build_plc_knowledge.py           # the pages
python _private/tools/hmi_check.py                     # every HMI binding resolves
```

`plc_io.py build --from-snapshot` re-renders `plc-io.md` from the committed snapshot without touching
the `.tmc` — the right command when TwinCAT is closed and only the document needs rebuilding.

## Where things live

| Path | What | Edited by |
|---|---|---|
| `_workflow/skills/` | The four TwinCAT skills. Read by path — there is no `.claude/` — see this module's `CLAUDE.md` for the index | You, deliberately |
| `_docs/context/` | The generated TwinCAT knowledge base, including `.plc-image.json` | **Nobody — it is generated** |
| `_workflow/config/handoff/` | The committed copy of the main repo's `.machine.json`, and its provenance | **Nobody — the main repo's `sync_machine.py` writes it** |
| `module.json` | This module's name, vendor, version and platform | The release bot writes `version`; the rest is yours |
| `_docs/reference/` | `spt-framework.md`, `plc-io-exceptions.md` — hand-written, TwinCAT-only | You, deliberately |
| `_private/tools/tc_model.py` | One parse of the TwinCAT solution, shared by everything below | You, when the projects move |
| `_private/tools/plc_io.py` | Links, terminals, the snapshot, `plc-io.md` | You, when the wiring model changes |
| `_private/tools/build_plc_knowledge.py` | The group and device pages | You, when the shape of the knowledge changes |
| `_private/tools/hmi_check.py` | Proves every HMI binding resolves | You, when a new binding form appears |
| `TwinCAT_1/` | The solution: `PLC_1`, `SIM_1`, `HMI` | XAE, the skills, and you |
