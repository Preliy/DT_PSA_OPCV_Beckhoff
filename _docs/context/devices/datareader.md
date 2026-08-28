<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# DataReader in TwinCAT

**3 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`DataReader`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/datareader.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_AbstractCamera` | 3 |

### `FB_AbstractCamera`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `InputData` | IN | `BYTE` | 8 |
| `OutputData` | OUT | `BYTE` | 8 |

Published to the HMI: `HMI : ST_AbstractCamera_HMI`

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `P_Camera` | FG_01 | `MAIN.Machine.FG_01.P_Camera` | `FB_AbstractCamera` |
| `P_Camera` | FG_02 | `MAIN.Machine.FG_02.P_Camera` | `FB_AbstractCamera` |
| `P_Camera` | FG_05 | `MAIN.Machine.FG_05.P_Camera` | `FB_AbstractCamera` |
