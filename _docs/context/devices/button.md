<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# Button in TwinCAT

**2 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`Button`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/button.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_IlluminatedButton` | 2 |

### `FB_IlluminatedButton`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `HardwareInput` | IN | `BOOL` | 1 |
| `LampOutput` | OUT | `BOOL` | 1 |

Published to the HMI: `HMI : ST_IlluminatedButton_HMI`

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `SS_EStop1` | FG_System | `MAIN.Machine.FG_System.SS_EStop1` | `FB_IlluminatedButton` |
| `SS_EStop2` | FG_System | `MAIN.Machine.FG_System.SS_EStop2` | `FB_IlluminatedButton` |
