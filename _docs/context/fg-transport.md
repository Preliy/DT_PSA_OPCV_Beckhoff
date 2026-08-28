<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# FG_Transport in TwinCAT

The control side only. What FG_Transport *is* - its scene hierarchy, its devices and everything a human authored about it - is in the main repo: [`FG_Transport`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/fg-transport.md).

| | |
|---|---|
| Twin PLC path | `MAIN.FG_Transport` |
| Control PLC path | `MAIN.Machine.FG_Transport` |
| Module | `FG_Transport EXTENDS FB_PackML_BaseModule` |
| Served by | — |
| Devices | 42 |
| Behaviour | [`transport-behaviour.md`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md) |

## Components

| Symbol | Device type | Twin FB | Control PLC path | I/O | Linked |
|---|---|---|---|---:|---:|
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Index01.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Index01.B_Exit` | 1 | 1 |
| `Y_Lift` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Index01.Y_Lift` | 4 | 4 |
| `Y_Stopper` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Index01.Y_Stopper` | 3 | 3 |
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Index02.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Index02.B_Exit` | 1 | 1 |
| `Y_Lift` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Index02.Y_Lift` | 4 | 4 |
| `Y_Stopper` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Index02.Y_Stopper` | 3 | 3 |
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Index03.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Index03.B_Exit` | 1 | 1 |
| `Y_Lift` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Index03.Y_Lift` | 4 | 4 |
| `Y_Stopper` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Index03.Y_Stopper` | 3 | 3 |
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Index04.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Index04.B_Exit` | 1 | 1 |
| `Y_Lift` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Index04.Y_Lift` | 4 | 4 |
| `Y_Stopper` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Index04.Y_Stopper` | 3 | 3 |
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Index05.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Index05.B_Exit` | 1 | 1 |
| `Y_Lift` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Index05.Y_Lift` | 4 | 4 |
| `Y_Stopper` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Index05.Y_Stopper` | 3 | 3 |
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Lift01.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Lift01.B_Exit` | 1 | 1 |
| `M_Conveyor` | DriveSimple | `FB_Drive` | `MAIN.Machine.FG_Transport.Lift01.M_Conveyor` | 3 | 3 |
| `Y_Lift` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Lift01.Y_Lift` | 4 | 4 |
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Lift02.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Lift02.B_Exit` | 1 | 1 |
| `M_Conveyor` | DriveSimple | `FB_Drive` | `MAIN.Machine.FG_Transport.Lift02.M_Conveyor` | 3 | 3 |
| `Y_Lift` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Lift02.Y_Lift` | 4 | 4 |
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Stopper01.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Stopper01.B_Exit` | 1 | 1 |
| `Y_Stopper` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Stopper01.Y_Stopper` | 3 | 3 |
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Stopper02.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Stopper02.B_Exit` | 1 | 1 |
| `Y_Stopper` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Stopper02.Y_Stopper` | 3 | 3 |
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Stopper03.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Stopper03.B_Exit` | 1 | 1 |
| `Y_Stopper` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Stopper03.Y_Stopper` | 3 | 3 |
| `B_Detect` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Stopper04.B_Detect` | 1 | 1 |
| `B_Exit` | SensorBinary | `FB_SensorBinary` | `MAIN.Machine.FG_Transport.Stopper04.B_Exit` | 1 | 1 |
| `Y_Stopper` | Cylinder | `FB_Cylinder` | `MAIN.Machine.FG_Transport.Stopper04.Y_Stopper` | 3 | 3 |
| `M_Conveyor` | DriveSimple | `FB_Drive` | `MAIN.Machine.FG_Transport.Transport01` ¹ | 3 | 3 |
| `M_Conveyor` | DriveSimple | `FB_Drive` | `MAIN.Machine.FG_Transport.Transport02` ¹ | 3 | 3 |

¹ **Folded.** The PLC has no member of its own for this device — the unit named here *is* the device, and owns the process image. A twin child that the control side does not model separately.

