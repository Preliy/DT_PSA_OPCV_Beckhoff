# Process-image symbols that are not linked, on purpose

Hand-written. The I/O reconciliation reads the first column of the table below and
treats those symbols as accounted for, reporting them as **by design** rather than as
open work.

Everything else in the process image that has no terminal channel is a gap. A signal
with no link compiles, runs, and does nothing — no compiler and no runtime will
mention it. That is the whole reason this file is narrow: an entry here silences a
real check, so it needs a reason someone can verify, not a reason someone assumed.

**Before adding a row, establish the reason from the project** — a declaration
comment, a registration call, an HMI binding — and cite it. If the only argument is
"it has never been linked", that is an open gap, not an exception.

| Symbol | Why it is not linked | Owner |
|---|---|---|
| `MAIN.ControlSource_HMI_Web.MainPMLControl_Simplified.StartPressed` | Written by the panel over ADS, not by a terminal. `FB_ControlSource_HMI`'s declaration header states it: *"The HMI binds straight to this block's inherited structs - there is no translation layer."* The block is registered by `MAIN.Initialize` via `Machine.RegisterExternalController(THIS^)`. | HMI |
| `MAIN.ControlSource_HMI_Web.MainPMLControl_Simplified.StopPressed` | Same block, same mechanism. | HMI |
| `MAIN.ControlSource_HMI_Web.MainPMLControl_Simplified.ResetPressed` | Same block, same mechanism. | HMI |

## Polarity: the two emergency stops are normally closed, on both sides

Not a linking exception — both `SS_EStop1.HardwareInput` and `SS_EStop2.HardwareInput` are
linked like any other input. This is a **sense** note, recorded here because it is
invisible in the process image and dangerous to discover late.

**A real emergency stop is wired normally closed and reads TRUE while healthy.** Getting that
the other way round has the worst failure mode available: a cut cable would read as "no
emergency stop". So the NC sense is the one the control program is written against, and the
twin was made to match it rather than the other way round.

**The twin inverts, so `PLC_1` does not branch on whether it is driven by the twin.** The
twin's `OC.Interactions.Button` sets `_link.Status.SetBit(0, value)` from `_pressed`, so
`bValue` is TRUE while the mushroom is pressed — the opposite of the hardware. `SIM_1`'s
`FG_System.Mapping` carries the `NOT` that fixes it:

```iecst
GVL_EtherCAT_1_SIM.FG_System_Panel_EL1809_1.bIn9	:= NOT SS_EStop1.bValue;
GVL_EtherCAT_1_SIM.FG_System_Panel_EL1809_1.bIn10	:= NOT SS_EStop2.bValue;
```

`PLC_1` then reads NC in both worlds. `FB_IlluminatedButton.Active` is
`HardwareInput XOR _Inverted`, and `FG_System.Initialize` sets the polarity once:

```iecst
SS_EStop1.Inverted := TRUE;   // NC contact - TRUE while healthy
SS_EStop2.Inverted := TRUE;
```

`FG_System.EmergencyStopActive` is unchanged: it is written against `Active`, which is still
TRUE while a mushroom is latched.

> **The two edits are one change.** Dropping the `NOT` in `SIM_1` without clearing
> `Inverted` in `PLC_1`, or the reverse, gives a machine that is emergency-stopped whenever
> nobody is pressing anything — or, far worse, one that never reports an emergency stop at all.

### Two ordering traps, both closed in code

Neither is obvious from reading the assignment, and both turn an inverted input back into a
spurious or a missed emergency stop.

**The polarity is set in `Initialize` step 0, with the registrations — not in step 10 with the
other parameters.** `Machine.EnforceSafety` reads `FG_System.EmergencyStopActive` through a
property getter that does not care whether `FG_System` has finished initialising. Every scan the
polarity is still FALSE is a scan on which a healthy mushroom reads as latched and the machine
aborts. Step 0 leaves no such scan.

**`FB_IlluminatedButton.Initialize` seeds `HMI.DeviceConfig.Inverted` from `_Inverted`.**
`HMICommunication` runs `_Inverted := HMI.DeviceConfig.Inverted` whenever HMI control is
available, and `CyclicLogic` publishes the other direction only *after* `SUPER^.CyclicLogic()`
has already called it — so on the first executing scan the mirror is still the struct's zero
default. Without the seed, selecting Manual could silently revert the polarity to FALSE.

**With no process image, both mushrooms report active.** SIM_1 not running, EtherCAT down or a
cut cable all leave the bits at 0, which under NC means latched. That is the fail-safe
direction and it is intended — a machine that will not leave `Aborted` right after startup is
usually the twin not being connected yet, not a fault in `FG_System`.

## Not exceptions

Recorded here so nobody adds them to the table by mistake.

- **`MAIN.Machine.FG_02._CameraEnable`, `._LightEnable`, `._Trigger`, `._ShotOk`** —
  open work, not exempt. FG_02's module exists and declares its I/O, but no `FG_02*`
  terminal exists on either master yet, so there is nothing to allocate against.
  The I/O tooling can propose the terminals to add. Once they exist, these four link
  like any others.
