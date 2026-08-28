<!-- GENERATED from the TwinCAT type model and link file - do not edit. See _workflow/README.md. -->
<!-- Source: TwinCAT_1/PLC/TwinCAT.tsproj and Mapping_PLC.xml. Change the wiring in XAE or with plc_io.py, then re-run refreshing-project-knowledge. -->

# PLC I/O map

Which terminal channel every PLC signal is on, which channels are free, and whether the link file and the project still agree. Read from the tsproj and `Mapping_PLC.xml`; no TwinCAT and no Unity needed.

## The two masters

| Device | `<Device Id>` | Boxes | Driven by | Layout |
|---|---|---|---|---|
| `EtherCAT_1` | 1 | 1-43 | `PLC_1` (real master) | terminals nested under their EK1100 coupler |
| `EtherCAT_1_SIM` | 2286744 | 44-89 | `SIM_1` (EtherCAT simulation) | flat, identical names |

**The box names are identical on both masters - only the id tells them apart.** That is why the SIM side addresses terminals numerically as `TIIB(n)` while the control side uses the symbolic `TIID^EtherCAT_1^...` path, and why a `TIIB` number copied from the wrong master compiles and links to the wrong device.

## Terminals - `EtherCAT_1`

| Box | Terminal | Type | Width | Used | Free |
|---:|---|---|---:|---:|---|
| 29 | `FG_System_EK1100^FG_System_Panel_EL1809_1` | EL1809 | 16 DI | 10 | 11-16 |
| 28 | `FG_System_EK1100^FG_System_Panel_EL2809_1` | EL2809 | 16 DO | 14 | 15-16 |
| 27 | `FG_System_EK1100^FG_System_Door_EL1809_1` | EL1809 | 16 DI | 12 | 13-16 |
| 30 | `FG_System_EK1100^FG_System_Door_EL2008_1` | EL2008 | 8 DO | 6 | 7-8 |
| 9 | `FG_Transport_EK1100^FG_Transport_Index_EL1809_1` | EL1809 | 16 DI | 16 | - |
| 14 | `FG_Transport_EK1100^FG_Transport_Index_EL1809_2` | EL1809 | 16 DI | 14 | 15-16 |
| 10 | `FG_Transport_EK1100^FG_Transport_Stopper_EL1809_1` | EL1809 | 16 DI | 16 | - |
| 11 | `FG_Transport_EK1100^FG_Transport_Lift_EL1809_1` | EL1809 | 16 DI | 10 | 11-16 |
| 8 | `FG_Transport_EK1100^FG_Transport_Drive_EL1008_1` | EL1008 | 8 DI | 2 | 3-8 |
| 13 | `FG_Transport_EK1100^FG_Transport_Index_EL2809_1` | EL2809 | 16 DO | 15 | 16 |
| 5 | `FG_Transport_EK1100^FG_Transport_Stopper_EL2008_1` | EL2008 | 8 DO | 4 | 5-8 |
| 6 | `FG_Transport_EK1100^FG_Transport_Lift_EL2008_1` | EL2008 | 8 DO | 8 | - |
| 12 | `FG_Transport_EK1100^FG_Transport_Drive_EL2008_1` | EL2008 | 8 DO | 4 | 5-8 |
| 2 | `FG_01_EK1100^FG_01_EL1008_1` | EL1008 | 8 DI | 6 | 7-8 |
| 4 | `FG_01_EK1100^FG_01_EL1008_2` | EL1008 | 8 DI | 6 | 7-8 |
| 3 | `FG_01_EK1100^FG_01_EL2008_1` | EL2008 | 8 DO | 8 | - |
| 15 | `FG_01_EK1100^FG_01_EL1859_1` | EL1859 | 16 DI+DO | 16 | - |
| 16 | `FG_01_EK1100^FG_01_EL1859_2` | EL1859 | 16 DI+DO | 16 | - |
| 18 | `FG_02_EK1100^FG_02_EL1859_1` | EL1859 | 16 DI+DO | 16 | - |
| 22 | `FG_03_EK1100^FG_03_EL1809_1` | EL1809 | 16 DI | 16 | - |
| 23 | `FG_03_EK1100^FG_03_EL2809_1` | EL2809 | 16 DO | 14 | 15-16 |
| 24 | `FG_04_EK1100^FG_04_EL1008_1` | EL1008 | 8 DI | 3 | 4-8 |
| 25 | `FG_04_EK1100^FG_04_EL2008_1` | EL2008 | 8 DO | 2 | 3-8 |
| 40 | `FG_05_EK1100^FG_05_EL1809_1` | EL1809 | 16 DI | 14 | 15-16 |
| 41 | `FG_05_EK1100^FG_05_EL2809_1` | EL2809 | 16 DO | 12 | 13-16 |
| 42 | `FG_05_EK1100^FG_05_EL1859_1` | EL1859 | 16 DI+DO | 16 | - |
| 43 | `FG_05_EK1100^FG_05_EL1859_2` | EL1859 | 16 DI+DO | 16 | - |

