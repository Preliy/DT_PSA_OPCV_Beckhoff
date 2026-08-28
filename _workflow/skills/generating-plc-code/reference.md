# Reference — SPT framework, OC device mapping, TcPOU mechanics

Grounding for `generating-plc-code`. Sourced from
<https://beckhoff-usa-community.github.io/SPT-Libraries/> and the `PackML_PLC_Example` (VFFS) demo.

**This project targets SPT V3.9** — the versions actually installed are `SPT Base Types 3.9.0`,
`SPT Components 3.9.1`, `SPT Event Logger 3.9.0`, plus `SPT Motion Control` and `SPT Utilities` which
`SPT Components` pulls in. They depend on **`Tc3_PackML_V2`**, not V3.

Most of the published documentation and the newest examples are the **V4** line. Every PackML enum
literal differs, so V4 material must be translated before use:

| | **V3.9 (this project)** | V4 (translate from) |
|---|---|---|
| State | `E_PMLState.ePMLState_Idle` | `E_PMLState.Idle` |
| Complete state | `E_PMLState.ePMLState_Complete` | `E_PMLState.Completed` |
| Command | `E_PMLCommand.ePMLCommand_Start` | `E_PMLCommand.Start` |
| Mode | `E_PMLUnitMode.ePMLUnitMode_Production` | `E_PMLUnitMode.Production` |
| Mode name fn | `F_UnitModeToString()` | `F_PMLUnitModeToString()` |
| PackML lib | `Tc3_PackML_V2` | `Tc3_PackML_V3` |

`E_PMLState` and `E_PMLCommand` come from `Tc3_PackML_V2`. **`E_PMLUnitMode` does not** — it is
defined in `SPT Base Types`. `Tc3_PackML_V2` has only `E_PMLProtectedUnitMode`.

Referencing `Tc3_PackML_V3` alongside SPT V3.9 loads two PackML libraries at once and makes every
`E_PML*` type resolve ambiguously — hundreds of errors from one wrong line in the `.plcproj`.

Module POUs in this project are named for their twin group without an `FB_` prefix (`Machine`,
`FG_01`, instantiated as `FG_01 : FG_01`). That is a deliberate deviation from the V3 VFFS
convention (`FB_Machine`, `FB_Unwind`): keeping the PLC name identical to the Unity name and the
twin's symbol path is the point of the pipeline. TwinCAT accepts an instance named after its type —
`SIM_1`'s generated `MAIN` already does exactly this.

## Read the installed library, not the documentation

The SPT docs are wrong in places, and the wrong places cost a full build cycle to find. Every
installed library ships an authoritative symbol tree. Read it first:

```
C:\ProgramData\Beckhoff\TwinCAT\PlcEngineering\Managed Libraries\<Company>\<Library>\<Version>\
    browsercache      plain XML - every FB with its exact methods and properties
    dependencies      which libraries it needs (this is how you learn V2 vs V3)
    <Library>.library a ZIP - see below, this is the best source
```

**Best source: the shipped ST itself.** A `.library` is a ZIP whose
`__shared_data_storage_string_table__.auxiliary` entry holds the library's **actual Structured Text**
— declarations, method bodies, comments. Search it for `FUNCTION_BLOCK <name>` or `TYPE <name>` and
you are reading exactly what the compiler sees. Records are length-prefixed and de-duplicated, so
strip control bytes (`re.sub(r'[\x00-\x08\x0b-\x1f\x7f-\x9f]','\n',s)`); identifiers are byte-exact
even though blank lines are not.

```bash
python -c "
import zipfile,re
z=zipfile.ZipFile(r'...\SPT Components\3.9.1\SPT_Components.library')
t=z.read([n for n in z.namelist() if 'string_table' in n][0]).decode('utf-8','ignore')
i=t.find('FUNCTION_BLOCK FB_SingleSolenoid')
print(re.sub(r'[\x00-\x08\x0b-\x1f\x7f-\x9f]','\n',t[i:i+2000]))"
```

This only works for source libraries. Beckhoff's own `Tc3_*` ship as `.compiled-library-ge33` with an
encrypted string table — for those, fall back to `browsercache` plus the vendor documentation.

