<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# SensorBinary in TwinCAT

**25 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`SensorBinary`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/sensorbinary.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_DigitalSensor` | 25 |

### `FB_DigitalSensor`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `HardwareInput` | IN | `BOOL` | 1 |

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `B_SafetyGate1` | FG_01 | `MAIN.Machine.FG_01.B_SafetyGate1` | `FB_DigitalSensor` |
| `B_SafetyGate2` | FG_01 | `MAIN.Machine.FG_01.B_SafetyGate2` | `FB_DigitalSensor` |
| `B_Part` | FG_05 | `MAIN.Machine.FG_05.B_Part` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Index01.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Index01.B_Exit` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Index02.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Index02.B_Exit` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Index03.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Index03.B_Exit` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Index04.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Index04.B_Exit` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Index05.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Index05.B_Exit` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Lift01.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Lift01.B_Exit` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Lift02.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Lift02.B_Exit` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper01.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper01.B_Exit` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper02.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper02.B_Exit` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper03.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper03.B_Exit` | `FB_DigitalSensor` |
| `B_Detect` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper04.B_Detect` | `FB_DigitalSensor` |
| `B_Exit` | FG_Transport | `MAIN.Machine.FG_Transport.Stopper04.B_Exit` | `FB_DigitalSensor` |
