<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# Beckhoff knowledge base provenance

Read this before trusting anything else in `Beckhoff/_docs/context/`. It answers one question the twin's own provenance cannot: how current the **control** side is, and which build of the twin export it was matched against.

| | |
|---|---|
| Control platform | TwinCAT 3 · `PLC_1` AmsPort 851 · `SIM_1` AmsPort 852 |
| PLC snapshot | current, written `2026-10-14T23:06:16Z` |
| Type model | `TwinCAT_1/PLC/PLC_1/PLC_1.tmc` |
| Twin scene | `VC_Demo_1_Beckhoff_1` (reference for the root pages: `VC_Demo_1_Beckhoff_1`) |
| Twin export | `2026-10-14T20:03:08.0167801Z` (commit `4de76f0 2026-10-15`) |
| Twin handoff | `_workflow/config/handoff/.machine.json` schema 2, commit `9a64e5a 2026-10-15` |
| Twin live-verified | yes |
| Groups | 7 |
| Process-image symbols | 225 |
| Linked | 222 |

The twin half is stamped separately in [`_docs/context/PROVENANCE.md`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/PROVENANCE.md). If the two disagree about how fresh the export is, this page is the one that is behind: re-run the root build first, then this one.
