# Third-party notices

DT_PSA_OPCV_Beckhoff is licensed under [GPL-3.0](LICENSE). It is built against the third-party
components listed below, each under its own licence and copyright.

**This repository redistributes almost none of them.** The PLC libraries are resolved by TwinCAT
from your own library repository, the HMI packages are restored by NuGet from Beckhoff's feed
(`TwinCAT_1/Packages/` is git-ignored), and TwinCAT itself is not here at all. What is committed is
this project's own source: PLC POUs, HMI pages, configuration and documentation. The one third-party
file that does travel with the repository is called out under *Documents* below.

A licence here describes the component, not this project — **nothing below is granted to you by
us.**

## You need your own Beckhoff licences

TwinCAT 3 (XAE engineering and XAR runtime) and TwinCAT HMI Engineering (TE2000) are **Beckhoff
products**. This project does not ship them, does not ship a licence for them, and cannot grant you
one. Obtaining whatever licences your use requires — a trial licence you generate yourself on your
own engineering system, or a purchased one — is **between you and Beckhoff**.

Nothing in this repository is affiliated with, endorsed by, or supported by Beckhoff Automation.

| Beckhoff product | Needed for |
|---|---|
| **TwinCAT 3 XAE** | Opening and building the solution |
| **TwinCAT 3 XAR** (runtime) | Running the machine — the PLC and the EtherCAT emulation |
| **TwinCAT HMI Engineering (TE2000)** | Only to edit or build the web HMI. Not needed to run the machine. Anything beyond engineering use of the HMI server has its own Beckhoff licensing — ask Beckhoff |

## PLC libraries — `PLC_1`, the control program

| Library | Version | Licence | Source |
|---|---|---|---|
| **SPT Base Types** | 3.9.0 | MIT — © Beckhoff Automation LLC | [SPT-Libraries](https://github.com/Beckhoff-USA-Community/SPT-Libraries) · [docs](https://beckhoff-usa-community.github.io/SPT-Libraries/) |
| **SPT Components** | 3.9.1 | MIT — © Beckhoff Automation LLC | same |
| **SPT Event Logger** | 3.9.0 | MIT — © Beckhoff Automation LLC | same |
| **SPT Motion Control** | 3.9.0 | MIT — © Beckhoff Automation LLC | same |
| **SPT Utilities** | 3.9.0 | MIT — © Beckhoff Automation LLC | same |
| `Tc2_Standard`, `Tc2_System`, `Tc3_EventLogger`, `Tc3_Module`, `Tc3_PackML_V2` | ships with TwinCAT | Beckhoff's own terms | Included in the TwinCAT 3 installation; not downloadable as single files |

The SPT libraries are **not** in this repository. They are installed by cloning the SPT-Libraries
repository and pointing TwinCAT's Library Repository at its `Library Repository` folder — see
[01 · Setup](_docs/01-setup.md).

## PLC libraries — `SIM_1`, the twin device layer

| Library | Licence | Source |
|---|---|---|
| **OC_Core**, **OC_EtherCAT** | BSD 3-Clause | [OC_TwinCAT_Core](https://github.com/OpenCommissioning/OC_TwinCAT_Core) |
| `Tc2_Math`, `Tc2_Standard`, `Tc2_System`, `Tc2_Utilities`, `Tc3_Module` | ships with TwinCAT | Included in the TwinCAT 3 installation |

`SIM_1`'s generated code is written by **OC Assistant**
([OC_Assistant](https://github.com/OpenCommissioning/OC_Assistant)), which is a tool this project
uses, not a component it redistributes.

## HMI packages — `TwinCAT_1/HMI`

Restored by NuGet from Beckhoff's feed into the git-ignored `TwinCAT_1/Packages/`. The list and the
pinned versions are in [`TwinCAT_1/HMI/packages.config`](TwinCAT_1/HMI/packages.config), which is
the authority; this is a summary of it.

| Package | Version | Terms |
|---|---|---|
| `Beckhoff.TwinCAT.HMI.BaseTemplate` | 14.5.1 | Beckhoff's own — see the `Legal/` folder inside each restored package |
| `Beckhoff.TwinCAT.HMI.Controls` | 14.7.1 | same |
| `Beckhoff.TwinCAT.HMI.EcDiagnostics` | 23.0.275 | same |
| `Beckhoff.TwinCAT.HMI.EcDiagnosticsControl` | 14.5.1 | same |
| `Beckhoff.TwinCAT.HMI.EventLogger` | 23.0.421 | same |
| `Beckhoff.TwinCAT.HMI.Framework` | 14.5.1 | same |
| `Beckhoff.TwinCAT.HMI.Functions` | 14.5.1 | same |
| `Beckhoff.TwinCAT.HMI.Industries.Common` | 14.5.1 | same |
| `Beckhoff.TwinCAT.HMI.Motion` | 14.5.1 | same |
| `Beckhoff.TwinCAT.HMI.PackML` | 14.4.5 | same |
| `Beckhoff.TwinCAT.HMI.Server.Engineering` | 23.0.421 | same |
| `Microsoft.TypeScript.MSBuild` | 7.0.0 | Apache-2.0 — © Microsoft Corporation |

## Documents

| | Author | Terms |
|---|---|---|
| `_data/SPT Framework.pdf` — *SPT Framework for TwinCAT 3: A Practical Guide*, Articles 1–7, 2025 | Emad Eddin Abdelghany | Published for free distribution. Kept as background reading only — its API surface does not match this project and **must not be copied**; see [the SPT framework guideline](_docs/reference/spt-framework.md) |

## The machine, the twin, and the rest of the project

The Unity twin, the CAD model every shape derives from, and the Unity packages are in the **main
repository** and are covered by its own notices, not by this file:
[THIRD-PARTY-NOTICES.md](https://github.com/Preliy/DT_PSA_OPCV/blob/master/THIRD-PARTY-NOTICES.md).

## Corrections

If an attribution here is wrong, incomplete, or names your work under the wrong licence, please
[open an issue](https://github.com/Preliy/DT_PSA_OPCV_Beckhoff/issues) — it will be fixed promptly.
