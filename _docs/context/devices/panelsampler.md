<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# PanelSampler in TwinCAT

**2 instances.** What this device type *is* - its authored description, its bit layout, the full instance list with twin paths - is in the main repo: [`PanelSampler`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/devices/panelsampler.md). This page states only what TwinCAT makes of it.

## Control function blocks

| Control FB | Instances |
|---|---:|
| `FB_SignalTower` | 1 |

### `FB_SignalTower`

| Process-image member | Dir | Type | Channels |
|---|---|---|---:|
| `Red` | OUT | `BOOL` | 1 |
| `Yellow` | OUT | `BOOL` | 1 |
| `Blue` | OUT | `BOOL` | 1 |
| `Green` | OUT | `BOOL` | 1 |

Published to the HMI: `HMI : ST_SignalTower_HMI`

## Instances

| Symbol | Group | Control PLC path | Control FB |
|---|---|---|---|
| `H_ControlPanel` | FG_System | — | — |
| `H_SignalTower` | FG_System | `MAIN.Machine.FG_System.H_SignalTower` | `FB_SignalTower` |
