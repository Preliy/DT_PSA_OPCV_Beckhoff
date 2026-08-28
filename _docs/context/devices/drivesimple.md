<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# DriveSimple in TwinCAT

**4 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`DriveSimple`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/drivesimple.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_AbstractBinaryDrive` | 4 |

### `FB_AbstractBinaryDrive`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `_Forward` | OUT | `BOOL` | 1 |
| `_Backward` | OUT | `BOOL` | 1 |
| `_DriveActive` | IN | `BOOL` | 1 |

Published to the HMI: `HMI : ST_AbstractBinaryDrive_HMI`

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `M_Conveyor` | FG_Transport | `MAIN.Machine.FG_Transport.Lift01.M_Conveyor` | `FB_AbstractBinaryDrive` |
| `M_Conveyor` | FG_Transport | `MAIN.Machine.FG_Transport.Lift02.M_Conveyor` | `FB_AbstractBinaryDrive` |
| `M_Conveyor` | FG_Transport | `MAIN.Machine.FG_Transport.Transport01` ¹ | `FB_AbstractBinaryDrive` |
| `M_Conveyor` | FG_Transport | `MAIN.Machine.FG_Transport.Transport02` ¹ | `FB_AbstractBinaryDrive` |

¹ folded — the PLC has no member of its own; the unit named *is* the device and owns the process image.