**200 DI + 152 DO = 352 channels, 292 used, 60 free.**

## Allocation

### `FG_System_Panel_EL1809_1` (EL1809, 16 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.ControlSource_Panel.MainPMLControl_Simplified.StartPressed` | `Mapping_PLC.xml` |
| 2 | `MAIN.ControlSource_Panel.MainPMLControl_Simplified.ResetPressed` | `Mapping_PLC.xml` |
| 3 | `MAIN.ControlSource_Panel.MainPMLControl_Simplified.StopPressed` | `Mapping_PLC.xml` |
| 4 | `MAIN.ControlSource_Panel.ClearPressed` | `Mapping_PLC.xml` |
| 5 | `MAIN.ControlSource_Panel.AbortPressed` | `Mapping_PLC.xml` |
| 6 | `MAIN.ControlSource_Panel.ProductionPressed` | `Mapping_PLC.xml` |
| 7 | `MAIN.ControlSource_Panel.MaintenancePressed` | `Mapping_PLC.xml` |
| 8 | `MAIN.ControlSource_Panel.ManualPressed` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_System.SS_EStop1.HardwareInput` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_System.SS_EStop2.HardwareInput` | `Mapping_PLC.xml` |

### `FG_System_Panel_EL2809_1` (EL2809, 16 DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.ControlSource_Panel.LampStart` | `Mapping_PLC.xml` |
| 2 | `MAIN.ControlSource_Panel.LampReset` | `Mapping_PLC.xml` |
| 3 | `MAIN.ControlSource_Panel.LampStop` | `Mapping_PLC.xml` |
| 4 | `MAIN.ControlSource_Panel.LampClear` | `Mapping_PLC.xml` |
| 5 | `MAIN.ControlSource_Panel.LampAbort` | `Mapping_PLC.xml` |
| 6 | `MAIN.ControlSource_Panel.LampProduction` | `Mapping_PLC.xml` |
| 7 | `MAIN.ControlSource_Panel.LampMaintenance` | `Mapping_PLC.xml` |
| 8 | `MAIN.ControlSource_Panel.LampManual` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_System.H_SignalTower.Red` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_System.H_SignalTower.Yellow` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_System.H_SignalTower.Blue` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_System.H_SignalTower.Green` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_System.SS_EStop1.LampOutput` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_System.SS_EStop2.LampOutput` | `Mapping_PLC.xml` |

### `FG_System_Door_EL1809_1` (EL1809, 16 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_System.B_SafetyDoor11.ClosedSensor` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_System.B_SafetyDoor11.LockedSensor` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_System.B_SafetyDoor12.ClosedSensor` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_System.B_SafetyDoor12.LockedSensor` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_System.B_SafetyDoor13.ClosedSensor` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_System.B_SafetyDoor13.LockedSensor` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_System.B_SafetyDoor21.ClosedSensor` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_System.B_SafetyDoor21.LockedSensor` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_System.B_SafetyDoor22.ClosedSensor` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_System.B_SafetyDoor22.LockedSensor` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_System.B_SafetyDoor23.ClosedSensor` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_System.B_SafetyDoor23.LockedSensor` | `Mapping_PLC.xml` |

### `FG_System_Door_EL2008_1` (EL2008, 8 DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_System.B_SafetyDoor11.LockOutput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_System.B_SafetyDoor12.LockOutput` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_System.B_SafetyDoor13.LockOutput` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_System.B_SafetyDoor21.LockOutput` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_System.B_SafetyDoor22.LockOutput` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_System.B_SafetyDoor23.LockOutput` | `Mapping_PLC.xml` |

