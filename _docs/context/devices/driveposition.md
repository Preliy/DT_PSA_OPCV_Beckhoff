<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# DrivePosition in TwinCAT

**2 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`DrivePosition`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/driveposition.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_Component_BasicAxis` | 2 |

### `FB_Component_BasicAxis`

_No process-image members - this type reaches no terminal._

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `Y_Lift` | FG_Transport | `MAIN.Machine.FG_Transport.Lift01.Y_Lift` | `FB_Component_BasicAxis` |
| `Y_Lift` | FG_Transport | `MAIN.Machine.FG_Transport.Lift02.Y_Lift` | `FB_Component_BasicAxis` |
