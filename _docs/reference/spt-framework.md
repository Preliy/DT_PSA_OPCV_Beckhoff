# SPT framework — validated guideline

How the SPT application framework is meant to be used, and why it is shaped that way. Everything here
was checked against the libraries this project actually compiles against.

**This file is curated, not generated.** No tool writes it. `_docs/context/` is the opposite —
derived from the twin and rebuilt wholesale — so the never-hand-edit rule applies there, not here.

---

## Trust order

When two sources disagree about an identifier, believe them in this order:

1. **The installed library** — `TwinCAT_1/PLC/PLC_1/_Libraries/Beckhoff Automation LLC/SPT Base Types/3.9.0/SPT_Base_Types.library`
2. **Official Beckhoff docs** — <https://beckhoff-usa-community.github.io/SPT-Libraries/>
3. **This project's compiling code** — `TwinCAT_1/PLC/PLC_1/Modules/10 FG_Transport/` is the richest worked
   example (one EM with eleven submodules of three reusable types, plus a full recovery model);
   `TwinCAT_1/PLC/PLC_1/Modules/11 FG_01/FG_01.TcPOU` is the smaller one
4. **Third-party write-ups**, including the white paper in `_data/` — good for *rationale*, never for API

This order settles **identifiers**. For **behaviour** — sequences, handshakes, interlocks, recovery —
the PLC is master outright and [`transport-behaviour.md`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md) records it.

This is not pedantry, and there are two distinct hazards:

**Version drift.** The docs site and the newest examples document **V4**; this project runs the
**V3.9** line. Every PackML enum literal differs (`ePMLState_Idle` here vs. `E_PMLState.Idle` there),
and a few identifiers do too. **Check every identifier against the installed 3.9.0 library** before
reusing any published V4 material.

**Plain errors.** The Getting Started page writes `RegisterSubModule()`; the function-block reference
and the binary both say `RegisterSubmodule`. The class diagram has `RegsterExernalController()`. The
V3.9 docs call a solenoid property `ExtendedOutput` where the library defines `ExtendOutput` — caught
by the compiler, not by reading.

**The binary settles both.** Every identifier asserted below was found in the 3.9.0 library. Anything
unverified is marked as such rather than stated.

## What this project runs

| | |
|---|---|
| TwinCAT | 3.1.4026.25 — `TcVersion` in `TwinCAT_1/PLC/TwinCAT.tsproj` |
| SPT Base Types | 3.9.0 |
| SPT Components | 3.9.1 |
| SPT Event Logger / Motion Control / Utilities | 3.9.0 |
| PackML enum form | `E_PMLState.ePMLState_Execute`, `E_PMLCommand.ePMLCommand_Reset`, `E_PMLUnitMode.ePMLUnitMode_Production` |

**The libraries are not in this repository.** They come from
[Beckhoff-USA-Community/SPT-Libraries](https://github.com/Beckhoff-USA-Community/SPT-Libraries) —
MIT, © Beckhoff Automation LLC — installed by cloning that repository and adding its
`Library Repository` folder to TwinCAT's library repositories, which is also how you pin or move a
version. [01 · Setup](../01-setup.md) has it with the rest of the prerequisites.

## ⚠ The white paper in `_data/` is not ground truth

`_data/SPT Framework.pdf` — *SPT Framework for TwinCAT 3: A Practical Guide*, Articles 1–7 of a
planned 12, Emad Eddin Abdelghany, 2025, free distribution — explains the architecture well. Its API
surface does not match this project and **must not be copied**.

| The paper says | Verified reality | How it was checked |
|---|---|---|
| `M_Resetting()`, `M_Execute()`, `M_Stopping()` … | `Resetting`, `Execute`, `Stopping` — **no prefix** | `M_Resetting` occurs **0** times in the 3.9.0 binary; official docs list the unprefixed names and write `SUPER^.Resetting`; `FG_01.TcPOU` compiles with `SUPER^.Resetting()`. The `M_` prefix belongs to the *inner* PackML FB (`StateMachine.M_StateComplete()`), not to SPT |
| `M_UnHolding()`, `M_UnSuspending()` | `Unholding`, `Unsuspending` | capitalisation differs too |
| `THIS^.StateComplete()` is how you signal completion | `StateComplete` exists but is `PROTECTED`; the application signals through the `NoStateTasksToComplete` / `StateTasksComplete` pair and the framework calls `StateComplete()` itself | official docs state the pair explicitly; the binary contains `StateTasksComplete := FALSE; … StateComplete();` |
| `Initialize := SUPER^.Initialize()` behind a boolean guard | a `CASE` ladder indexed by `DescendantSequenceState` | official docs describe both indexers; the paper mentions neither |
| "every component tracks its own internal `MainState`" | **`MainState` is not a framework member** — 0 occurrences. It is a variable the paper's own example declares | easy to mistake for something inherited |

The paper claims to document "V4", and this project is on the 3.9.x line — so some divergence would be
expected. **But the `M_` prefix is not a version difference.** The official docs site *is* the V4
reference, and it lists the state methods unprefixed and writes `SUPER^.Resetting`. So the prefix
appears in neither line, and is best read as the author's own convention. *(V4 library source was not
inspected directly; that one claim rests on the docs rather than on a binary.)*

