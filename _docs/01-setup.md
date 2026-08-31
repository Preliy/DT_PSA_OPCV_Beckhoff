# Setup — TwinCAT

Installing the Beckhoff side and connecting it to the Unity twin.

**Do the [main setup](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/01-setup.md) first** — clone the repository and get the Unity
project opening. This page picks up from there.

> **This page describes a single PC** — Unity, the control PLC and the emulated bus all on one
> machine, which is how the project is developed and how everything here was verified. The one part
> that has *not* been exercised that way is running Unity on a separate host; it is written up in
> [§8](#running-unity-on-a-different-pc) and marked as unverified where it is.

## 1. What you need

This project runs **a real EtherCAT master and an emulated EtherCAT segment on the same PC**, and it
is meant to run them at industrial timing rather than best-effort. That makes the host requirements
stricter than an ordinary TwinCAT install, and the two that people get wrong are the **CPU cores**
(§3) and the **network adapters** (§4). Read both before buying or reconfiguring anything.

### The engineering PC

| | Needs | Why |
|---|---|---|
| **CPU** | x64, multi-core — enough cores that at least one can be handed to TwinCAT exclusively | An isolated core is what makes the real-time behaviour industrial instead of Windows-scheduled — [§3](#3-real-time-give-twincat-an-isolated-core) |
| **Network** | **two** Ethernet ports with a chipset the TwinCAT real-time driver supports, **patched to each other with a cable** | One port carries the real master, the other the emulated segment, and the frames travel between them over that wire — [§4](#4-two-network-adapters-and-the-loop-cable) |
| **OS** | Windows 10 or Windows 11, x64 | TwinCAT 3.1 requires it |
| **Rights** | Local administrator | The real-time driver and the core configuration are both machine-level changes |

**A laptop with one onboard NIC will not run this project as designed.** The second port has to be
real hardware TwinCAT can bind its real-time driver to — a PCIe card or a dual-port card, not a USB
dongle and not a virtual adapter. Which chipsets qualify is in [§4](#4-two-network-adapters-and-the-loop-cable).

### Software

| Component | Version | Notes |
|---|---|---|
| **TwinCAT 3** | `3.1.4026.25` | XAE (engineering) and XAR (runtime). The version the project was saved with; installed with the TwinCAT Package Manager — [§2](#2-installing-twincat-3) |
| **TwinCAT 3 EtherCAT Simulation (TE1111)** | — | Provides the **EtherCAT Simulation Device** that `EtherCAT_1_SIM` is. Part of the XAE installation; the instance it creates is licensed — [§2](#licences) |
| **TwinCAT HMI (TE2000)** | — | Only to build or edit the web HMI. Not needed to run the machine |
| **OC Assistant** | `v1.18.7` | Generates the `SIM_1` twin device layer from the twin's device tree — [releases](https://github.com/OpenCommissioning/OC_Assistant/releases). **Engineering only:** not needed to build or run the project as it stands — [§7](#oc-assistant-is-an-engineering-tool-not-a-build-step) |
| **The PLC libraries** | — | Neither PLC project compiles without them, and none of them are in this repository — [§5](#5-the-plc-libraries) |

## 2. Installing TwinCAT 3

**Build 4026 is installed with the TwinCAT Package Manager, not with a monolithic setup `.exe`.**
That is the change from 4024 and it catches people out: you install the Package Manager once, then
use it (or its `tcpkg` command line) to install the workloads you need.

1. Install the **TwinCAT Package Manager** — [initial installation](https://infosys.beckhoff.com/content/1033/tc3_installation/15698627211.html).
2. Install **both** the engineering and the runtime workloads —
   `TwinCAT.Standard.XAE` and `TwinCAT.Standard.XAR`. Engineering alone is not enough: this project
   runs the PLC, the EtherCAT master and the emulated segment on the same PC you develop on. See
   [installation with the TwinCAT Package Manager](https://infosys.beckhoff.com/content/1033/tc3_installation/15698617995.html).
3. Install **TE2000** only if you intend to edit the web HMI.
4. Reboot.

The Package Manager can also be driven from a shell, which is the reproducible way to see what is
available and what a machine already has: `tcpkg list -t workload` and `tcpkg list --installed`. The
command set is documented under
[working with the command line](https://infosys.beckhoff.com/content/1033/tc3_installation/15698626059.html).

The **EtherCAT Simulation Device** used by `EtherCAT_1_SIM` comes with the XAE engineering
installation — there is no separate download for it, only a licence for the instance
([§ Licences](#licences)).

**Install TwinCAT before doing anything in §3 or §4.** Both the core configuration dialog and the
real-time Ethernet driver installer ship *with* TwinCAT — they are not separate downloads.

### Licences

**You need your own Beckhoff licences, and getting them is between you and Beckhoff.** This project
ships no Beckhoff software and no licence for any: TwinCAT 3 XAE, the XAR runtime, TE1111 and TE2000
are Beckhoff products with their own terms. Trial licences are generated on your own engineering
system, in TwinCAT, by you.

Two that are easy to miss:

- **TE1111 is an instance-based licence.** The EtherCAT Simulation Device is included with TwinCAT
  3.1 XAE, and its runtime requires `TC1000`; a licence is ordered per instantiated simulation
  device. This project instantiates **one** — `EtherCAT_1_SIM`. See the
  [TE1111 product page](https://www.beckhoff.com/en-en/products/automation/twincat/texxxx-twincat-3-engineering/te1111.html).
- **A clone never receives a licence file.** `*.tclrs` is excluded by `TwinCAT_1/.gitignore`, so the
  `TrialLicense.tclrs` that sits in a maintainer's checkout is not distributed and is not yours to
  reuse — the one your machine runs on is the one you generate in TwinCAT on that machine.

Everything this project builds against, and who owns it, is in
[THIRD-PARTY-NOTICES.md](../THIRD-PARTY-NOTICES.md).

### Activating a trial licence

TwinCAT 3 **test licences run for 7 days, can be re-activated as often as you like, and need no
internet connection** — they are generated on the engineering system itself. That is the normal way
to bring a fresh machine up on this project.

1. Open the solution in XAE.
2. If you are licensing a remote runtime rather than this PC, pick it in **Choose Target System**
   first.
3. Go to **SYSTEM → License**, and open the **Manage Licenses** tab.
4. Tick **Add License** for each licence the project needs.
5. Click the **7-Day Trial License…** button.
6. Type the security code shown in the dialog, exactly as displayed, and confirm.
7. The **Order Information** tab now shows each licence with its expiry date.

When the seven days run out, repeat from step 5 — nothing else changes and the project is unaffected.

The procedure and its limits are Beckhoff's:
[TwinCAT 3 test licenses](https://infosys.beckhoff.com/content/1033/tc3_licensing/921947147.html),
[activating standard licenses manually](https://infosys.beckhoff.com/content/1033/tc3_licensing/2338480267.html),
and [TwinCAT 3 licensing](https://www.beckhoff.com/en-us/products/automation/twincat/twincat-3-licensing/)
for what is chargeable and what is not.

**A quicker route to the same list:** activate the configuration once with no licences. TwinCAT
refuses to start the runtime and names the licence it is missing — repeat until it starts. That is
slower to read about than to do, and it produces the exact list your machine needs rather than a
list copied from someone else's.

## 3. Real-time: give TwinCAT an isolated core

**This is the step that decides whether the twin behaves like a machine or like a program.** On a
default installation TwinCAT shares every core with Windows: the real-time portion of each shared
core is capped between 10% and 90%, and Windows' scheduler, power management and drivers are all
still on it. That is fine for a demo and visibly not fine for a bus running at 1 ms.

An **isolated core** is taken away from Windows entirely — the guest operating system no longer knows
it exists — and is available to the TwinCAT real-time exclusively. This is what
[TwinCAT 3 core management](https://infosys.beckhoff.com/content/1033/tc3_system/5211863691.html)
calls the distinction between *Windows cores* and *isolated cores*, and it is the single largest
lever on jitter.

### The procedure

Core isolation is a **target-system** setting, not a project setting. It is applied to the machine
and it needs a restart; it is not carried by this repository and cloning the project does not
configure it.

1. Open the solution (or any TwinCAT project) and go to **SYSTEM → Real-Time → Settings**.
2. Click **Read from Target** to see what the machine currently has.
3. Click **Set on Target** and choose the split — how many cores stay with Windows, and how many
   become isolated.
4. **Restart the PC.** The setting only takes effect after a reboot.
5. **Read from Target** again to confirm it took, then assign the tasks to the isolated core.

A reasonable starting split: leave Windows enough cores to stay responsive and isolate one. On a
4-core-or-more machine, isolating one core costs Windows very little and gives the runtime a core
nobody else can touch.

### What this project ships

The solution's real-time settings are recorded in `TwinCAT_1/PLC/TwinCAT.tsproj`, and they describe
**the machine it was saved on**:

| Setting | Value | Reading |
|---|---|---|
| `MaxCpus` | `20` | 20 logical CPUs on that host |
| `NonWinCpus` | `1` | **one** core isolated from Windows |
| `Cpu CpuId` | `19` | the isolated core in use is CPU 19 |
| `CoreBoostActive` | `true` | TwinCAT Core Boost enabled |
| `PCoreAffinity` / `ECoreAffinity` | `255` / `1048320` | a hybrid Intel CPU: CPUs 0–7 are P-core threads, CPUs 8–19 are E-cores |

**These numbers are not a requirement and will not match your PC.** Read your own with *Read from
Target* and set your own; a different core count and a different `CpuId` are normal and change
nothing about the project.

**Core Boost matters on a hybrid CPU** — the 12th/13th-generation Intel parts with performance and
efficiency cores. It lets a fixed clock frequency be assigned to each real-time core instead of
leaving it to the CPU's automatic selection, which is what stops an isolated core from being
downclocked out from under a 1 ms task. It is switched on the same way — *Read from Target* to see
whether the CPU supports it, *Set on Target* to activate, then a restart — after which a **Core
Frequency** column appears in the real-time table. Beckhoff's warning is worth repeating: you are
responsible for not asking for a frequency the machine will thermally throttle away from, because
that shows up as a cycle timeout. See
[TwinCAT Core Boost](https://infosys.beckhoff.com/content/1033/tc3_system/5206499979.html).

### The timing this project asks for

Two PLC tasks and the simulation device, as saved in the `tsproj`:

| | Cycle | Priority |
|---|---|---|
| `PlcTask_PLC` — the control program `PLC_1` | **10 ms** | 20 |
| `PlcTask_SIM` — the twin device layer `SIM_1` | **1 ms** | 4 |
| `EtherCAT_1_SIM` — the simulation device | **1 ms** | — |

The emulation running ten times faster than the program under test is deliberate, and it is the rule
TE1111 states: the EtherCAT Simulation Device runs **unsynchronised** with the master, so the
simulation has to be sampled faster than the control system it is answering — see
[TE1111 basic principles](https://infosys.beckhoff.com/content/1033/te1111_ethercat_simulation/6880082827.html).
A simulation task starved by Windows is exactly the failure this section exists to prevent.

## 4. Two network adapters and the loop cable

### Why two

`PLC_1` drives a **real EtherCAT master**, `EtherCAT_1`, with the cell's real terminal
configuration behind it — EK1100 couplers, EL1809 inputs, EL2809 outputs. `SIM_1` sits behind an
**EtherCAT Simulation Device**, `EtherCAT_1_SIM`, which answers as those terminals.

The master does not know it is talking to a simulation. It does what a master does: it puts EtherCAT
frames **on the wire** and waits for them to come back. So the two ends have to be joined by a wire.

```
   PLC_1 ──► EtherCAT_1      NIC A ──┐
                                     │  Ethernet patch cable
   SIM_1 ──► EtherCAT_1_SIM  NIC B ──┘
```

**Both ports are on the same PC and the cable loops from one to the other.** That is a supported
TE1111 configuration: the simulation can run on a separate computer as an HIL rig, or *"on the same
computer, as long as sufficient free network interfaces are available"*
([TE1111 basic principles](https://infosys.beckhoff.com/content/1033/te1111_ethercat_simulation/6880082827.html)).
This project takes the second option, so one PC runs the whole cell.

An ordinary Ethernet patch cable is all that is needed — EtherCAT is 100BASE-TX full duplex and no
crossover cable is required. Windows will show both adapters as an unidentified network with no
gateway. That is correct and should be left alone.

### The adapters have to be ones TwinCAT can drive

**A NIC is usable here only if the TwinCAT real-time driver supports its chipset.** The real-time
driver bypasses the Windows network stack to reach the chip directly, and it only knows the
controllers it ships `.inf` files for — in practice **Intel**. Beckhoff's
[supported network controllers](https://infosys.beckhoff.com/content/1033/tc3_overview/9309844363.html)
lists them by driver family:

| Driver | Covers |
|---|---|
| `TcI2xx.inf` | I350, I210 / I211, I219, I225 / I226, I220, I221, the 8256x/8257x series |
| `TcI8254x.inf` | The older Intel Gigabit line — 8254x, 8257x, I217, I218 |
| `TcI8255x.inf` | Intel PRO/100 and ICH-integrated controllers |
| `TcIXgbe.inf` | Intel 10 GbE — X540, X550 |

Realtek onboard ports, USB adapters and virtual adapters are **not** on that list. Beckhoff's own
caveat is worth carrying over: supporting a network card is not the same as the system being
real-time capable — the card is a precondition, not a guarantee.

The `TC_1 (TwinCAT-Intel PCI Ethernet Adapter (Gigabit))` string recorded against `EtherCAT_1` in
this project's `tsproj` is the name the real-time driver gives an adapter once it is installed on it.
Seeing that name in the adapter list is how you know the driver took.

### Installing the real-time driver

The installer ships with TwinCAT and needs administrator rights.

1. In XAE: **TwinCAT → Show Real Time Ethernet Compatible Devices…**, or run
   `TcRteInstall.exe` directly. On 3.1.4026 it is at
   `C:\Program Files (x86)\Beckhoff\TwinCAT\3.1\System\TcRteInstall.exe`; on 4024 and earlier,
   `C:\TwinCAT\3.1\System\TcRteInstall.exe` — see
   [TcRteInstall](https://infosys.beckhoff.com/content/1033/tc3_grundlagen/11328888459.html).
2. The dialog groups the machine's adapters. **Install the driver only on adapters under
   *Compatible devices*** — the *Incompatible devices* group is exactly what it says.
3. Select **both** ports you intend to use and click **Install**. Windows may warn about an unsigned
   driver; that warning can be ignored here.
4. Confirm both moved into **Installed and ready to use devices**.
5. On each of the two ports, **switch TCP/IP off DHCP** and give it a fixed address, or none at all.
   A DHCP client on a port that will never carry IP traffic just adds a startup delay — Beckhoff's
   [installation of the TwinCAT real-time driver](https://infosys.beckhoff.com/content/1033/ethercatsystem/1036996875.html)
   says the same.

### Pointing this project's devices at *your* adapters

**A fresh clone will not run until you do this.** The `tsproj` records the adapters of the machine it
was saved on, by hardware identity — `EtherCAT_1` on device `{5AF77408-…}`, MAC `98:B7:85:24:16:F3`,
and `EtherCAT_1_SIM` on device `{19D0D68E-…}`, MAC `98:B7:85:24:16:F2` (two ports of one dual-port
card, hence the consecutive addresses). Neither GUID exists on your PC.

Do this **before** Activate Configuration:

1. In the solution tree, select **I/O → Devices → `EtherCAT_1`**, open the **Adapter** tab, click
   **Search…** and pick the port that carries the master.
2. Select **`EtherCAT_1_SIM`**, open its **Adapter** tab, **Search…**, and pick the *other* port.
3. Check you have not picked the same port twice — the two entries must show different MAC
   addresses.
4. Make sure the cable is actually plugged in between them, and that both ports show link.

The **2nd Adapter** tab on the simulation device is for mixed operation of real and virtual slaves.
This project does not use it; leave it empty.

## 5. The PLC libraries

Neither PLC project compiles without these, and **none of them are in this repository** — TwinCAT
resolves them from your own library repository. There are three kinds and each is installed
differently.

| Library | Used by | Kind |
|---|---|---|
| **SPT Base Types** 3.9.0, **SPT Components** 3.9.1, **SPT Event Logger** 3.9.0 — plus **SPT Motion Control** and **SPT Utilities** 3.9.0, resolved with them | `PLC_1` | A **repository location** you add — [5.1](#51-the-spt-application-framework) |
| **OC_Core**, **OC_EtherCAT** | `SIM_1` | Library **files** you install — [5.2](#52-open-commissioning) |
| `Tc2_Standard`, `Tc2_System`, `Tc2_Math`, `Tc2_Utilities`, `Tc3_Module`, `Tc3_EventLogger`, `Tc3_PackML_V2` | both | **Nothing to do** — they arrive with TwinCAT 3 |

The version each project actually asks for is in its `.plcproj` as a `PlaceholderReference` with a
`*` resolution, so TwinCAT takes the newest matching version in the repository. The versions above
are what this project was verified against and are the ones recorded in
[THIRD-PARTY-NOTICES.md](../THIRD-PARTY-NOTICES.md).

### 5.1 The SPT Application Framework

The SPT libraries are distributed as a **git repository that doubles as a TwinCAT library
repository**. You point TwinCAT at the clone rather than installing files, which means `git pull`
updates the libraries.

1. Clone [Beckhoff-USA-Community/SPT-Libraries](https://github.com/Beckhoff-USA-Community/SPT-Libraries).
2. In XAE open the **Library Repository** — *PLC → Library Repository*, or right-click **References**
   in a PLC project.
3. Click **Edit Locations… → Add…**.
4. Browse to the clone and select the **`Library Repository` folder under the repository root** — not
   the repository root itself. Give the location a name, e.g. `SPT Libraries`.
5. The SPT libraries now appear in the repository list and resolve in `PLC_1`.

**This project runs the V3.9 line.** The published SPT documentation describes V4 and disagrees with
the shipped binary in several places — different enum literals, a few identifiers, and some outright
typos. Every identifier this project relies on was checked against the installed 3.9.0 library and
the differences are recorded in [the SPT framework guideline](reference/spt-framework.md).
**When a source disagrees with the shipped binary, the binary wins.**

### 5.2 Open Commissioning

`OC_Core` and `OC_EtherCAT` come from
[OpenCommissioning/OC_TwinCAT_Core](https://github.com/OpenCommissioning/OC_TwinCAT_Core) as library
files. Install them into the repository rather than adding a location:

1. Download the libraries from the repository's releases.
2. Open the **Library Repository** and click **Install**.
3. Select the library file. If it does not show, change the file filter to **All files** — the
   dialog defaults to `*.library` and will hide a `*.compiled-library`.
4. Install `OC_Core` first, then `OC_EtherCAT`, then any library either of them lists as a
   dependency.

The mechanics of both dialogs are in Beckhoff's
[Library Repository](https://infosys.beckhoff.com/content/1033/tc3_plc_intro/4189333259.html) and
[library installation](https://infosys.beckhoff.com/content/1033/tc3_plc_intro/4218300427.html)
pages.

### 5.3 Checking they resolved

Open **`PLC_1` → References → Library Manager** and then the same for `SIM_1`. Every entry must show
a concrete resolved version. A placeholder that resolves to nothing is reported as an unresolved
reference and the build fails with it — that is the symptom of a missing repository location, not of
a broken project.

## 6. The solution

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
| `TwinCAT_1/PLC/OC_EtherCAT.ethml` | OC Assistant's terminal template map: per terminal type, the `ST_Beckhoff_*` declaration and `TcLinkTo` pragma it generates into the `SIM_1` GVL |
| `TwinCAT_1/HMI` | TE2000 panels, `HMI.hmiproj` |

## 7. Build and activate

1. Build `PLC_1`.
2. Build `SIM_1`.
3. Activate Configuration.
4. Put the runtime into **Run** mode.

If Activate fails on the I/O devices, the adapters are the first thing to check — see
[§4](#pointing-this-projects-devices-at-your-adapters).

**Activate Configuration also starts the HMI project**, because it is part of this solution — see
[§9](#9-the-web-hmi-optional).

### OC Assistant is an engineering tool, not a build step

**Building and running this project does not involve OC Assistant.** `SIM_1` is generated code that
is *committed*, so a clone has it already. Installing the tool to get the solution running is wasted
effort.

You need it in exactly one case: **the machine changed in Unity and the emulation project has to be
regenerated** — a device added, removed, renamed or retyped. Then OC Assistant reads the twin's
device tree and rewrites the `{region generated code}` blocks in the `SIM_1` POUs.

That is also the reason for the standing rule: **never edit those blocks.** Only the `Mapping` action
in each POU is ours, and it is the part OC Assistant leaves alone.

## 8. Connecting the twin

Unity binds the twin's devices to `SIM_1` over ADS on **port 852**. Unity and TwinCAT on the same
machine is the simple case.

### Check the port on the Unity client

**Get this wrong and Unity connects to nothing, or to the wrong runtime, and no data is exchanged.**
The target is on the `TcAdsClient` component in the Unity scene:

| Field | This project |
|---|---|
| `NetId` | **`Local`** — Unity and TwinCAT on the same PC. On separate machines this is the one field that changes, see [below](#running-unity-on-a-different-pc) |
| `Port` | **852** — `SIM_1`, the twin device layer. **Not** 851, which is `PLC_1` |

`Machine_1.prefab` ships `852`, so the Beckhoff scene is right out of the box. It is still worth
checking, for two reasons:

- **Open Commissioning's own default is 851**, so a client added by hand starts on the wrong port.
- **The Siemens scene overrides the prefab to 851**, because its control PLC answers there. The port
  is a per-scene fact, not a machine fact.

### Read the Unity console

The failure is invisible in the scene and explicit in the console. Three signatures, three causes:

| Console message | Means |
|---|---|
| `TcAdsClient failed to connect: Local:852. …` (error) | Nothing is answering. The runtime is not in **Run**, or there is no route |
| `Port:<n> is out of range [301...399], [851...899]` (error) | The value is not an ADS PLC runtime port at all |
| `MAIN.<group>.<device> can't be found in client!` (warning, one per device) | **Connected to the wrong runtime** — almost always 851, where `PLC_1` answers and does not carry the twin's symbols |

The third is the one to memorise: a client that *connected* plus a page of "can't be found" warnings
is a port mistake, not a missing symbol. Each of those warnings is logged against the offending
device, so clicking it in the console selects that object in the hierarchy.

### Running Unity on a different PC

**`NetId` is the only field in the client that changes.** `Local` means *this machine*; to reach
another one, put the **target's AmsNetId** there — the six-part identifier the TwinCAT router uses,
like `5.86.23.11.1.1`. It is **not** an IP address, and an IP address in that field will not work.

Read the target's AmsNetId off the TwinCAT PC: the system-tray icon → **About TwinCAT**, or the
**SYSTEM** node in XAE.

Two things have to be true besides the field:

- **An ADS route has to exist**, and ADS routes are **bidirectional** — configured on both machines.
  On the TwinCAT PC: tray icon → **Router → Edit Routes → Add Route**. Use **Broadcast Search** to
  find the Unity host, or type its hostname or IP. Enter the route name, the AmsNetId, the address
  and **TCP/IP** as the transport, and choose **Static** so the route survives a reboot. You will be
  asked for administrator credentials on the target once; they are stored in the route. Confirm an
  **`x` appears under *Connected*** — that column, not the absence of an error, is what says the
  route works.
- **The Unity PC needs an AMS router of its own.** The client is built on the `TwinCAT.Ads` .NET
  library, which routes everything through the local router, so a machine with no TwinCAT
  installation has nothing to route through. It also opens a second connection to the router's
  real-time port to track whether the runtime is in Run or Config; the same route serves both.

Firewalls in between must pass ADS on **TCP 48898**.

> **This path has not been exercised on this project.** Everything published here was run with Unity
> and TwinCAT on one PC. The mechanism above is standard ADS rather than anything specific to this
> machine — if you run it split across two hosts and something is missing, that correction is a
> welcome pull request.

Start the TwinCAT runtime **first**, then enter Play mode in Unity.

## 9. The web HMI (optional)

`Beckhoff/TwinCAT_1/HMI` is a TE2000 project bound to `PLC_1`. Its server config
(`Server/ADS/ADS.Config.default.json`) maps the runtime alias `PLC1` to `127.0.0.1.1.1`
**port 851**, so page bindings read `ADS.PLC1.MAIN.…`.

**The binding is by ADS port, not by project name.** Renaming the PLC project does not break it — and
"fixing" a binding by renaming it after the PLC project is a mistake.

### Opening it

**There is nothing separate to start.** The HMI is a project inside this solution, so
**Activate Configuration starts it with everything else** ([§7](#7-build-and-activate)).

1. In the solution tree, open **`TwinCAT_1/HMI` → `Desktop.view`**. That is the entry point of the
   HMI — the start page the rest of the pages are reached from.
2. With `Desktop.view` open in the Designer, click the **LiveView** button in the quick-access strip
   at the **top right of the designer surface** — the small **L**.
3. The page opens with live values from `PLC_1`. Run the machine and it follows.

**LiveView is the point.** It renders the current configuration against the running PLC *without
publishing to a server first*, so an edit in the Designer is visible immediately — no download step,
no deploy. Beckhoff's pages:
[the TwinCAT HMI LiveView](https://infosys.beckhoff.com/content/1033/te2000_tc3_hmi_engineering/2669751691.html)
and [the HMI Engineering interface](https://infosys.beckhoff.com/content/1033/te2000_tc3_hmi_engineering/3477161867.html),
which describes the quick-access buttons.

If the pages render but every value is blank, the PLC is not in **Run** — the HMI reaches it as ADS
runtime `PLC1` on port 851, and an HMI with no PLC behind it still draws.

## 10. The generated documentation (optional)

The [TwinCAT description of the machine](../_docs/context/machine.md) is generated and
**committed**, so you do not need TwinCAT — or any of the build tooling — to read it.

It is refreshed by the maintainers whenever the TwinCAT projects change. The type model it is
built from is committed as `_docs/context/.plc-image.json`, so every page here can be read — and
checked against the solution — with no TwinCAT installed.

## 11. Checking it worked

| Check | Expect |
|---|---|
| **TwinCAT → Show Real Time Ethernet Compatible Devices…** | Both ports under *Installed and ready to use devices* |
| **SYSTEM → Real-Time → Settings → Read from Target** | At least one isolated core, and the tasks assigned to it |
| `EtherCAT_1` and `EtherCAT_1_SIM` **Adapter** tabs | Two different MAC addresses, both showing link |
| Both PLC projects' **Library Manager** | Every reference resolved to a concrete version |
| **SYSTEM → License** | Every required licence present and not expired |
| Activate Configuration, runtime in Run | No I/O device errors; the EtherCAT slaves reach OP |
| The Unity scene's `TcAdsClient` | `NetId` `Local`, `Port` **852** |
| TwinCAT in Run, Unity in Play on `VC_Demo_1_Beckhoff_1` | Devices respond to the PLC; the on-screen panel drives the machine. **No `can't be found in client!` warnings in the console** |
| `Desktop.view` in LiveView | Pages render with live values, not blanks |
| The operator panel's Reset, then Start | The line runs the ring: pallets circulate and every station processes |

## Reference documentation

Beckhoff's own pages for everything asserted above.

| Topic | Page |
|---|---|
| Installing build 4026 | [TwinCAT Package Manager](https://infosys.beckhoff.com/content/1033/tc3_installation/15698617995.html) · [initial installation](https://infosys.beckhoff.com/content/1033/tc3_installation/15698627211.html) · [command line](https://infosys.beckhoff.com/content/1033/tc3_installation/15698626059.html) |
| Windows cores vs isolated cores | [Core Management](https://infosys.beckhoff.com/content/1033/tc3_system/5211863691.html) |
| Fixed clock per real-time core on hybrid CPUs | [TwinCAT Core Boost](https://infosys.beckhoff.com/content/1033/tc3_system/5206499979.html) |
| What the real-time system is and does | [TwinCAT real-time](https://infosys.beckhoff.com/content/1033/tc3_grundlagen/6828869003.html) |
| Which NIC chipsets the RT driver supports | [Supported network controllers](https://infosys.beckhoff.com/content/1033/tc3_overview/9309844363.html) |
| Installing the RT driver on an adapter | [TcRteInstall](https://infosys.beckhoff.com/content/1033/tc3_grundlagen/11328888459.html) · [installation of the TwinCAT real-time driver](https://infosys.beckhoff.com/content/1033/ethercatsystem/1036996875.html) |
| The EtherCAT Simulation Device | [TE1111 basic principles](https://infosys.beckhoff.com/content/1033/te1111_ethercat_simulation/6880082827.html) · [user interface reference](https://infosys.beckhoff.com/content/1033/te1111_ethercat_simulation/6850067595.html) · [manual (PDF)](https://download.beckhoff.com/download/document/automation/twincat3/TE1111_TC3_EtherCAT_Simulation_en.pdf) · [product page](https://www.beckhoff.com/en-en/products/automation/twincat/texxxx-twincat-3-engineering/te1111.html) |
| Installing PLC libraries | [Library Repository](https://infosys.beckhoff.com/content/1033/tc3_plc_intro/4189333259.html) · [library installation](https://infosys.beckhoff.com/content/1033/tc3_plc_intro/4218300427.html) · [add library](https://infosys.beckhoff.com/content/1033/tc3_plc_intro/4189425291.html) |
| ADS routes between machines | [adding routes](https://infosys.beckhoff.com/content/1033/tc3_system/5211773067.html) · [Add Route dialog](https://infosys.beckhoff.com/content/1033/tcsystemmanager/1085351691.html) |
| Licences and the 7-day trial | [TwinCAT 3 test licenses](https://infosys.beckhoff.com/content/1033/tc3_licensing/921947147.html) · [activating standard licenses manually](https://infosys.beckhoff.com/content/1033/tc3_licensing/2338480267.html) · [TwinCAT 3 licensing](https://www.beckhoff.com/en-us/products/automation/twincat/twincat-3-licensing/) |
| The HMI designer and LiveView | [the TwinCAT HMI LiveView](https://infosys.beckhoff.com/content/1033/te2000_tc3_hmi_engineering/2669751691.html) · [HMI Engineering interface](https://infosys.beckhoff.com/content/1033/te2000_tc3_hmi_engineering/3477161867.html) |