### `FG_Transport_Index_EL1809_1` (EL1809, 16 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_Transport.Index01.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_Transport.Index01.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_Transport.Index01.Y_Lift.RetractedSensor` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_Transport.Index01.Y_Lift.ExtendedSensor` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_Transport.Index01.Y_Stopper.RetractedSensor` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_Transport.Index01.Y_Stopper.ExtendedSensor` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_Transport.Index02.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_Transport.Index02.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_Transport.Index02.Y_Lift.RetractedSensor` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_Transport.Index02.Y_Lift.ExtendedSensor` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_Transport.Index02.Y_Stopper.RetractedSensor` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_Transport.Index02.Y_Stopper.ExtendedSensor` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_Transport.Index03.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_Transport.Index03.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 15 | `MAIN.Machine.FG_Transport.Index03.Y_Lift.RetractedSensor` | `Mapping_PLC.xml` |
| 16 | `MAIN.Machine.FG_Transport.Index03.Y_Lift.ExtendedSensor` | `Mapping_PLC.xml` |

### `FG_Transport_Index_EL1809_2` (EL1809, 16 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_Transport.Index03.Y_Stopper.RetractedSensor` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_Transport.Index03.Y_Stopper.ExtendedSensor` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_Transport.Index04.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_Transport.Index04.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_Transport.Index04.Y_Lift.RetractedSensor` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_Transport.Index04.Y_Lift.ExtendedSensor` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_Transport.Index04.Y_Stopper.RetractedSensor` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_Transport.Index04.Y_Stopper.ExtendedSensor` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_Transport.Index05.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_Transport.Index05.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_Transport.Index05.Y_Lift.RetractedSensor` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_Transport.Index05.Y_Lift.ExtendedSensor` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_Transport.Index05.Y_Stopper.RetractedSensor` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_Transport.Index05.Y_Stopper.ExtendedSensor` | `Mapping_PLC.xml` |

### `FG_Transport_Stopper_EL1809_1` (EL1809, 16 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_Transport.Stopper01.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_Transport.Stopper01.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_Transport.Stopper01.Y_Stopper.RetractedSensor` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_Transport.Stopper01.Y_Stopper.ExtendedSensor` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_Transport.Stopper02.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_Transport.Stopper02.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_Transport.Stopper02.Y_Stopper.RetractedSensor` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_Transport.Stopper02.Y_Stopper.ExtendedSensor` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_Transport.Stopper03.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_Transport.Stopper03.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_Transport.Stopper03.Y_Stopper.RetractedSensor` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_Transport.Stopper03.Y_Stopper.ExtendedSensor` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_Transport.Stopper04.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_Transport.Stopper04.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 15 | `MAIN.Machine.FG_Transport.Stopper04.Y_Stopper.RetractedSensor` | `Mapping_PLC.xml` |
| 16 | `MAIN.Machine.FG_Transport.Stopper04.Y_Stopper.ExtendedSensor` | `Mapping_PLC.xml` |

### `FG_Transport_Lift_EL1809_1` (EL1809, 16 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_Transport.Lift01.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_Transport.Lift01.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_Transport.Lift01.Y_Lift.RetractedSensor` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_Transport.Lift01.Y_Lift.ExtendedSensor` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_Transport.Lift01.M_Conveyor._DriveActive` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_Transport.Lift02.B_Detect.HardwareInput` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_Transport.Lift02.B_Exit.HardwareInput` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_Transport.Lift02.Y_Lift.RetractedSensor` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_Transport.Lift02.Y_Lift.ExtendedSensor` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_Transport.Lift02.M_Conveyor._DriveActive` | `Mapping_PLC.xml` |

### `FG_Transport_Drive_EL1008_1` (EL1008, 8 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_Transport.Transport01._DriveActive` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_Transport.Transport02._DriveActive` | `Mapping_PLC.xml` |

