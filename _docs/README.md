# Beckhoff documentation

The TwinCAT 3 side of DT_PSA_OPCV — installing it, running the machine
against it, and how the PLC projects are organised.

**Read the [main documentation](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/README.md) first.** It covers the machine, the Unity
twin, and everything that is not specific to a control platform. This set assumes you have the twin
open already.

| Page | Answers |
|---|---|
| [01 · Setup](01-setup.md) | What the PC needs, installing TwinCAT, isolated cores, the two network adapters and the loop cable, the PLC libraries, building and connecting to the twin |
| [02 · Usage](02-usage.md) | Running the machine: startup order, the operator panel, the web HMI |
| [03 · Architecture](03-architecture.md) | How `PLC_1` and `SIM_1` are organised, and why there are two |

## Where the TwinCAT realisation is described

**Not here.** Like the machine description in the main repository, the per-group TwinCAT detail is
**generated** from the PLC projects, so it cannot drift:

| Looking for | Read |
|---|---|
| What TwinCAT makes of the machine, group by group | [`_docs/context/machine.md`](../_docs/context/machine.md) |
| A group's verified control PLC paths and terminal mapping | [`_docs/context/fg-*.md`](../_docs/context/) |
| Which terminal channel every signal is on | [`_docs/context/plc-io.md`](../_docs/context/plc-io.md) |
| How the SPT framework is meant to be used | [`_docs/reference/spt-framework.md`](../_docs/reference/spt-framework.md) |
| Which signals are unlinked on purpose | [`_docs/reference/plc-io-exceptions.md`](../_docs/reference/plc-io-exceptions.md) |

Read [`_docs/context/PROVENANCE.md`](../_docs/context/PROVENANCE.md) first — it says how
current the type model is and which build of the twin export it was matched against.

## Behaviour is not documented here either

Sequences, the station handshake, interlocks, fault codes and the reset model are **machine-level
contracts** and live in the main repository, at
[`_docs/reference/`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md). They were written from
*this* module's ST — because that is where the behaviour was first made to work — but any control
platform running this line has to honour the same ones.

This module documents its **realisation** of those contracts, never a second version of them.

## Paths are main-repository-root relative

Every path in every generated document here is spelled from the main repository root, not from
`Beckhoff/` — so `Beckhoff/TwinCAT_1/PLC/PLC_1` rather than `TwinCAT_1/PLC/PLC_1`. That is the
level this project is written from, and it stays true when the module is read inside a main-repo
checkout.
