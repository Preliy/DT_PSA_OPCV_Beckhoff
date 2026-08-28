<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# LinkByte in TwinCAT

**1 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`LinkByte`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/linkbyte.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_AbstractLightSource` | 1 |

### `FB_AbstractLightSource`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `InputData` | IN | `BYTE` | 8 |
| `OutputData` | OUT | `BYTE` | 8 |

Published to the HMI: `HMI : ST_AbstractLightSource_HMI`

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `Y_LaserMark` | FG_01 | `MAIN.Machine.FG_01.Y_LaserMark` | `FB_AbstractLightSource` |
