# Setup — TwinCAT

Installing the Beckhoff side and connecting it to the Unity twin.

**Do the [main setup](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/01-setup.md) first** — clone the repository and get the Unity
project opening. This page picks up from there.

> **Some steps are not yet written down.** Where this page says `TODO(setup)`, the procedure has not
> been captured from a working installation and is left blank rather than guessed at. Filling one in
> is the most useful contribution you can make to this page.

## 1. Prerequisites

| Component | Version | Notes |
|---|---|---|
| **TwinCAT 3** | `3.1.4026.25` | XAE (engineering) and XAR (runtime). The version the project was saved with |
| **TwinCAT HMI (TE2000)** | — | Only to build or edit the web HMI. Not needed to run the machine |
| **OC Assistant** | — | Generates the `SIM_1` twin device layer from the twin's device tree. `TODO(setup)`: which release, and where to get it |
| **Windows** | 10 / 11 | TwinCAT requires it |

### The PLC libraries

Neither PLC project compiles without these, and **neither set is in this repository** — TwinCAT
resolves both from your own library repository:

| Library | Used by | Where it comes from |
|---|---|---|
| **SPT Application Framework** — SPT Base Types 3.9.0, SPT Components 3.9.1, SPT Event Logger 3.9.0 (plus SPT Motion Control and SPT Utilities, 3.9.0, resolved with them) | `PLC_1` | Clone [Beckhoff-USA-Community/SPT-Libraries](https://github.com/Beckhoff-USA-Community/SPT-Libraries) and add its `Library Repository` folder as a TwinCAT PLC Library Repository. Pulling the repo then updates the libraries in XAE |
| **Open Commissioning** — `OC_Core`, `OC_EtherCAT` | `SIM_1` | [OC_TwinCAT_Core](https://github.com/OpenCommissioning/OC_TwinCAT_Core) |
| `Tc2_*` / `Tc3_*` | both | Installed with TwinCAT 3; nothing to fetch |

The project runs the **V3.9** SPT line while the published SPT documentation describes V4 — they
disagree in several places, and the differences that matter are in
[the SPT framework guideline](reference/spt-framework.md).

### Licences

**You need your own Beckhoff licences, and getting them is between you and Beckhoff.** This project
ships no Beckhoff software and no licence for any: TwinCAT 3 XAE, the XAR runtime and TE2000 are
Beckhoff products with their own terms. Trial licences are generated on your own engineering system,
in TwinCAT, by you.

**A clone never receives a licence file.** `*.tclrs` is excluded by `TwinCAT_1/.gitignore`, so the
`TrialLicense.tclrs` that sits in a maintainer's checkout is not distributed and is not yours to
reuse — the one your machine runs on is the one you generate in TwinCAT on that machine.

Everything this project builds against, and who owns it, is in
[THIRD-PARTY-NOTICES.md](../THIRD-PARTY-NOTICES.md).

- `TODO(setup)`: the exact licence activation a fresh machine needs — which licences the solution
  demands, and the trial-licence regeneration step.

## 2. The solution

Open `Beckhoff/TwinCAT_1/PLC_TwinCAT.sln` in TwinCAT XAE. One solution holds **two PLC
projects**, **one EtherCAT pair** and the HMI:

```
   PLC_1   AmsPort 851   the control program (SPT framework), drives EtherCAT_1
   SIM_1   AmsPort 852   the twin device layer, OC Assistant's output, on EtherCAT_1_SIM
```

Why two — and why it matters — is in [03 · Architecture](03-architecture.md). The short version:
`PLC_1` is the program under test and talks only to EtherCAT terminals, exactly as it would on the
real machine. `SIM_1` is what Unity binds to.

| Path | What |
|---|---|
| `TwinCAT_1/PLC/PLC_1` | The control program. `Modules/NN FG_xx/` per functional group |
| `TwinCAT_1/PLC/SIM_1` | Twin devices. Unity binds these ADS symbols |
| `TwinCAT_1/PLC/Mapping_PLC.xml` | The importable link file |
| `TwinCAT_1/PLC/OC_EtherCAT.ethml` | The EtherCAT topology description |
| `TwinCAT_1/HMI` | TE2000 panels, `HMI.hmiproj` |

## 3. Build and activate

1. Build `PLC_1`.
2. Build `SIM_1`.
3. Activate Configuration.
4. Put the runtime into **Run** mode.

- `TODO(setup)`: the `EtherCAT_1` / `EtherCAT_1_SIM` pairing — what has to be configured on a
  machine that has never run this project, and in what order relative to Activate Configuration.
- `TODO(setup)`: whether OC Assistant has to be run before the first build, or only when the twin's
  device list changes.

## 4. Connecting the twin

Unity binds the twin's devices to `SIM_1` over ADS on **port 852**. Unity and TwinCAT on the same
machine is the simple case.

- `TODO(setup)`: creating the ADS route, and what to enter when Unity and TwinCAT are on different
  machines.

Start the TwinCAT runtime **first**, then enter Play mode in Unity.

## 5. The web HMI (optional)

`Beckhoff/TwinCAT_1/HMI` is a TE2000 project bound to `PLC_1`. Its server config
(`Server/ADS/ADS.Config.default.json`) maps the runtime alias `PLC1` to `127.0.0.1.1.1`
**port 851**, so page bindings read `ADS.PLC1.MAIN.…`.

**The binding is by ADS port, not by project name.** Renaming the PLC project does not break it — and
"fixing" a binding by renaming it after the PLC project is a mistake.

- `TODO(setup)`: how to start the HMI server and reach the pages in a browser.

## 6. The generated documentation (optional)

The [TwinCAT description of the machine](../_docs/context/machine.md) is generated and
**committed**, so you do not need TwinCAT — or any of the build tooling — to read it.

It is refreshed by the maintainers whenever the TwinCAT projects change. The type model it is
built from is committed as `_docs/context/.plc-image.json`, so every page here can be read — and
checked against the solution — with no TwinCAT installed.

## 7. Checking it worked

| Check | Expect |
|---|---|
| TwinCAT in Run, Unity in Play on `VC_Demo_1_Beckhoff_1` | Devices respond to the PLC; the on-screen panel drives the machine |
| The operator panel's Reset, then Start | The line runs the ring: pallets circulate and every station processes |