**The twin path is not the control path.** Only the control PLC path works in an HMI binding or a `TcLinkTo` pragma, and the twin's spelling fails silently in both.

## SIM_1

| | |
|---|---|
| POU | `TwinCAT_1/PLC/SIM_1/FG_Transport/FG_Transport.TcPOU` |
| In `.plcproj` | yes |
| `Mapping` targets | GVL_EtherCAT_1_SIM |
| `Mapping` lines | 89 |

Only the `Mapping` action is ours. The `{region generated code}` block belongs to OC Assistant and is overwritten on the next twin regeneration.

## PLC_1

| | |
|---|---|
| POU | `TwinCAT_1/PLC/PLC_1/Modules/10 FG_Transport/FG_Transport.TcPOU` |
| In `.plcproj` | yes |
| PackML states | `Execute`, `Aborting`, `Clearing`, `Stopping`, `Resetting` |
| Fault codes | — |
| HMI struct | `ST_BaseModule_HMI` |
| Other POUs | `FB_TransferIndex.TcPOU`, `FB_TransferLift.TcPOU`, `FB_TransferStopper.TcPOU` |

Fault codes are read from `_FaultCode :=` in the ST. What each one *means* is behaviour and lives in the reference page named in the header.

## Mapping

| Process image member | Dir | Terminal | Via |
|---|---|---|---|
| `Index01.B_Detect.HardwareInput` | IN | FG_Transport_Index_EL1809_1 channel 1 | Mapping_PLC.xml |
| `Index01.B_Exit.HardwareInput` | IN | FG_Transport_Index_EL1809_1 channel 2 | Mapping_PLC.xml |
| `Index01.Y_Lift.ExtendedSensor` | IN | FG_Transport_Index_EL1809_1 channel 4 | Mapping_PLC.xml |
| `Index01.Y_Lift.RetractedSensor` | IN | FG_Transport_Index_EL1809_1 channel 3 | Mapping_PLC.xml |
| `Index01.Y_Lift._ExtendOutput` | OUT | FG_Transport_Index_EL2809_1 channel 2 | Mapping_PLC.xml |
| `Index01.Y_Lift._RetractOutput` | OUT | FG_Transport_Index_EL2809_1 channel 1 | Mapping_PLC.xml |
| `Index01.Y_Stopper.ExtendedSensor` | IN | FG_Transport_Index_EL1809_1 channel 6 | Mapping_PLC.xml |
| `Index01.Y_Stopper.RetractedSensor` | IN | FG_Transport_Index_EL1809_1 channel 5 | Mapping_PLC.xml |
| `Index01.Y_Stopper._ExtendOutput` | OUT | FG_Transport_Index_EL2809_1 channel 3 | Mapping_PLC.xml |
| `Index02.B_Detect.HardwareInput` | IN | FG_Transport_Index_EL1809_1 channel 7 | Mapping_PLC.xml |
| `Index02.B_Exit.HardwareInput` | IN | FG_Transport_Index_EL1809_1 channel 8 | Mapping_PLC.xml |
| `Index02.Y_Lift.ExtendedSensor` | IN | FG_Transport_Index_EL1809_1 channel 10 | Mapping_PLC.xml |
| `Index02.Y_Lift.RetractedSensor` | IN | FG_Transport_Index_EL1809_1 channel 9 | Mapping_PLC.xml |
| `Index02.Y_Lift._ExtendOutput` | OUT | FG_Transport_Index_EL2809_1 channel 5 | Mapping_PLC.xml |
| `Index02.Y_Lift._RetractOutput` | OUT | FG_Transport_Index_EL2809_1 channel 4 | Mapping_PLC.xml |
| `Index02.Y_Stopper.ExtendedSensor` | IN | FG_Transport_Index_EL1809_1 channel 12 | Mapping_PLC.xml |
| `Index02.Y_Stopper.RetractedSensor` | IN | FG_Transport_Index_EL1809_1 channel 11 | Mapping_PLC.xml |
| `Index02.Y_Stopper._ExtendOutput` | OUT | FG_Transport_Index_EL2809_1 channel 6 | Mapping_PLC.xml |
| `Index03.B_Detect.HardwareInput` | IN | FG_Transport_Index_EL1809_1 channel 13 | Mapping_PLC.xml |
| `Index03.B_Exit.HardwareInput` | IN | FG_Transport_Index_EL1809_1 channel 14 | Mapping_PLC.xml |
| `Index03.Y_Lift.ExtendedSensor` | IN | FG_Transport_Index_EL1809_1 channel 16 | Mapping_PLC.xml |
| `Index03.Y_Lift.RetractedSensor` | IN | FG_Transport_Index_EL1809_1 channel 15 | Mapping_PLC.xml |
| `Index03.Y_Lift._ExtendOutput` | OUT | FG_Transport_Index_EL2809_1 channel 8 | Mapping_PLC.xml |
| `Index03.Y_Lift._RetractOutput` | OUT | FG_Transport_Index_EL2809_1 channel 7 | Mapping_PLC.xml |
| `Index03.Y_Stopper.ExtendedSensor` | IN | FG_Transport_Index_EL1809_2 channel 2 | Mapping_PLC.xml |
| `Index03.Y_Stopper.RetractedSensor` | IN | FG_Transport_Index_EL1809_2 channel 1 | Mapping_PLC.xml |
| `Index03.Y_Stopper._ExtendOutput` | OUT | FG_Transport_Index_EL2809_1 channel 9 | Mapping_PLC.xml |
| `Index04.B_Detect.HardwareInput` | IN | FG_Transport_Index_EL1809_2 channel 3 | Mapping_PLC.xml |
| `Index04.B_Exit.HardwareInput` | IN | FG_Transport_Index_EL1809_2 channel 4 | Mapping_PLC.xml |
| `Index04.Y_Lift.ExtendedSensor` | IN | FG_Transport_Index_EL1809_2 channel 6 | Mapping_PLC.xml |
| `Index04.Y_Lift.RetractedSensor` | IN | FG_Transport_Index_EL1809_2 channel 5 | Mapping_PLC.xml |
| `Index04.Y_Lift._ExtendOutput` | OUT | FG_Transport_Index_EL2809_1 channel 11 | Mapping_PLC.xml |
| `Index04.Y_Lift._RetractOutput` | OUT | FG_Transport_Index_EL2809_1 channel 10 | Mapping_PLC.xml |
| `Index04.Y_Stopper.ExtendedSensor` | IN | FG_Transport_Index_EL1809_2 channel 8 | Mapping_PLC.xml |
| `Index04.Y_Stopper.RetractedSensor` | IN | FG_Transport_Index_EL1809_2 channel 7 | Mapping_PLC.xml |
| `Index04.Y_Stopper._ExtendOutput` | OUT | FG_Transport_Index_EL2809_1 channel 12 | Mapping_PLC.xml |
| `Index05.B_Detect.HardwareInput` | IN | FG_Transport_Index_EL1809_2 channel 9 | Mapping_PLC.xml |
| `Index05.B_Exit.HardwareInput` | IN | FG_Transport_Index_EL1809_2 channel 10 | Mapping_PLC.xml |
| `Index05.Y_Lift.ExtendedSensor` | IN | FG_Transport_Index_EL1809_2 channel 12 | Mapping_PLC.xml |
| `Index05.Y_Lift.RetractedSensor` | IN | FG_Transport_Index_EL1809_2 channel 11 | Mapping_PLC.xml |
| `Index05.Y_Lift._ExtendOutput` | OUT | FG_Transport_Index_EL2809_1 channel 14 | Mapping_PLC.xml |
| `Index05.Y_Lift._RetractOutput` | OUT | FG_Transport_Index_EL2809_1 channel 13 | Mapping_PLC.xml |
| `Index05.Y_Stopper.ExtendedSensor` | IN | FG_Transport_Index_EL1809_2 channel 14 | Mapping_PLC.xml |
| `Index05.Y_Stopper.RetractedSensor` | IN | FG_Transport_Index_EL1809_2 channel 13 | Mapping_PLC.xml |
| `Index05.Y_Stopper._ExtendOutput` | OUT | FG_Transport_Index_EL2809_1 channel 15 | Mapping_PLC.xml |
| `Lift01.B_Detect.HardwareInput` | IN | FG_Transport_Lift_EL1809_1 channel 1 | Mapping_PLC.xml |
| `Lift01.B_Exit.HardwareInput` | IN | FG_Transport_Lift_EL1809_1 channel 2 | Mapping_PLC.xml |
| `Lift01.M_Conveyor._Backward` | OUT | FG_Transport_Lift_EL2008_1 channel 3 | Mapping_PLC.xml |
| `Lift01.M_Conveyor._DriveActive` | IN | FG_Transport_Lift_EL1809_1 channel 5 | Mapping_PLC.xml |
| `Lift01.M_Conveyor._Forward` | OUT | FG_Transport_Lift_EL2008_1 channel 4 | Mapping_PLC.xml |
| `Lift01.Y_Lift.ExtendedSensor` | IN | FG_Transport_Lift_EL1809_1 channel 4 | Mapping_PLC.xml |
| `Lift01.Y_Lift.RetractedSensor` | IN | FG_Transport_Lift_EL1809_1 channel 3 | Mapping_PLC.xml |
| `Lift01.Y_Lift._ExtendOutput` | OUT | FG_Transport_Lift_EL2008_1 channel 2 | Mapping_PLC.xml |
| `Lift01.Y_Lift._RetractOutput` | OUT | FG_Transport_Lift_EL2008_1 channel 1 | Mapping_PLC.xml |
| `Lift02.B_Detect.HardwareInput` | IN | FG_Transport_Lift_EL1809_1 channel 6 | Mapping_PLC.xml |
| `Lift02.B_Exit.HardwareInput` | IN | FG_Transport_Lift_EL1809_1 channel 7 | Mapping_PLC.xml |
| `Lift02.M_Conveyor._Backward` | OUT | FG_Transport_Lift_EL2008_1 channel 7 | Mapping_PLC.xml |
| `Lift02.M_Conveyor._DriveActive` | IN | FG_Transport_Lift_EL1809_1 channel 10 | Mapping_PLC.xml |
| `Lift02.M_Conveyor._Forward` | OUT | FG_Transport_Lift_EL2008_1 channel 8 | Mapping_PLC.xml |
| `Lift02.Y_Lift.ExtendedSensor` | IN | FG_Transport_Lift_EL1809_1 channel 9 | Mapping_PLC.xml |
| `Lift02.Y_Lift.RetractedSensor` | IN | FG_Transport_Lift_EL1809_1 channel 8 | Mapping_PLC.xml |
| `Lift02.Y_Lift._ExtendOutput` | OUT | FG_Transport_Lift_EL2008_1 channel 6 | Mapping_PLC.xml |
| `Lift02.Y_Lift._RetractOutput` | OUT | FG_Transport_Lift_EL2008_1 channel 5 | Mapping_PLC.xml |
| `Stopper01.B_Detect.HardwareInput` | IN | FG_Transport_Stopper_EL1809_1 channel 1 | Mapping_PLC.xml |
| `Stopper01.B_Exit.HardwareInput` | IN | FG_Transport_Stopper_EL1809_1 channel 2 | Mapping_PLC.xml |
| `Stopper01.Y_Stopper.ExtendedSensor` | IN | FG_Transport_Stopper_EL1809_1 channel 4 | Mapping_PLC.xml |
| `Stopper01.Y_Stopper.RetractedSensor` | IN | FG_Transport_Stopper_EL1809_1 channel 3 | Mapping_PLC.xml |
| `Stopper01.Y_Stopper._ExtendOutput` | OUT | FG_Transport_Stopper_EL2008_1 channel 1 | Mapping_PLC.xml |
| `Stopper02.B_Detect.HardwareInput` | IN | FG_Transport_Stopper_EL1809_1 channel 5 | Mapping_PLC.xml |
| `Stopper02.B_Exit.HardwareInput` | IN | FG_Transport_Stopper_EL1809_1 channel 6 | Mapping_PLC.xml |
| `Stopper02.Y_Stopper.ExtendedSensor` | IN | FG_Transport_Stopper_EL1809_1 channel 8 | Mapping_PLC.xml |
| `Stopper02.Y_Stopper.RetractedSensor` | IN | FG_Transport_Stopper_EL1809_1 channel 7 | Mapping_PLC.xml |
| `Stopper02.Y_Stopper._ExtendOutput` | OUT | FG_Transport_Stopper_EL2008_1 channel 2 | Mapping_PLC.xml |
| `Stopper03.B_Detect.HardwareInput` | IN | FG_Transport_Stopper_EL1809_1 channel 9 | Mapping_PLC.xml |
| `Stopper03.B_Exit.HardwareInput` | IN | FG_Transport_Stopper_EL1809_1 channel 10 | Mapping_PLC.xml |
| `Stopper03.Y_Stopper.ExtendedSensor` | IN | FG_Transport_Stopper_EL1809_1 channel 12 | Mapping_PLC.xml |
| `Stopper03.Y_Stopper.RetractedSensor` | IN | FG_Transport_Stopper_EL1809_1 channel 11 | Mapping_PLC.xml |
| `Stopper03.Y_Stopper._ExtendOutput` | OUT | FG_Transport_Stopper_EL2008_1 channel 3 | Mapping_PLC.xml |
| `Stopper04.B_Detect.HardwareInput` | IN | FG_Transport_Stopper_EL1809_1 channel 13 | Mapping_PLC.xml |
| `Stopper04.B_Exit.HardwareInput` | IN | FG_Transport_Stopper_EL1809_1 channel 14 | Mapping_PLC.xml |
| `Stopper04.Y_Stopper.ExtendedSensor` | IN | FG_Transport_Stopper_EL1809_1 channel 16 | Mapping_PLC.xml |
| `Stopper04.Y_Stopper.RetractedSensor` | IN | FG_Transport_Stopper_EL1809_1 channel 15 | Mapping_PLC.xml |
| `Stopper04.Y_Stopper._ExtendOutput` | OUT | FG_Transport_Stopper_EL2008_1 channel 4 | Mapping_PLC.xml |
| `Transport01._Backward` | OUT | FG_Transport_Drive_EL2008_1 channel 1 | Mapping_PLC.xml |
| `Transport01._DriveActive` | IN | FG_Transport_Drive_EL1008_1 channel 1 | Mapping_PLC.xml |
| `Transport01._Forward` | OUT | FG_Transport_Drive_EL2008_1 channel 2 | Mapping_PLC.xml |
| `Transport02._Backward` | OUT | FG_Transport_Drive_EL2008_1 channel 3 | Mapping_PLC.xml |
| `Transport02._DriveActive` | IN | FG_Transport_Drive_EL1008_1 channel 2 | Mapping_PLC.xml |
| `Transport02._Forward` | OUT | FG_Transport_Drive_EL2008_1 channel 4 | Mapping_PLC.xml |

89 members, 89 linked, **0 unlinked**. A declared but unlinked signal compiles and is silently dead - see [plc-io.md](plc-io.md) for the channel map and [plc-io-exceptions.md](../reference/plc-io-exceptions.md) for the ones that are unlinked on purpose.
