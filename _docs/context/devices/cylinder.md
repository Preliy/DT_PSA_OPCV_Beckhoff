<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# Cylinder in TwinCAT

**35 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`Cylinder`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/cylinder.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_DoubleSolenoidFeedback` | 24 |
| `FB_SingleSolenoidFeedback` | 11 |

**The twin device type does not determine the control FB.** Read the instance table below before assuming which one a given device is.

### `FB_DoubleSolenoidFeedback`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `_ExtendOutput` | OUT | `BOOL` | 1 |
| `_RetractOutput` | OUT | `BOOL` | 1 |
| `ExtendedSensor` | IN | `BOOL` | 1 |
| `RetractedSensor` | IN | `BOOL` | 1 |

### `FB_SingleSolenoidFeedback`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `_ExtendOutput` | OUT | `BOOL` | 1 |
| `ExtendedSensor` | IN | `BOOL` | 1 |
| `RetractedSensor` | IN | `BOOL` | 1 |

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `Y_Gate1` | FG_01 | `MAIN.Machine.FG_01.Y_Gate1` | `FB_SingleSolenoidFeedback` |
| `Y_Gate2` | FG_01 | `MAIN.Machine.FG_01.Y_Gate2` | `FB_SingleSolenoidFeedback` |
| `Y_Gripper` | FG_01 | `MAIN.Machine.FG_01.Y_Gripper` | `FB_DoubleSolenoidFeedback` |
| `Y_Platform` | FG_01 | `MAIN.Machine.FG_01.Y_Platform` | `FB_DoubleSolenoidFeedback` |
| `Y_ReaderWindow` | FG_01 | `MAIN.Machine.FG_01.Y_ReaderWindow` | `FB_DoubleSolenoidFeedback` |
| `Y_AxisR1` | FG_03 | `MAIN.Machine.FG_03.Y_AxisR1` | `FB_DoubleSolenoidFeedback` |
| `Y_AxisX1` | FG_03 | `MAIN.Machine.FG_03.Y_AxisX1` | `FB_DoubleSolenoidFeedback` |
| `Y_AxisX2` | FG_03 | `MAIN.Machine.FG_03.Y_AxisX2` | `FB_DoubleSolenoidFeedback` |
| `Y_AxisY1` | FG_03 | `MAIN.Machine.FG_03.Y_AxisY1` | `FB_DoubleSolenoidFeedback` |
| `Y_AxisY2` | FG_03 | `MAIN.Machine.FG_03.Y_AxisY2` | `FB_DoubleSolenoidFeedback` |
| `Y_Gripper1` | FG_03 | `MAIN.Machine.FG_03.Y_Gripper1` | `FB_DoubleSolenoidFeedback` |
| `Y_Gripper2` | FG_03 | `MAIN.Machine.FG_03.Y_Gripper2` | `FB_DoubleSolenoidFeedback` |
| `Y_AxisZ` | FG_04 | `MAIN.Machine.FG_04.Y_AxisZ` | `FB_DoubleSolenoidFeedback` |
| `Y_AxisR` | FG_05 | `MAIN.Machine.FG_05.Y_AxisR` | `FB_DoubleSolenoidFeedback` |
| `Y_AxisX` | FG_05 | `MAIN.Machine.FG_05.Y_AxisX` | `FB_DoubleSolenoidFeedback` |
| `Y_AxisZ1` | FG_05 | `MAIN.Machine.FG_05.Y_AxisZ1` | `FB_DoubleSolenoidFeedback` |
| `Y_AxisZ2` | FG_05 | `MAIN.Machine.FG_05.Y_AxisZ2` | `FB_DoubleSolenoidFeedback` |
| `Y_CapsSourceStopper` | FG_05 | `MAIN.Machine.FG_05.Y_CapsSourceStopper` | `FB_DoubleSolenoidFeedback` |
| `Y_Gripper` | FG_05 | `MAIN.Machine.FG_05.Y_Gripper` | `FB_DoubleSolenoidFeedback` |
| `Y_Lift` | FG_Transport | `MAIN.Machine.FG_Transport.Index01.Y_Lift` | `FB_DoubleSolenoidFeedback` |
| `Y_Stopper` | FG_Transport | `MAIN.Machine.FG_Transport.Index01.Y_Stopper` | `FB_SingleSolenoidFeedback` |
| `Y_Lift` | FG_Transport | `MAIN.Machine.FG_Transport.Index02.Y_Lift` | `FB_DoubleSolenoidFeedback` |
| `Y_Stopper` | FG_Transport | `MAIN.Machine.FG_Transport.Index02.Y_Stopper` | `FB_SingleSolenoidFeedback` |
| `Y_Lift` | FG_Transport | `MAIN.Machine.FG_Transport.Index03.Y_Lift` | `FB_DoubleSolenoidFeedback` |
| `Y_Stopper` | FG_Transport | `MAIN.Machine.FG_Transport.Index03.Y_Stopper` | `FB_SingleSolenoidFeedback` |
| `Y_Lift` | FG_Transport | `MAIN.Machine.FG_Transport.Index04.Y_Lift` | `FB_DoubleSolenoidFeedback` |
| `Y_Stopper` | FG_Transport | `MAIN.Machine.FG_Transport.Index04.Y_Stopper` | `FB_SingleSolenoidFeedback` |
| `Y_Lift` | FG_Transport | `MAIN.Machine.FG_Transport.Index05.Y_Lift` | `FB_DoubleSolenoidFeedback` |
| `Y_Stopper` | FG_Transport | `MAIN.Machine.FG_Transport.Index05.Y_Stopper` | `FB_SingleSolenoidFeedback` |
| `Y_Lift` | FG_Transport | `MAIN.Machine.FG_Transport.Lift01.Y_Lift` | `FB_DoubleSolenoidFeedback` |
| `Y_Lift` | FG_Transport | `MAIN.Machine.FG_Transport.Lift02.Y_Lift` | `FB_DoubleSolenoidFeedback` |
| `Y_Stopper` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper01.Y_Stopper` | `FB_SingleSolenoidFeedback` |
| `Y_Stopper` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper02.Y_Stopper` | `FB_SingleSolenoidFeedback` |
| `Y_Stopper` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper03.Y_Stopper` | `FB_SingleSolenoidFeedback` |
| `Y_Stopper` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper04.Y_Stopper` | `FB_SingleSolenoidFeedback` |