Where the paper genuinely is describing V4 rather than erring, the V3.9 ⇄ V4 difference is what you
need — most visibly the enum literals.

What the paper *is* good for: the ISA-88 reasoning, the hierarchy decision rule, the command-flow and
completion-propagation model, and the registration failure modes. Nothing official contradicts any of
it, and it is explained better there than anywhere else. Articles 8–12 — Control Source, Alarms and
Events, Machine Code Progression, and the end-to-end example — are **not written**, so do not go
looking for them. Its three figures are images and are not reproduced here.

---

## The three levels

```
Machine Module (MM)          one per project, owns the PackML state machine
    Equipment Module (EM)    one functional section; "Submodule" in SPT terms
        Component            one device, or one logical concern
```

Each level has a fixed scope, and crossing it is the mistake that costs the most later:

| Level | Base class | Owns | Must not |
|---|---|---|---|
| Machine Module | `FB_PackML_BaseModule` | machine state, operator commands, coordination of EMs | know how any device works |
| Equipment Module | `FB_PackML_BaseModule` | what its components do in each state | touch `%I*` / `%Q*` directly |
| Component | `FB_ComponentBase` | one device: drive it, report status, raise its own alarms | know which PackML state the machine is in |

**Placing something.** Is it a physical device or a single logical concern → Component. Is it a group
of devices that always work together as one functional unit → Equipment Module containing those
components. Does it coordinate other units → the Machine Module, or a Submodule if genuinely
warranted. More than three levels is discouraged.

An EM is not always required: a component belonging to the *machine* rather than to a station — a
signal tower, say — registers directly with the Machine Module. In this project `FG_System`'s
`H_SignalTower` is exactly that case.

**A component must run standalone.** If it cannot be instantiated in a bare test program and driven
through its own public methods, it is too tightly coupled to this machine and will not survive into
the next one.

## Command flow and completion

Top-down, each level commanding **only its direct children**:

```
operator → Control Source → MM enters Resetting → MM.Resetting()
                                                    → EM.Resetting()   (via SUPER^)
                                                        → components commanded
```

Bottom-up, by aggregation:

```
components report done → EM sets StateTasksComplete → MM sees all EMs done
                                                    → PackML advances Resetting → Idle
```

**No level skips a level, in either direction.** The MM never reaches past its direct children; a
component never receives a command from the MM. Both directions work only because of registration.

## Registration

Two methods, both called from `Initialize()`. Verified spellings — note the lowercase `m`:

| Method | Registers | Interface |
|---|---|---|
| `RegisterSubmodule()` | a child Equipment Module | `I_PackML_BaseModule` |
| `RegisterComponent()` | a child Component | `I_ComponentBase` |
| `RegisterExternalController()` | an HMI / control-source bridge | `I_PackML_ExternalController` |

Inheriting the right base class satisfies the interface automatically — no casting. Registration is
what builds the internal arrays the framework iterates when propagating state calls, so:

| Forgotten | Symptom | Compile error? |
|---|---|---|
| `RegisterSubmodule` for an EM | its state methods are **never called**; it silently does nothing | no |
| `RegisterComponent` for a component | its `CyclicLogic()` is never called by the framework | no |
| the `InitComplete` guard | the state machine activates before components are ready | no |
| `Name` | alarms and traces carry an empty identity — you cannot tell which of four identical cylinders faulted | no |

None of these fail loudly. Register a child in the same edit that declares it.

## `Initialize()`

Runs before the state machine exists. Its job is **structure**, not behaviour: register children, name
them, link I/O, set fixed parameters. The framework calls it every scan until it returns `TRUE`.

**Two indexers, never interchangeable:**

| Variable | Use in | Reset |
|---|---|---|
| `SequenceState` | state methods (`Resetting`, `Execute`, …) | automatic on state change |
| `DescendantSequenceState` | `Initialize` **only** — `SequenceState` is reserved by the base `Initialize` | manual |

