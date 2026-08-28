<!-- GENERATED from the machine handoff and the TwinCAT solution - do not edit. The build sweeps this directory; see _workflow/README.md. -->
<!-- Sources: _docs/context/.machine.json (the twin's structure) and the TwinCAT solution in Beckhoff/TwinCAT_1/. Edit the scene's ContextNodes or the PLC, then re-run refreshing-project-knowledge. -->

# Beckhoff — the machine in TwinCAT

How the twin's structure is realised on Beckhoff hardware. The machine itself - what the groups are, how the pallet ring works, what each group is *for* - is in the main repo: [the machine](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/context/machine.md).

| | |
|---|---|
| Control PLC | `PLC_1`, AmsPort 851, drives the `EtherCAT_1` master |
| Twin devices | `SIM_1`, AmsPort 852, bound by Unity over ADS |
| HMI | TE2000, bound to `PLC_1` as ADS runtime `PLC1` (by **port**, not by project name) |
| Solution | `TwinCAT_1/PLC_TwinCAT.sln` |

## Groups

| Group | Control PLC path | Module | Devices | Process image | Linked |
|---|---|---|---:|---:|---:|
| [FG_System](fg-system.md) | `MAIN.Machine.FG_System` | yes | 10 | 26 | 26 |
| [FG_Transport](fg-transport.md) | `MAIN.Machine.FG_Transport` | yes | 42 | 89 | 89 |
| [FG_01](fg-01.md) | `MAIN.Machine.FG_01` | yes | 9 | 24 | 24 |
| [FG_02](fg-02.md) | `MAIN.Machine.FG_02` | yes | 1 | 2 | 2 |
| [FG_03](fg-03.md) | `MAIN.Machine.FG_03` | yes | 9 | 30 | 30 |
| [FG_04](fg-04.md) | `MAIN.Machine.FG_04` | yes | 2 | 5 | 5 |
| [FG_05](fg-05.md) | `MAIN.Machine.FG_05` | yes | 10 | 30 | 30 |

## Also here

| Page | Answers |
|---|---|
| [plc-io.md](plc-io.md) | Which terminal channel every signal is on, what is free, and whether the link file and the project agree |
| [devices/](devices/) | Per twin device type: which control FB it becomes, its process-image members and channel widths |
| [`../reference/spt-framework.md`](../reference/spt-framework.md) | How the SPT framework is meant to be used, checked against the shipped V3.9 binary |
| [`../reference/plc-io-exceptions.md`](../reference/plc-io-exceptions.md) | Which signals are unlinked on purpose |

**Behaviour is not here.** Sequences, interlocks, fault codes and the reset model are machine-level contracts that any control platform has to honour, and they live in [the behaviour contracts](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md) in the main repo.