### `FG_Transport_Index_EL2809_1` (EL2809, 16 DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_Transport.Index01.Y_Lift._RetractOutput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_Transport.Index01.Y_Lift._ExtendOutput` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_Transport.Index01.Y_Stopper._ExtendOutput` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_Transport.Index02.Y_Lift._RetractOutput` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_Transport.Index02.Y_Lift._ExtendOutput` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_Transport.Index02.Y_Stopper._ExtendOutput` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_Transport.Index03.Y_Lift._RetractOutput` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_Transport.Index03.Y_Lift._ExtendOutput` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_Transport.Index03.Y_Stopper._ExtendOutput` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_Transport.Index04.Y_Lift._RetractOutput` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_Transport.Index04.Y_Lift._ExtendOutput` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_Transport.Index04.Y_Stopper._ExtendOutput` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_Transport.Index05.Y_Lift._RetractOutput` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_Transport.Index05.Y_Lift._ExtendOutput` | `Mapping_PLC.xml` |
| 15 | `MAIN.Machine.FG_Transport.Index05.Y_Stopper._ExtendOutput` | `Mapping_PLC.xml` |

### `FG_Transport_Stopper_EL2008_1` (EL2008, 8 DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_Transport.Stopper01.Y_Stopper._ExtendOutput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_Transport.Stopper02.Y_Stopper._ExtendOutput` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_Transport.Stopper03.Y_Stopper._ExtendOutput` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_Transport.Stopper04.Y_Stopper._ExtendOutput` | `Mapping_PLC.xml` |

### `FG_Transport_Lift_EL2008_1` (EL2008, 8 DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_Transport.Lift01.Y_Lift._RetractOutput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_Transport.Lift01.Y_Lift._ExtendOutput` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_Transport.Lift01.M_Conveyor._Backward` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_Transport.Lift01.M_Conveyor._Forward` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_Transport.Lift02.Y_Lift._RetractOutput` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_Transport.Lift02.Y_Lift._ExtendOutput` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_Transport.Lift02.M_Conveyor._Backward` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_Transport.Lift02.M_Conveyor._Forward` | `Mapping_PLC.xml` |

### `FG_Transport_Drive_EL2008_1` (EL2008, 8 DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_Transport.Transport01._Backward` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_Transport.Transport01._Forward` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_Transport.Transport02._Backward` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_Transport.Transport02._Forward` | `Mapping_PLC.xml` |

### `FG_01_EL1008_1` (EL1008, 8 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_01.Y_Gripper.RetractedSensor` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_01.Y_Gripper.ExtendedSensor` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_01.Y_Platform.RetractedSensor` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_01.Y_Platform.ExtendedSensor` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_01.Y_ReaderWindow.RetractedSensor` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_01.Y_ReaderWindow.ExtendedSensor` | `Mapping_PLC.xml` |

### `FG_01_EL1008_2` (EL1008, 8 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_01.Y_Gate1.RetractedSensor` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_01.Y_Gate1.ExtendedSensor` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_01.Y_Gate2.RetractedSensor` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_01.Y_Gate2.ExtendedSensor` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_01.B_SafetyGate1.HardwareInput` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_01.B_SafetyGate2.HardwareInput` | `Mapping_PLC.xml` |

### `FG_01_EL2008_1` (EL2008, 8 DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_01.Y_Gripper._ExtendOutput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_01.Y_Platform._ExtendOutput` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_01.Y_Platform._RetractOutput` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_01.Y_ReaderWindow._ExtendOutput` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_01.Y_Gripper._RetractOutput` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_01.Y_ReaderWindow._RetractOutput` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_01.Y_Gate1._ExtendOutput` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_01.Y_Gate2._ExtendOutput` | `Mapping_PLC.xml` |

### `FG_01_EL1859_1` (EL1859, 16 DI+DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_01.P_Camera.InputData` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_01.P_Camera.InputData` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_01.P_Camera.InputData` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_01.P_Camera.InputData` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_01.P_Camera.InputData` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_01.P_Camera.InputData` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_01.P_Camera.InputData` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_01.P_Camera.InputData` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_01.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_01.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_01.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_01.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_01.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_01.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 15 | `MAIN.Machine.FG_01.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 16 | `MAIN.Machine.FG_01.P_Camera.OutputData` | `Mapping_PLC.xml` |