The shape this project uses, from [`FG_01.TcPOU`](../../TwinCAT_1/PLC/PLC_1/Modules/11%20FG_01/FG_01.TcPOU):

```
Initialize := FALSE;

CASE DescendantSequenceState OF
    0:  // Names first - they are used in every alarm this module raises.
        Y_Gripper.Name := 'Y_Gripper';
        RegisterComponent(Y_Gripper);
        _LogModeChanges  := FALSE;
        _LogStateChanges := TRUE;
        DescendantSequenceState := DescendantSequenceState + 10;

    10: // Parameters that never change at runtime
        Y_Gripper.ExtendTime := 2000.0;
        DescendantSequenceState := DescendantSequenceState + 10;

    20: IF SUPER^.Initialize() THEN
            DescendantSequenceState := DescendantSequenceState + 10;
        END_IF

    30: Initialize := TRUE;
END_CASE
```

**Never goes in `Initialize()`:** motion commands, conditional production logic, or anything that must
repeat after a fault and reset. `Initialize()` wires the structure; the state methods run the machine.

**I/O linking.** SPT documents a pattern in which a component takes its addresses from outside:
a group-level I/O GVL passed in during `Initialize()`, either as a `REFERENCE TO` through a setter
or `ADR()` into a `POINTER TO`. That keeps a component portable — point it at a different
reference and it works on a different machine.

**This project does not do that, and the shipped components do not either.** `FB_DigitalSensor`
declares `HardwareInput AT %I*` itself; `FB_SingleSolenoidFeedback` declares `_ExtendOutput AT
%Q*`. Each instance is linked to a terminal channel directly, and there is no `GVL_IO_<FG>`
anywhere in `PLC_1`. Only signals with no component that fits — bare coils like
`FG_01._LaserFire` — are declared in the module.

The consequence is worth carrying: a component consumes terminal channels that appear in no GVL,
so the group's channel count cannot be read off its module declaration. It is counted from the
compiled process image instead.

## `CyclicLogic()`

One call from `MAIN` drives the whole hierarchy. Every module's override opens with the init gate:

```
IF NOT _InitComplete THEN
    _InitComplete := Initialize();
    RETURN;
END_IF

SUPER^.CyclicLogic();
```

**The execution order is fixed** and holds at every level:

| Step | | Why |
|---|---|---|
| 1 | children's `CyclicLogic()` | so their status is current before anything reads it |
| 2 | your own logic | acts on up-to-date child status |
| 3 | `SUPER^.CyclicLogic()` | runs the state machine, calls the active state method |
| 4 | status derivation (components only) | `Busy` / `Error` reflect this scan |

Invert steps 1 and 3 and your state method evaluates **last scan's** child status — a one-scan lag
that is harmless until it isn't.

**Never call a child's `CyclicLogic()` conditionally.** Skipping it stops that component's alarm
monitoring and HMI processing and can stall its internal state machine. If something should not run
every scan, put the condition *inside* the method, not around the call.

The body of an FB extending `FB_CyclicFB` stays empty — all code lives in methods.

## State methods

Verified names on `FB_PackML_BaseModule`, **no `M_` prefix**:

`Aborted`, `Aborting`, `Clearing`, `Complete`, `Completing`, `Execute`, `Held`, `Holding`, `Idle`,
`Resetting`, `Starting`, `Stopped`, `Stopping`, `Suspended`, `Suspending`, `Undefined`, `Unholding`,
`Unsuspending`

> The official function-block page lists this state as **`Completed`**. That is the **V4** spelling;
> the V3.9 line this project runs uses `Complete`, and `Completed` occurs **0** times in the shipped
> binary. The enum differs the same way — `E_PMLState.ePMLState_Complete` here versus
> `E_PMLState.Completed` in V4. Consult the installed library before reusing anything from the docs
> site, which documents V4.

| Waiting — leave only on a command | Acting — self-complete |
|---|---|
| Stopped, Idle, Suspended, Aborted, Held, Complete | Clearing, Starting, Stopping, Aborting, Holding, Unholding, Suspending, Unsuspending, Resetting, Completing, **Execute\*** |

**\*`Execute` is the exception.** It is an acting state but does not self-complete; it leaves on an
explicit `Complete` command (`ChangeState(E_PMLCommand.ePMLCommand_Complete)`). For continuous
production it simply never completes.

The acting-state shape, from working code:

```
CASE SequenceState OF
    0:  NoStateTasksToComplete := FALSE;      // there is work to do
        SequenceState := SequenceState + 10;

    10: Y_ReaderWindow.Retract();
        IF Y_ReaderWindow.Retracted THEN
            SequenceState := SequenceState + 10;
        END_IF

    30: StateTasksComplete := TRUE;           // finished
END_CASE

SUPER^.Resetting();                            // housekeeping - always last
```