Use it to **verify every enum literal before generating**, with word boundaries — a plain substring
test passes `ePMLState_Complete` against `ePMLState_Completing` and hides a real error.

```bash
python -c "
import xml.etree.ElementTree as ET
r=ET.parse(r'C:\ProgramData\Beckhoff\TwinCAT\PlcEngineering\Managed Libraries\Beckhoff Automation LLC\SPT Components\3.9.1\browsercache').getroot()
def dump(n,d=0,on=False):
    for c in n.findall('Node'):
        hit = on or (d==0 and 'Solenoid' in (c.get('Name') or ''))
        if hit: print('  '*d + c.get('Name'))
        dump(c,d+1,hit)
dump(r)"
```

`browsercache` lists methods, properties and their Get/Set accessors. It does **not** list plain
`VAR` members, so a component's `AT %I*` hardware variable will not appear there — check the docs for
those. Where the two disagree on a name, **the library wins**.

### The collision `browsercache` cannot show you

Because it omits `VAR` members, **a name clash with a protected backing variable in the base chain is
invisible to it**. `FB_BaseFB` declares `_Busy`, `_Error`, `_ErrorID`; `FB_ComponentBase` adds
`_Name` and `_Simulate`. Declaring your own `_Busy : BOOL` in a descendant compiles nowhere and fails
with

```
C0097  Duplicate definition of variable '_Busy' in function block 'FB_X' and in base 'FB_BaseFB'
```

Worse, the clash is usually **two-sided**: `Busy` is also a *property* on `FB_BaseFB`, so a
`_Busy`/`Busy` pair produces two errors and fixing only the one the compiler named leaves the other.

Screen for it before generating, by intersecting your declarations against every `_`-prefixed token
in the shipped library ST (over-approximate on purpose — a false positive costs a rename, a miss
costs a build):

```bash
python -c "
import zipfile,re,glob
tok=set()
for p in glob.glob(r'C:\ProgramData\Beckhoff\TwinCAT\PlcEngineering\Managed Libraries\Beckhoff Automation LLC\**\*.library',recursive=True):
    z=zipfile.ZipFile(p); n=[x for x in z.namelist() if 'string_table' in x]
    if n: tok |= set(re.findall(r'\b_[A-Za-z]\w*', z.read(n[0]).decode('utf-8','ignore')))
mine={'_Busy','_Ready','_Starved'}   # your VAR names
print('collides:', sorted(mine & tok))"
```

Prefer a domain word over a framework word anyway. A transport station holding a pallet is
`Occupied`; SPT's `Busy` means the block is mid async operation. Two different ideas that should
never have shared a name.

## Style guide

From `Getting_Started/DesignGuide.html`. **No Hungarian notation** — this is explicit in the guide
and enforced by their static analysis. The OC twin project uses `bExtend` / `nControl`; SPT does not.
Do not carry twin naming into `PLC_1`.

- PascalCase for everything. Whole words, not acronyms: `PositiveOvertravelSwitch_Left`, not `LPotSw`.
- Datatype prefixes only: `FB_`, `F_`, `I_`, `ST_`, `E_`, `U_`, `T_`.
- Instance prefixes only for pointers (`p`) and interfaces (`ip`).
- A local backing a property takes an underscore: `_Extended : BOOL` backs `PROPERTY Extended`.
- **Methods are verbs** (what it does), **properties are nouns** (what it is or has).

## Module anatomy

Both the machine module and every equipment module extend `FB_PackML_BaseModule`. Hierarchy comes
from **where an instance is declared**, not from any configuration.

**Body is always empty.** "No code should be written in the body of function blocks extending
FB_CyclicFB."

`CyclicLogic` — mandatory opening, every module, no exceptions:

```
IF NOT _InitComplete THEN
    _InitComplete := Initialize();
    RETURN;
END_IF

SUPER^.CyclicLogic();
```

`Initialize` — a `CASE` ladder. Registration happens at step 0, `SUPER^.Initialize()` second to last:

```
METHOD PROTECTED Initialize : BOOL;

Initialize := FALSE;

CASE DescendantSequenceState OF
    0:
        RegisterSubmodule(FG_01);        // submodules
        RegisterComponent(Y_Gripper);    // components
        _LogModeChanges  := FALSE;
        _LogStateChanges := TRUE;
        DescendantSequenceState := DescendantSequenceState + 10;

    10:
        // parameters, custom modes, recipes
        DescendantSequenceState := DescendantSequenceState + 10;

    20:
        IF SUPER^.Initialize() THEN
            DescendantSequenceState := DescendantSequenceState + 10;
        END_IF

    30:
        Initialize := TRUE;
END_CASE
```

Note the real spellings: **`RegisterSubmodule`** (lowercase `m`), `RegisterComponent`,
`RegisterExternalController`. The class diagram in the docs misspells all three.

Modules take their name through the declaration initialiser, verbatim from the VFFS demo:

```
FG_01 : FG_01 := (Name := 'FG_01', LogStateChanges := TRUE);
```

Components take theirs through the `Name` property in `Initialize` — `FB_ComponentBase` does not
document an `FB_init` taking a name.

## States

**Two indexers. Never confuse them.**

| Variable | Where | Reset |
|---|---|---|
| `SequenceState` | inside state methods (`Execute`, `Resetting`, …) | automatic on state change |
| `DescendantSequenceState` | inside `Initialize` **only** | manual — `SequenceState` is reserved by the base `Initialize` |

| Waiting (need a command to leave) | Acting (self-complete) |
|---|---|
| Stopped, Idle, Suspended, Aborted, Held, Complete | Clearing, Starting, Stopping, Aborting, Holding, Unholding, Suspending, Unsuspending, Resetting, Completing, **Execute\*** |

The state is **`Complete`**, not `Completed` — the official function-block page says `Completed`, which
occurs zero times in the shipped 3.9.0 library. The enum literal is `E_PMLState.ePMLState_Complete`.

**\*`Execute` is the exception.** It is an acting state but does **not** use `StateComplete()`. It
leaves only on an explicit `Complete` command — `ChangeState(E_PMLCommand.Complete)`.

Standard acting-state shape:

```
METHOD PROTECTED Resetting

CASE _CurrentMode OF
    E_PMLUnitMode.Production:
        CASE SequenceState OF
            0:
                NoStateTasksToComplete := FALSE;
                SequenceState := SequenceState + 10;
            10:
                IF <condition> THEN
                    SequenceState := SequenceState + 10;
                END_IF
            20:
                StateTasksComplete := TRUE;
        END_CASE

    E_PMLUnitMode.Maintenance, E_PMLUnitMode.Manual:
        ;
END_CASE

SUPER^.Resetting();
```

`NoStateTasksToComplete := FALSE` at step 0 tells the sequencer there is work to do;
`StateTasksComplete := TRUE` at the end says it is finished. Both are re-initialised on state change,
so they need no management. `SUPER^.State()` goes **last** — it does the housekeeping.

Omitting `SUPER^.State()` detaches submodules from the parent's state machine. That is a deliberate
tool, not an oversight — the machine module uses it in `Execute` to sequence groups by hand.

Timers go after the `CASE`, gated on the step that uses them:

```
ClampSettleTimer(IN := (SequenceState = 20) AND Y_Gripper.Extended, PT := T#500MS);
```

## Layering

> Only Components talk to Hardware. An Equipment Module should not talk directly to hardware.
> A module communicates only with one layer above and only with one layer below.

Error propagation goes Component → EM → Machine, re-contextualised at each level.
`ParentResponseDefinitions` maps a severity to a reaction:

```
ParentResponseDefinitions[TcEventSeverity.Warning]  := E_AlarmResponse.Suspend_Immediate;
ParentResponseDefinitions[TcEventSeverity.Error]    := E_AlarmResponse.Abort_ImmediateError;
```

**On this project, components declare their own `%I*` / `%Q*`.** `FB_DigitalSensor` carries
`HardwareInput AT %I*`, `FB_SingleSolenoidFeedback` carries `_ExtendOutput AT %Q*`, and they are
linked at the component instance. There is no `GVL_IO_<FG>` — the SPT documentation describes a
reference-passing alternative (`REFERENCE TO` through a setter, or `ADR()` into a `POINTER TO`,
set during `Initialize`), which keeps a component portable but is not what this machine does.

Consequence when allocating channels: a sensor consumes a real terminal channel that appears in
no GVL anywhere, so counting only the signals visible in the module under-counts the group. See
`mapping-plc-io`.