### `FG_01_EL1859_2` (EL1859, 16 DI+DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_01.Y_LaserMark.InputData` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_01.Y_LaserMark.InputData` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_01.Y_LaserMark.InputData` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_01.Y_LaserMark.InputData` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_01.Y_LaserMark.InputData` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_01.Y_LaserMark.InputData` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_01.Y_LaserMark.InputData` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_01.Y_LaserMark.InputData` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_01.Y_LaserMark.OutputData` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_01.Y_LaserMark.OutputData` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_01.Y_LaserMark.OutputData` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_01.Y_LaserMark.OutputData` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_01.Y_LaserMark.OutputData` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_01.Y_LaserMark.OutputData` | `Mapping_PLC.xml` |
| 15 | `MAIN.Machine.FG_01.Y_LaserMark.OutputData` | `Mapping_PLC.xml` |
| 16 | `MAIN.Machine.FG_01.Y_LaserMark.OutputData` | `Mapping_PLC.xml` |

### `FG_02_EL1859_1` (EL1859, 16 DI+DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_02.P_Camera.InputData` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_02.P_Camera.InputData` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_02.P_Camera.InputData` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_02.P_Camera.InputData` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_02.P_Camera.InputData` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_02.P_Camera.InputData` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_02.P_Camera.InputData` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_02.P_Camera.InputData` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_02.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_02.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_02.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_02.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_02.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_02.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 15 | `MAIN.Machine.FG_02.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 16 | `MAIN.Machine.FG_02.P_Camera.OutputData` | `Mapping_PLC.xml` |

### `FG_03_EL1809_1` (EL1809, 16 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_03.Y_AxisX1.ExtendedSensor` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_03.Y_AxisX1.RetractedSensor` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_03.Y_AxisY1.ExtendedSensor` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_03.Y_AxisY1.RetractedSensor` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_03.Y_AxisR1.ExtendedSensor` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_03.Y_AxisR1.RetractedSensor` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_03.Y_Gripper1.ExtendedSensor` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_03.Y_Gripper1.RetractedSensor` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_03.Y_AxisX2.ExtendedSensor` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_03.Y_AxisX2.RetractedSensor` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_03.Y_AxisY2.ExtendedSensor` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_03.Y_AxisY2.RetractedSensor` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_03.Y_Gripper2.ExtendedSensor` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_03.Y_Gripper2.RetractedSensor` | `Mapping_PLC.xml` |
| 15 | `MAIN.Machine.FG_03.B_Detect1.HardwareInput` | `Mapping_PLC.xml` |
| 16 | `MAIN.Machine.FG_03.B_Detect2.HardwareInput` | `Mapping_PLC.xml` |

### `FG_03_EL2809_1` (EL2809, 16 DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_03.Y_AxisX1._ExtendOutput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_03.Y_AxisX1._RetractOutput` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_03.Y_AxisY1._ExtendOutput` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_03.Y_AxisY1._RetractOutput` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_03.Y_AxisR1._ExtendOutput` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_03.Y_AxisR1._RetractOutput` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_03.Y_Gripper1._ExtendOutput` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_03.Y_Gripper1._RetractOutput` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_03.Y_AxisX2._ExtendOutput` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_03.Y_AxisX2._RetractOutput` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_03.Y_AxisY2._ExtendOutput` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_03.Y_AxisY2._RetractOutput` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_03.Y_Gripper2._ExtendOutput` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_03.Y_Gripper2._RetractOutput` | `Mapping_PLC.xml` |

### `FG_04_EL1008_1` (EL1008, 8 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_04.Y_AxisZ.ExtendedSensor` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_04.Y_AxisZ.RetractedSensor` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_04.B_NIO.HardwareInput` | `Mapping_PLC.xml` |

### `FG_04_EL2008_1` (EL2008, 8 DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_04.Y_AxisZ._ExtendOutput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_04.Y_AxisZ._RetractOutput` | `Mapping_PLC.xml` |

### `FG_05_EL1809_1` (EL1809, 16 DI)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_05.Y_AxisX.ExtendedSensor` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_05.Y_AxisX.RetractedSensor` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_05.Y_AxisZ1.ExtendedSensor` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_05.Y_AxisZ1.RetractedSensor` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_05.Y_AxisZ2.ExtendedSensor` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_05.Y_AxisZ2.RetractedSensor` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_05.Y_AxisR.ExtendedSensor` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_05.Y_AxisR.RetractedSensor` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_05.Y_Gripper.ExtendedSensor` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_05.Y_Gripper.RetractedSensor` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_05.Y_CapsSourceStopper.ExtendedSensor` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_05.Y_CapsSourceStopper.RetractedSensor` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_05.B_Part.HardwareInput` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_05.B_Detect.HardwareInput` | `Mapping_PLC.xml` |