`NoStateTasksToComplete := FALSE` tells the sequencer there is work; `StateTasksComplete := TRUE` says
it is done. Both are re-initialised on state change, so neither needs managing. `SUPER^.State()` goes
**last** — it propagates to registered submodules and aggregates their completion.

Omitting `SUPER^.State()` detaches submodules from the parent's state machine. That is occasionally a
deliberate tool — the machine module uses it in `Execute` to sequence groups by hand — but never an
accident.

## Verified API inventory (SPT Base Types 3.9.0)

Everything below was extracted from the shipped library.

**Function blocks:** `FB_BaseFB`, `FB_CyclicFB`, `FB_ComponentBase`, `FB_PackML_BaseModule`,
`FB_ControlSource`, `FB_PackML_ModeLogger`, `FB_PackML_StateLogger`

**Interfaces:** `I_BaseFB`, `I_CyclicFB`, `I_ComponentBase`, `I_PackML_BaseModule`,
`I_PackML_Control`, `I_PackML_ExternalController`

**Properties:** `Busy`, `Control`, `CurrentAlarmSeverity`, `CurrentMode`, `CurrentState`,
`DisableSubModuleModeChange`, `Error`, `ErrorID`, `InSimulation`, `InitComplete`, `LogModeChanges`,
`LogStateChanges`, `ModeCommand`, `Name`, `ParentResponseDefinitions`, `Registered`, `StateCommand`,
`TracingAllowed`

**Structs / enums:** `ST_ComponentBase_HMI` (+ `_Command`, `_Config`, `_Status`),
`ST_PackMLBaseModule_HMI` (+ `_Command`, `_Config`, `_Status`), `ST_PackML_Control`,
`ST_PackML_Control_Simplified`, `E_AlarmResponse`, `E_PMLUnitMode`

**Methods beyond the state set:** `Initialize`, `CyclicLogic`, `StateComplete`, `RegisterSubmodule`,
`RegisterComponent`, `RegisterExternalController`, `CreateEvents`, `Monitoring`, `HMICommunication`,
`HMIPermissions`, `AllowHMIControl`, `BlockHMIControl`, `ComponentMonitor`, `SubModuleMonitor`,
`RaiseAlarm`, `RaiseAlarmWithStrings`, `RaiseEventWithStrings`, `ChangeState`, `ChangeMode`,
`StateChanged`, `ModeChanged`, `Reset`, `Complete`, `AbortImmediate`, `AbortImmediateError`,
`HoldControlled`, `HoldImmediate`, `StopControlled`, `StopImmediate`, `SuspendControlled`,
`SuspendImmediate`, `Trace`, `Marker`, `TraceWithJson`, `FB_init`

## Build order — the official progression

From Beckhoff's [Machine Code Progression](https://beckhoff-usa-community.github.io/SPT-Libraries/SPT%20Training/MachineCodeProgression.html).
This is the guidance the white paper lists as an unwritten article; it exists.

1. **Plan.** Agree the machine's operation and terminology with everyone involved *before* coding.
   Two questions to settle first: where are the possible mechanical collisions, and which alarms stop
   the whole machine versus only one Equipment Module?
2. **Build the Components.** Hardware control first, written to be reusable.
3. **Build the Modules.** Machine Module and Equipment Modules, where the state machine lives.

Then, within the modules, **code Auto mode last**:

```
Manual  →  Maintenance  →  Home  →  Pre-Production  →  Production (Auto)
```

Manual gives basic functionality; Maintenance adds the advanced and potentially damaging operations;
Home establishes known positions across every EM; Pre-Production prepares the machine; Production is
the automated sequence.

**This matters here.** Two groups are wired end to end — FG_Transport and FG_01 — and the other five
are still twin only; check the group's own page rather
than trusting this sentence to stay current. The twin's MIL sequences describe *only* the production
case, so working straight from them produces Production mode first — the exact inversion of this
guidance. Get a group homing and jogging under Manual and Maintenance before automating it.

FG_Transport learned the same lesson the expensive way, in a different register: its `Resetting` was
written last and got rewritten three times before it stopped deadlocking. The rules that came out of
it are in [`transport-behaviour.md`](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md) — read them before writing any state
method that waits on something.

## Related

- [The FG_Transport behaviour contract](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md)
  — the derived handshake, the transfer latch, the lift interlocks and the reset model, and the
  handshake any EM here has to honour. The PLC is master for behaviour, and that page is where it is
  written down.
- [The machine in TwinCAT](../context/machine.md) — the group index and how far each group has got.