Architecture and the official build order are in
[`Beckhoff/_docs/reference/spt-framework.md`](../../../_docs/reference/spt-framework.md). This file
stays the authority on API surface.

## Registration — silent failure modes

All four fail at runtime with **no compile error**, which is what makes them expensive:

| Forgotten | Symptom |
|---|---|
| `RegisterSubmodule` for an EM | its state methods are never called; the module silently does nothing |
| `RegisterComponent` for a component | its `CyclicLogic()` is never called by the framework |
| the `InitComplete` guard | the state machine activates before children are ready |
| `Name` | alarms and traces carry an empty identity — you cannot tell which of four identical cylinders faulted |

Register a child in the same edit that declares it.

## Component-level HMI and alarms

Verified against `SPT Base Types 3.9.0`.

`FB_ComponentBase` gives every component four overridable methods beyond `Initialize` / `CyclicLogic`:
`HMICommunication`, `Monitoring`, `CreateEvents`, plus `RaiseAlarm` / `RaiseAlarmWithStrings` /
`RaiseEventWithStrings`. Each override calls `SUPER^` first.

**One HMI command per scan.** The base publishes `HMICommandActive_Base`; a descendant that adds its
own commands must publish `HMICommandActive_Descendant` so the base can interlock them. Gate on
`ComponentBase_HMI.Status.HMIControlAvailable`, which `HMIPermissions()` derives from the PackML mode
— never re-derive the permissive in the component or on the panel.

```
METHOD PROTECTED HMICommunication
SUPER^.HMICommunication();

HMICommandActive_Descendant :=
    ComponentBase_HMI.Status.HMIControlAvailable
    AND (<my command bits>);
```

`RaiseAlarmWithStrings` prepends the component's `Name` automatically — which is *why* `Name` must be
set in `Initialize`, and why the same alarm definition reused across four identical cylinders still
reports which one raised it. `RaiseEventWithStrings` logs without setting the `Error` bit.

`Monitoring()` runs every scan and is where fault conditions raise and clear. It runs from
`SUPER^.CyclicLogic()` — which is the concrete reason a child's `CyclicLogic()` must never be called
conditionally: skip it and that component stops monitoring, so an active alarm is never cleared.

Aggregation upward is automatic: `ComponentMonitor` and `SubModuleMonitor` on
`FB_PackML_BaseModule` collect children's alarm state into the module's own.

## Device mapping: twin → control

`oc.deviceType` is the **Unity component type**. It determines the OC_Core FB on the twin side, which
determines the signals, which determines the SPT component on the control side.

| `oc.deviceType` | OC_Core FB | Twin members | SPT component | Count |
|---|---|---|---|---|
| `Cylinder` | `FB_Cylinder` | `bRetract`, `bExtend` in; `bRetracted`, `bExtended` out | `FB_SingleSolenoidFeedback` / `FB_DoubleSolenoidFeedback` | 35 |
| `SensorBinary`, `SignalBinary` | `FB_SensorBinary` | `bValue` out | `FB_DigitalSensor` | 28 |
| `Button` | `FB_Button` | `bEnable` in; `bValue` out | `FB_ControlSource` input | 8 |
| `Lock` | `FB_Lock` | `bLock` in; `bClosed`, `bLocked` out | self-contained component | 6 |
| `Lamp` | `FB_Lamp` | `bEnable` in | direct output | 4 |
| `DriveSimple`, `DriveSpeed`, `DrivePosition` | `FB_Drive` | `nControl`, `fTargetValue` in; `nStatus`, `fActualValue` out | self-contained — **not** an NC axis, do not use `FB_Component_BasicAxis` | 4 |
| `TagReader` | `FB_Reader` | `nControl`, `nCommand` in; `nStatus`, `nResult` out | self-contained | 2 |
| `LinkByte` | `FB_DeviceByte` | `nControl`, `nControlData` in; `nStatus`, `nStatusData` out | direct output | 2 |
| `PanelSampler` | `FB_Panel` | `nControlData`, `nStatusData` DWORD | `FB_ControlSource` | 2 |
| `SwitchRotary` | `FB_Switch` | one-hot status bits | `FB_ControlSource` input | |

