<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# ControlBunker in TwinCAT

**1 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`ControlBunker`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/controlbunker.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_AbstractBunker` | 1 |

### `FB_AbstractBunker`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `InputData` | IN | `BYTE` | 8 |
| `OutputData` | OUT | `BYTE` | 8 |

Published to the HMI: `HMI : ST_AbstractBunker_HMI`

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `Y_CapsSource` | FG_05 | `MAIN.Machine.FG_05.Y_CapsSource` | `FB_AbstractBunker` |
