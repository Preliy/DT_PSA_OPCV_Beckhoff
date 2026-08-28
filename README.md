# DT_PSA_OPCV — Beckhoff

The Beckhoff TwinCAT 3 realisation of [DT_PSA_OPCV](https://github.com/Preliy/DT_PSA_OPCV) — the Digital Twin for Laser Welding & Assembly System (PSA OPCV), a complete production line
that exists as a digital twin and is driven by a real PLC program.

## The architecture

![Unity and the TwinCAT emulation unit, with a TwinCAT machine PLC behind an emulated EtherCAT](https://raw.githubusercontent.com/Preliy/DT_PSA_OPCV/master/_docs/images/OC_Base_Beckhoff.svg)

Every [Open Commissioning](https://github.com/OpenCommissioning) setup has the same two parts: the
**Unity twin**, and an **emulation unit** — a TwinCAT project (`SIM_1`) holding the same device
hierarchy, generated and kept in step by OC Assistant. What makes this setup Beckhoff-shaped is what
is added on the control side: a **second TwinCAT PLC project, `PLC_1`**, carrying the machine
program, and the **real hardware configuration** — an `EtherCAT_1` master with all its terminals,
exactly as the cell would be wired. From that master an `EtherCAT_1_SIM` simulation device is
created; the two are coupled and run in full emulation.

```
Unity ⇄ SIM_1 ⇄ EtherCAT_1_SIM ⇄ EtherCAT_1 ⇄ PLC_1
```

**`PLC_1` never talks to Unity.** It talks to EtherCAT terminals, exactly as it would on the real
machine — which is the whole point: the control program cannot tell it is running against a twin, so
nothing about it has to change when it runs against steel.

```
   TwinCAT_1/PLC/TwinCAT.tsproj      one solution, two PLC projects, one EtherCAT pair
     PLC_1   AmsPort 851   the control program (SPT framework), drives EtherCAT_1
     SIM_1   AmsPort 852   the twin device layer, OC Assistant's output, on EtherCAT_1_SIM
   TwinCAT_1/HMI                     TE2000, bound to PLC_1 as ADS runtime PLC1
```

The same figure, with the Siemens variant beside it, is on the main repository's
[PLC connectivity page](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/04-plc-connectivity.md).
This module's own layout is in [03 · Architecture](_docs/03-architecture.md).

## How this is used

It is a module of the main repository: you clone it **into** that repo's root, as `Beckhoff/`.

```bash
git clone https://github.com/Preliy/DT_PSA_OPCV.git
cd DT_PSA_OPCV
git clone https://github.com/Preliy/DT_PSA_OPCV_Beckhoff.git Beckhoff
```

The main repo gitignores `/Beckhoff/`, so the two git repositories do not collide — inside here
everything is an ordinary checkout on an ordinary branch. Which versions pair with which is in the
main repo's [COMPATIBILITY.md](https://github.com/Preliy/DT_PSA_OPCV/blob/master/COMPATIBILITY.md).

**A standalone clone works too.** TwinCAT work needs no Unity and no twin, and this module carries a
committed copy of the machine's structure — `_workflow/config/handoff/.machine.json` — so every tool and
every generated page builds with nothing else present:

```bash
git clone https://github.com/Preliy/DT_PSA_OPCV_Beckhoff.git
cd DT_PSA_OPCV_Beckhoff
python _private/tools/build_plc_knowledge.py
```

## The control program is built on SPT

`PLC_1` is not ad-hoc ST. It is written on the **SPT Application Framework** — the PackML-based
application framework published by the [Beckhoff USA
Community](https://github.com/Beckhoff-USA-Community/SPT-Libraries) — and it follows that
framework's intended patterns rather than a private variation on them:

- **A hierarchy of equipment modules, not a flat program.** `Modules/00 Machine` is the machine unit
  and registers the seven functional groups as its submodules; each group under `Modules/NN FG_xx/`
  is a PackML state machine of its own, driven through the framework's state methods.
- **Reusable submodules where the machine repeats itself.** `FG_Transport` is a single equipment
  module with eleven submodules built from three reusable types — five Index, four Stopper and two
  Lift — rather than eleven copies of the same code.
- **Completion signalled the framework's way**, through the `NoStateTasksToComplete` /
  `StateTasksComplete` pair, so the framework owns the state transition and the application owns
  only the work.
- **A full recovery model.** Every group resets on its own cylinders and terminates on time, which
  is a machine-level contract rather than a TwinCAT detail — it is written down
  [in the main repository](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md).

The project runs the **V3.9** line of the libraries, while the published SPT documentation describes
V4 and disagrees with the shipped binary in several places — different enum literals, a few
identifiers, and some outright typos. Every identifier asserted in [the SPT framework
guideline](_docs/reference/spt-framework.md) was checked against the installed 3.9.0 library, and the
differences are recorded there. Read it before reusing anything from the public docs: **when a source
disagrees with the shipped binary, the binary wins.**

## Where to start

| | |
|---|---|
| [**Setup**](_docs/01-setup.md) | Installing TwinCAT, building the solution, connecting the twin |
| [**Usage**](_docs/02-usage.md) | Running the machine: startup order, the operator panel, the web HMI |
| [**Architecture**](_docs/03-architecture.md) | Why `PLC_1` and `SIM_1` are separate, and where the boundary runs |
| [**The machine in TwinCAT**](_docs/context/machine.md) | Generated: verified PLC paths, terminal mapping, process image |
| [**I/O map**](_docs/context/plc-io.md) | Which terminal channel every signal is on, and what is free |

These are also browsable as this repository's own
[wiki](https://github.com/Preliy/DT_PSA_OPCV_Beckhoff/wiki), which cross-links with the machine's
[wiki](https://github.com/Preliy/DT_PSA_OPCV/wiki) in the main repository.

## What this repository is master for

Its **realisation** only — function blocks, terminal channels, the HMI, the `.plcproj` mechanics.

It is not master for the machine's **structure** (that is the Unity twin, in the main repo) or its
**behaviour** — sequences, interlocks, fault codes and the reset model are machine-level contracts
every platform must honour, and they live in the main repo's
[`_docs/reference/`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md).
They were written from *this* module's ST, because that is where the behaviour was first made to
work — but what they state is the contract, not TwinCAT's version of it.

## Contributing

**Contributions are genuinely welcome.** A missing setup step, a bug you hit, a correction to
something we got wrong, an HMI page, a better recovery path — all of it.

The most useful thing right now is the setup procedure. [01 · Setup](_docs/01-setup.md) carries seven
`TODO(setup)` markers — steps that have not been captured from a working installation and were left
blank rather than guessed at. Filling one in is a small pull request with a large effect on everyone
who tries this next.

Two things to know before you start:

- **Behaviour changes belong upstream.** Sequences, interlocks, fault codes and the reset model are
  machine-level contracts every control platform has to honour, so they are written down in the main
  repository and changing them is a change to the machine, not to this module.
- **Follow the framework.** New control code goes on SPT, in the shape described above — and every
  identifier gets checked against the installed 3.9.0 library, not against the published V4 docs.

Start with the main repository's
[CONTRIBUTING.md](https://github.com/Preliy/DT_PSA_OPCV/blob/master/CONTRIBUTING.md), or just
[open an issue](https://github.com/Preliy/DT_PSA_OPCV_Beckhoff/issues) here to say what you are
starting.

## Licence

This repository's own work — the PLC source, the HMI pages, the documentation and the tooling — is
[GPL-3.0](LICENSE), Copyright © 2026 Viktor Gaponenko. Use it, learn from it, build on it. If you
share a modified version, it stays open for the next person.

### You need your own Beckhoff licences

**This project ships no Beckhoff software and no licence for any.** TwinCAT 3, the XAR runtime and
the TE2000 HMI engineering are Beckhoff products with their own terms, obtained from Beckhoff — and
whatever licences your use of them requires are **a matter between you and Beckhoff, not something
this project provides, arranges or is responsible for.** Trial licences are generated on your own
engineering system, in TwinCAT, by you.

What is in this repository is the *project*: PLC source, HMI pages, configuration and documentation.
It compiles and runs only on software you have licensed yourself. Nothing here is affiliated with,
endorsed by, or supported by Beckhoff Automation.

The third-party libraries this project builds against, and where each comes from, are listed in
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

Built on [Open Commissioning](https://github.com/OpenCommissioning).