### `FG_05_EL2809_1` (EL2809, 16 DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_05.Y_AxisX._ExtendOutput` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_05.Y_AxisX._RetractOutput` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_05.Y_AxisZ1._ExtendOutput` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_05.Y_AxisZ1._RetractOutput` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_05.Y_AxisZ2._ExtendOutput` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_05.Y_AxisZ2._RetractOutput` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_05.Y_AxisR._ExtendOutput` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_05.Y_AxisR._RetractOutput` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_05.Y_Gripper._ExtendOutput` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_05.Y_Gripper._RetractOutput` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_05.Y_CapsSourceStopper._ExtendOutput` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_05.Y_CapsSourceStopper._RetractOutput` | `Mapping_PLC.xml` |

### `FG_05_EL1859_1` (EL1859, 16 DI+DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_05.Y_CapsSource.InputData` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_05.Y_CapsSource.InputData` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_05.Y_CapsSource.InputData` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_05.Y_CapsSource.InputData` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_05.Y_CapsSource.InputData` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_05.Y_CapsSource.InputData` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_05.Y_CapsSource.InputData` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_05.Y_CapsSource.InputData` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_05.Y_CapsSource.OutputData` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_05.Y_CapsSource.OutputData` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_05.Y_CapsSource.OutputData` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_05.Y_CapsSource.OutputData` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_05.Y_CapsSource.OutputData` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_05.Y_CapsSource.OutputData` | `Mapping_PLC.xml` |
| 15 | `MAIN.Machine.FG_05.Y_CapsSource.OutputData` | `Mapping_PLC.xml` |
| 16 | `MAIN.Machine.FG_05.Y_CapsSource.OutputData` | `Mapping_PLC.xml` |

### `FG_05_EL1859_2` (EL1859, 16 DI+DO)

| Ch | PLC symbol | Source |
|---:|---|---|
| 1 | `MAIN.Machine.FG_05.P_Camera.InputData` | `Mapping_PLC.xml` |
| 2 | `MAIN.Machine.FG_05.P_Camera.InputData` | `Mapping_PLC.xml` |
| 3 | `MAIN.Machine.FG_05.P_Camera.InputData` | `Mapping_PLC.xml` |
| 4 | `MAIN.Machine.FG_05.P_Camera.InputData` | `Mapping_PLC.xml` |
| 5 | `MAIN.Machine.FG_05.P_Camera.InputData` | `Mapping_PLC.xml` |
| 6 | `MAIN.Machine.FG_05.P_Camera.InputData` | `Mapping_PLC.xml` |
| 7 | `MAIN.Machine.FG_05.P_Camera.InputData` | `Mapping_PLC.xml` |
| 8 | `MAIN.Machine.FG_05.P_Camera.InputData` | `Mapping_PLC.xml` |
| 9 | `MAIN.Machine.FG_05.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 10 | `MAIN.Machine.FG_05.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 11 | `MAIN.Machine.FG_05.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 12 | `MAIN.Machine.FG_05.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 13 | `MAIN.Machine.FG_05.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 14 | `MAIN.Machine.FG_05.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 15 | `MAIN.Machine.FG_05.P_Camera.OutputData` | `Mapping_PLC.xml` |
| 16 | `MAIN.Machine.FG_05.P_Camera.OutputData` | `Mapping_PLC.xml` |

## Reconciliation

| | |
|---|---|
| Process-image symbols (`.tmc`) | 225 |
| Linked in the project (tsproj `<Mappings>`) | 222 |
| - from `Mapping_PLC.xml`, imported | 222 |
| - from `{attribute 'TcLinkTo'}` (`AutoLink="true"`) | 0 |
| Unlinked | 3 - 3 by design, 0 open |
| `Mapping_PLC.xml` vs tsproj drift | **none** - every link in the file is in the project |
| Channels booked twice | none |

**225 = 222 + 3.** If that identity ever fails, a signal is dead and no compiler will say so.

tsproj: `not committed` - `Mapping_PLC.xml`: `not committed`
