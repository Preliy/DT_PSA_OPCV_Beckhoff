<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# FG_System in TwinCAT

The control side only. What FG_System *is* - its scene hierarchy, its devices and everything a human authored about it - is in the main repo: [`FG_System`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/fg-system.md).

| | |
|---|---|
| Twin PLC path | `MAIN.FG_System` |
| Control PLC path | `MAIN.Machine.FG_System` |
| Module | `FG_System EXTENDS FB_PackML_BaseModule` |
| Served by | — |
| Devices | 10 |
| Behaviour | [`fg-system-safety.md`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/fg-system-safety.md) |

## Components

| Symbol | Device type | Twin FB | Control PLC path | I/O | Linked |
|---|---|---|---|---:|---:|
| `B_SafetyDoor11` | Lock | `FB_Lock` | `MAIN.Machine.FG_System.B_SafetyDoor11` | 3 | 3 |
| `B_SafetyDoor12` | Lock | `FB_Lock` | `MAIN.Machine.FG_System.B_SafetyDoor12` | 3 | 3 |
| `B_SafetyDoor13` | Lock | `FB_Lock` | `MAIN.Machine.FG_System.B_SafetyDoor13` | 3 | 3 |
| `B_SafetyDoor21` | Lock | `FB_Lock` | `MAIN.Machine.FG_System.B_SafetyDoor21` | 3 | 3 |
| `B_SafetyDoor22` | Lock | `FB_Lock` | `MAIN.Machine.FG_System.B_SafetyDoor22` | 3 | 3 |
| `B_SafetyDoor23` | Lock | `FB_Lock` | `MAIN.Machine.FG_System.B_SafetyDoor23` | 3 | 3 |
| `H_ControlPanel` | PanelSampler | `FB_Panel` | — ² | 0 | 0 |
| `H_SignalTower` | PanelSampler | `FB_Panel` | `MAIN.Machine.FG_System.H_SignalTower` | 4 | 4 |
| `SS_EStop1` | Button | `FB_Button` | `MAIN.Machine.FG_System.SS_EStop1` | 2 | 2 |
| `SS_EStop2` | Button | `FB_Button` | `MAIN.Machine.FG_System.SS_EStop2` | 2 | 2 |

² **Not addressed under this group.** Either the control PLC reaches it from another root (the operator panel is `MAIN.ControlSource_Panel`, not an `FG_System` member), or the type model this page was built from predates the device. Check the source banner above before treating it as a gap.

**The twin path is not the control path.** Only the control PLC path works in an HMI binding or a `TcLinkTo` pragma, and the twin's spelling fails silently in both.

## SIM_1

| | |
|---|---|
| POU | `TwinCAT_1/PLC/SIM_1/FG_System/FG_System.TcPOU` |
| In `.plcproj` | yes |
| `Mapping` targets | GVL_EtherCAT_1_SIM |
| `Mapping` lines | 43 |

Only the `Mapping` action is ours. The `{region generated code}` block belongs to OC Assistant and is overwritten on the next twin regeneration.

## PLC_1

| | |
|---|---|
| POU | `TwinCAT_1/PLC/PLC_1/Modules/01 FG_System/FG_System.TcPOU` |
| In `.plcproj` | yes |
| PackML states | — |
| Fault codes | — |
| HMI struct | `ST_HMI_FG_System` |

Fault codes are read from `_FaultCode :=` in the ST. What each one *means* is behaviour and lives in the reference page named in the header.

## Mapping

| Process image member | Dir | Terminal | Via |
|---|---|---|---|
| `B_SafetyDoor11.ClosedSensor` | IN | FG_System_Door_EL1809_1 channel 1 | Mapping_PLC.xml |
| `B_SafetyDoor11.LockOutput` | OUT | FG_System_Door_EL2008_1 channel 1 | Mapping_PLC.xml |
| `B_SafetyDoor11.LockedSensor` | IN | FG_System_Door_EL1809_1 channel 2 | Mapping_PLC.xml |
| `B_SafetyDoor12.ClosedSensor` | IN | FG_System_Door_EL1809_1 channel 3 | Mapping_PLC.xml |
| `B_SafetyDoor12.LockOutput` | OUT | FG_System_Door_EL2008_1 channel 2 | Mapping_PLC.xml |
| `B_SafetyDoor12.LockedSensor` | IN | FG_System_Door_EL1809_1 channel 4 | Mapping_PLC.xml |
| `B_SafetyDoor13.ClosedSensor` | IN | FG_System_Door_EL1809_1 channel 5 | Mapping_PLC.xml |
| `B_SafetyDoor13.LockOutput` | OUT | FG_System_Door_EL2008_1 channel 3 | Mapping_PLC.xml |
| `B_SafetyDoor13.LockedSensor` | IN | FG_System_Door_EL1809_1 channel 6 | Mapping_PLC.xml |
| `B_SafetyDoor21.ClosedSensor` | IN | FG_System_Door_EL1809_1 channel 7 | Mapping_PLC.xml |
| `B_SafetyDoor21.LockOutput` | OUT | FG_System_Door_EL2008_1 channel 4 | Mapping_PLC.xml |
| `B_SafetyDoor21.LockedSensor` | IN | FG_System_Door_EL1809_1 channel 8 | Mapping_PLC.xml |
| `B_SafetyDoor22.ClosedSensor` | IN | FG_System_Door_EL1809_1 channel 9 | Mapping_PLC.xml |
| `B_SafetyDoor22.LockOutput` | OUT | FG_System_Door_EL2008_1 channel 5 | Mapping_PLC.xml |
| `B_SafetyDoor22.LockedSensor` | IN | FG_System_Door_EL1809_1 channel 10 | Mapping_PLC.xml |
| `B_SafetyDoor23.ClosedSensor` | IN | FG_System_Door_EL1809_1 channel 11 | Mapping_PLC.xml |
| `B_SafetyDoor23.LockOutput` | OUT | FG_System_Door_EL2008_1 channel 6 | Mapping_PLC.xml |
| `B_SafetyDoor23.LockedSensor` | IN | FG_System_Door_EL1809_1 channel 12 | Mapping_PLC.xml |
| `H_SignalTower.Blue` | OUT | FG_System_Panel_EL2809_1 channel 11 | Mapping_PLC.xml |
| `H_SignalTower.Green` | OUT | FG_System_Panel_EL2809_1 channel 12 | Mapping_PLC.xml |
| `H_SignalTower.Red` | OUT | FG_System_Panel_EL2809_1 channel 9 | Mapping_PLC.xml |
| `H_SignalTower.Yellow` | OUT | FG_System_Panel_EL2809_1 channel 10 | Mapping_PLC.xml |
| `SS_EStop1.HardwareInput` | IN | FG_System_Panel_EL1809_1 channel 9 | Mapping_PLC.xml |
| `SS_EStop1.LampOutput` | OUT | FG_System_Panel_EL2809_1 channel 13 | Mapping_PLC.xml |
| `SS_EStop2.HardwareInput` | IN | FG_System_Panel_EL1809_1 channel 10 | Mapping_PLC.xml |
| `SS_EStop2.LampOutput` | OUT | FG_System_Panel_EL2809_1 channel 14 | Mapping_PLC.xml |

26 members, 26 linked, **0 unlinked**. A declared but unlinked signal compiles and is silently dead - see [plc-io.md](plc-io.md) for the channel map and [plc-io-exceptions.md](../reference/plc-io-exceptions.md) for the ones that are unlinked on purpose.