Choosing the cylinder component: **one output → Single, two outputs → Double.** Read the twin's
existing `Mapping` action, which shows exactly which coils the machine actually has. `Y_Gripper` is
commanded only to extend (spring return) and so is `FB_SingleSolenoidFeedback` despite having two
limit switches.

`I_Solenoid` API, verified against `SPT Components 3.9.1`:

| Member | Kind | Access |
|---|---|---|
| `Extend()`, `Retract()` | method | |
| `Extended`, `Retracted` | property | R |
| **`ExtendOutput`**, `RetractOutput` | property | R |
| `ExtendTime`, `RetractTime` | property | RW, **LREAL** milliseconds — write `2000.0`, not `2000` |
| `ExtendedInput`, `RetractedInput` | property | **W only**, on the `*Feedback` variants |
| `Reset()` | method | from `FB_ComponentBase` |

⚠️ **The V3.9 docs are wrong: they call it `ExtendedOutput`. The library defines `ExtendOutput`.**
`RetractOutput` is spelled as documented. `ExtendedInput` / `RetractedInput` keep the `-ed`.

The `*Feedback` variants raise a timeout alarm when the actual state disagrees with the command for
longer than the configured time — which is the whole reason to wire both limit switches even where
the twin's legacy byte map only carried one.

`FB_DigitalSensor` carries its own `HardwareInput AT %I* : BOOL` and is linked to a terminal channel
directly — it does **not** take its input through a GVL, and there is no writable input property.
Properties: `Active` (R), `Inverted`, `DebounceMode`, `DebounceTime`, `SimulationInput`,
`SimulationMode`, `SimulationTimeBase`, `TimeActive`, `TimeInactive`.

**Do not use `InSimulation` or `E_SensorSimulationMode`.** Those simulate inside the PLC. The twin is
the simulation and it drives the real process image.

## Operator control and HMI

**`FB_ControlSource` is concrete and already does the work.** Do not reimplement command dispatch.
Derive from it, register the instance with `Machine.RegisterExternalController(...)` in `MAIN.Initialize`,
and call its `CyclicLogic()` before the machine's. Its base `CyclicLogic`:

- copies `CurrentState` / `CurrentMode` off the module into `MainPMLControl_Standard`;
- recomputes `MainPMLControl_Simplified.{Reset,Start,Stop}Permissive` from the PackML state model —
  `Reset` ⇔ Complete/Stopped/Aborted, `Start` ⇔ Idle/Held, `Stop` ⇔ anything but
  Stopped/Clearing/Aborted/Aborting/Undefined. Publish these so the HMI greys buttons out instead of
  duplicating the rules;
- dispatches, including the two rules people get wrong: **Reset while Aborted sends `Clear`**, and
  **Start while Held sends `Unhold`**.

**Dispatch through `ipModule.ChangeState()` / `.ChangeMode()`, not through
`MainPMLControl_Standard.StateCommand`.** The base edge-detects on `StateCommandLast <> StateCommand`,
so the same command twice in a row is silently dropped unless you also reset `StateCommandLast`.
`ipModule` is a plain `VAR` on the base — `VAR` is public in CODESYS, so a derived block reaches it.

Guard the whole thing with the inherited `Registered` property: before registration `ipModule` is
null and the base `CyclicLogic` would dereference it.

`ST_PackML_Control_Simplified.{Reset,Start,Stop}Pressed` are declared `AT %I*` — they are for a
physical button panel, not an HMI. An HMI drives the module through your derived block instead.

### Binding a TwinCAT HMI

With `Beckhoff.TwinCAT.HMI.PackML` installed, `TcHmiStateMachineV2` binds to three PackTags symbols —
its `Description.json` names them explicitly:

| Control property | PackTags origin | Type | Mode |
|---|---|---|---|
| `StateCurrent` | `ST_PMLs > StateCurrent` | DINT | OneWay |
| `UnitModeCurrent` | `ST_PMLs > UnitModeCurrent` | DINT | OneWay |
| `Command` | `ST_PMLc > CntrlCmd` | DINT | TwoWay |

