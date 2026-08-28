<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# SignalBinary in TwinCAT

**4 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`SignalBinary`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/signalbinary.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_DigitalSensor` | 4 |

### `FB_DigitalSensor`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `HardwareInput` | IN | `BOOL` | 1 |

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `B_Detect1` | FG_03 | `MAIN.Machine.FG_03.B_Detect1` | `FB_DigitalSensor` |
| `B_Detect2` | FG_03 | `MAIN.Machine.FG_03.B_Detect2` | `FB_DigitalSensor` |
| `B_NIO` | FG_04 | `MAIN.Machine.FG_04.B_NIO` | `FB_DigitalSensor` |
| `B_Detect` | FG_05 | `MAIN.Machine.FG_05.B_Detect` | `FB_DigitalSensor` |
