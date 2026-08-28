<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# Lock in TwinCAT

**6 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`Lock`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/lock.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_SafetyDoor` | 6 |

### `FB_SafetyDoor`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `ClosedSensor` | IN | `BOOL` | 1 |
| `LockedSensor` | IN | `BOOL` | 1 |
| `LockOutput` | OUT | `BOOL` | 1 |

Published to the HMI: `HMI : ST_SafetyDoor_HMI`

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `B_SafetyDoor11` | FG_System | `MAIN.Machine.FG_System.B_SafetyDoor11` | `FB_SafetyDoor` |
| `B_SafetyDoor12` | FG_System | `MAIN.Machine.FG_System.B_SafetyDoor12` | `FB_SafetyDoor` |
| `B_SafetyDoor13` | FG_System | `MAIN.Machine.FG_System.B_SafetyDoor13` | `FB_SafetyDoor` |
| `B_SafetyDoor21` | FG_System | `MAIN.Machine.FG_System.B_SafetyDoor21` | `FB_SafetyDoor` |
| `B_SafetyDoor22` | FG_System | `MAIN.Machine.FG_System.B_SafetyDoor22` | `FB_SafetyDoor` |
| `B_SafetyDoor23` | FG_System | `MAIN.Machine.FG_System.B_SafetyDoor23` | `FB_SafetyDoor` |