`E_PMLState` and `E_PMLUnitMode` are enums over DINT, so `TO_DINT()` publishes them directly. Expose
these in a GVL rather than letting the HMI bind into POU internals, so the panel survives refactoring.
Convert a numeric command by comparing against `TO_DINT(E_PMLCommand.ePMLCommand_x)` rather than
hard-coded numbers.

### Manual mode costs almost no code

The base `HMIPermissions` already maps mode to permission — `ePMLUnitMode_Manual` →
`AllowHMIControl(ThisModuleOnly := FALSE)`, which sets `ComponentBase_HMI.Status.HMIControlAvailable`
on every registered component. **Every SPT component then honours its own HMI struct**; for cylinders,
`FB_SingleSolenoid.HMICommunication` runs:

```
IF ComponentBase_HMI.Status.HMIControlAvailable THEN
	IF SolenoidHMI.Command.Extend THEN
		Extend();
	ELSIF SolenoidHMI.Command.Retract THEN
		Retract();
```

So the panel binds straight to the component symbol and no PLC code is written at all:

```
MAIN.Machine.<GROUP>.<DEVICE>.SolenoidHMI.Command.Extend / .Command.Retract
MAIN.Machine.<GROUP>.<DEVICE>.SolenoidHMI.Status.Extended / .Retracted / .Extending / .Retracting
```

The member is `SolenoidHMI` (type `ST_Cylinder_HMI` = `Config` / `Command` / `Status`). Only devices
with **no** SPT component — a bare coil such as a laser fire bit — need a hand-written manual path in
the module, gated on `_CurrentMode` being Manual or Maintenance.

**Do not relax a safety permissive in Manual mode.** Extract it as a property used by both the
production sequence and the manual path so the two cannot drift.

## Twin bit layouts

Needed when writing the `SIM_1` `Mapping` action. Bit access on a `BYTE` member is valid ST
(`P_Reader.nControl.0`).

| FB | Control (PLC → twin) | Status (twin → PLC) |
|---|---|---|
| `FB_Cylinder` | `bRetract`, `bExtend` | `bRetracted`, `bExtended` |
| `FB_SensorBinary` | — | `bValue` |
| `FB_Drive` | `nControl.0` forward, `nControl.1` backward, `fTargetValue` | `nStatus.6` active, `nStatus.7` valid, `fActualValue` |
| `FB_Reader` | `nControl`, `nCommand` (ULINT) | `nStatus`, `nResult` (ULINT) |
| `FB_DeviceByte` | `nControl`, `nControlData` | `nStatus`, `nStatusData` |
| `FB_Lock` | `bLock`, `nControlData` | `bClosed`, `bLocked`, `nStatusData` |
| `FB_Panel` | `nControlData` (DWORD) | `nStatusData` (DWORD) |

## TcPOU XML mechanics

The part that silently breaks generated code.

```xml
<?xml version="1.0" encoding="utf-8"?>
<TcPlcObject Version="1.1.0.1" ProductVersion="3.1.4026.18">
  <POU Name="FG_01" Id="{...}" SpecialFunc="None">
    <Declaration><![CDATA[FUNCTION_BLOCK FG_01 EXTENDS FB_PackML_BaseModule
VAR
END_VAR]]></Declaration>
    <Implementation><ST><![CDATA[]]></ST></Implementation>
    <Method Name="Initialize" Id="{...}">
      <Declaration><![CDATA[METHOD PROTECTED Initialize : BOOL;]]></Declaration>
      <Implementation><ST><![CDATA[...]]></ST></Implementation>
    </Method>
    <Action Name="ReadInputs" Id="{...}">
      <Implementation><ST><![CDATA[...]]></ST></Implementation>
    </Action>
    <Property Name="GatesClosed" Id="{...}">
      <Declaration><![CDATA[PROPERTY GatesClosed : BOOL]]></Declaration>
      <Get Name="Get" Id="{...}"><Declaration><![CDATA[VAR END_VAR]]></Declaration>
        <Implementation><ST><![CDATA[...]]></ST></Implementation></Get>
      <Set Name="Set" Id="{...}"><Declaration><![CDATA[VAR END_VAR]]></Declaration>
        <Implementation><ST><![CDATA[...]]></ST></Implementation></Set>
    </Property>
  </POU>
</TcPlcObject>
```

Rules:

- **Every `Id` is a fresh unique GUID.** `POU`, `Method`, `Action`, `Property`, `Get`, `Set` each need
  their own. A duplicate makes TwinCAT drop or merge objects without a clear error.
- All code lives in `<![CDATA[...]]>`.
- `<Action>` has no `<Declaration>`.
- GVLs use `<TcPlcObject><GVL Name="..." Id="{...}"><Declaration><![CDATA[...]]></Declaration></GVL>`.
- Files are UTF-8; the existing project files carry a BOM.
- **Register in the `.plcproj`** — `<Compile Include="path"><SubType>Code</SubType></Compile>` plus a
  `<Folder Include="dir" />` for each new directory. Unregistered files are invisible to TwinCAT.

## Doc defects to code around

- **`I_Solenoid.ExtendedOutput` does not exist — it is `ExtendOutput`.** Documented wrong on the
  `V3.9` branch and on the live docs site. Confirmed against the shipped 3.9.1 library and by the
  compiler (`C0004 'ExtendedOutput' is no component of 'FB_DoubleSolenoidFeedback'`).
- `I_DigitalInput` exposes **`IsActive`**, not `On`. The `CylinderDualOutputWithFeedback` example
  page uses `.On` and is wrong.
- `FB_SolenoidBankBase.AddSolenoid()` takes `I_Cylinder` while the interface section defines
  `I_Solenoid`.
- The V4 class diagram lists `Completed()`; the V3 one lists `Complete()`.
- `RegsterExernalController()` in the class diagram is a typo for `RegisterExternalController()`.

## Worked example — FG_01

Context: `Function` says barcode identify plus laser mark, both abstract. `Process` gives the cycle.
`Safety` gives the laser permissive. `Interfaces` gives the Index01 handshake. `SequenceUnit1.cs`
confirms ordering and timings.

Five nodes pass the symbol test:

| Device | `oc.deviceType` | Component | DI | DO |
|---|---|---|---|---|
| `Y_Gripper` | `Cylinder` | `FB_SingleSolenoidFeedback` | 2 | 1 |
| `Y_Platform` | `Cylinder` | `FB_DoubleSolenoidFeedback` | 2 | 2 |
| `Y_ReaderWindow` | `Cylinder` | `FB_SingleSolenoidFeedback` | 2 | 1 |
| `P_Reader` | `TagReader` | `FB_DigitalSensor` + trigger output | 1 | 1 |
| `Y_LaserMark` | `LinkByte` | direct output | 0 | 1 |

`Y_Platform` moves the laser head in **service only** — its `Function` entry records that
SequenceUnit1 takes override control of it but never actuates it during the cycle. It is therefore
reachable in Manual and Maintenance modes and absent from `Execute`. Reading the device list without
the context would have put it in the cycle.

See `Beckhoff/TwinCAT_1/PLC/PLC_1/Modules/01 FG_01/FG_01.TcPOU` for the result.

### FG_01 I/O assignment

**Do not read a channel table from this file.** The live one is generated into
`Beckhoff/_docs/context/plc-io.md`, one table per terminal, and
`python Beckhoff/_private/tools/plc_io.py terminals` prints it on demand. A hand-copied table here
went stale within one iteration — it claimed `EL1809`/`EL2809` for a group that is actually
wired on `EL1008` ×2 + `EL2008`, against variables in a GVL that does not exist.

What is worth knowing structurally:

- Terminals go under `EtherCAT_1` for `PLC_1` and are mirrored under `EtherCAT_1_SIM` for
  `SIM_1`, with **identical names** — only the box id distinguishes them.
- FG_01 currently declares 21 process-image symbols (13 DI, 8 DO), all linked.
- Most are component-owned (`Y_Gripper.RetractedSensor`, `P_Reader.HardwareInput`); two are
  bare coils declared in the module (`_LaserFire`, `_ReaderTrigger`) and are the only two
  links on this project produced by a `TcLinkTo` pragma.

The tsproj `<Mappings>` section is **not** hand-authored — those links carry variable GUIDs
and image offsets that TwinCAT owns. Add the *terminals* in XAE; generate the *links* with
`python Beckhoff/_private/tools/plc_io.py write-mapping`, which emits `Mapping_PLC.xml` byte-exactly
for import on the Mappings node. See `mapping-plc-io`.
