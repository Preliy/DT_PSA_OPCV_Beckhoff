# Usage — running the machine on TwinCAT

Operating the demo with the TwinCAT control program driving it.

For the twin's own controls — camera, selection, the tool strip, hot keys — see
[using the application](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/02-using-the-application.md). This page is only about the control side.

## 1. Startup order

The order matters: the twin's devices bind to PLC symbols on connect, so the runtime has to be there
first.

1. Open the TwinCAT solution and put the runtime into **Run** mode.
2. Open `Unity/Assets/Demo_1/Scenes/VC_Demo_1_Beckhoff_1.unity`.
3. Press **Play**.

If the twin comes up with devices that never move, the usual cause is the runtime not being in Run,
or the ADS route not resolving — see [01 · Setup](01-setup.md).

## 2. The operator panel

The Beckhoff scene adds an on-screen panel, `MAIN.FG_System.H_ControlPanel`. It is a `PanelSampler`
aggregating **eight buttons**, and they are PackML states rather than free-form commands:

| Button | |
|---|---|
| `START` | |
| `STOP` | |
| `RESET` | |
| `CLEAR` | |
| `ABORT` | |
| `PRODUCTION` | Mode |
| `MAINTANANCE` | Mode. Spelled this way in the twin — the misspelling is the actual symbol name |
| `MANUAL` | Mode |

The bit each button occupies is in the panel's generated `BitLayout` on
[FG_System in TwinCAT](../_docs/context/fg-system.md).

> The panel is **this vendor's**, not the machine's. The Siemens scene has a different one — seven
> controls including a rotary mode switch. That is why the panel is marked `†` on the main
> repository's pages.

## 3. The signal tower

`H_SignalTower` reports machine state by colour. The mapping is a machine-level contract, not a
TwinCAT detail — it is in
[the state-lamp table](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/state-lamp.md).

## 4. The web HMI

`Beckhoff/TwinCAT_1/HMI` is a TE2000 project bound to `PLC_1` as runtime `PLC1` on port 851. Its
pages:

| Page | Shows |
|---|---|
| `StartPage`, `GroupsOverview` | The machine and its groups |
| `FG_01` … `FG_05` | Per-group device tiles and controls |
| `FG_Transport`, `FGTransport_Index`, `FGTransport_Lift`, `FGTransport_Stopper`, `FGTransport_Drive` | The conveyor, and one page per module type |
| `EtherCAT` | Bus and terminal state |
| `Events` | The event log |
| `Settings`, `LoginPage` | — |

Every HMI binding is checked against the PLC's own symbols when this module is built, so a page
cannot quietly bind to a symbol that no longer exists.

## 5. Faults, recovery and what the machine will not do

The behaviour is a **machine-level contract**, so it is documented in the main repository, not here:

| Question | Read |
|---|---|
| How a station stops, resets and hands the pallet on | [Transport behaviour](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/transport-behaviour.md) |
| Why a group will not start without its Index unit | same — the step chain and its three invariants |
| What the FG_01 laser interlock does and does not enforce | [FG_01 behaviour](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/fg-01-behaviour.md) |
| Why a NOK verdict stops the pallet | [FG_02 behaviour](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/fg-02-behaviour.md), [FG_04 behaviour](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/fg-04-behaviour.md) |
| Resetting FG_03 or FG_05 with a part in the gripper | [Gripper station reset](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/gripper-station-reset.md) |
| The safety chain, and who owns which fact | [The safety chain](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/reference/fg-system-safety.md) |

Two things that surprise people, both documented in full at those links:

- **No functional group runs on its own.** Each is served by an Index unit in `FG_Transport` that
  fixes the pallet, triggers the group, and waits for it to report done before releasing.
- **Retracted holds the pallet; extending releases it.** Several authored descriptions in the twin
  say the opposite and are known to be wrong.

## 6. Which control path to use

The twin says `MAIN.FG_01.P_Camera`. **TwinCAT says `MAIN.Machine.FG_01.P_Camera`.** Only the second
works in a link or an HMI binding, and the first fails *silently* in both.

Never derive a control path by hand — the verified one for every device is on that group's page in
[the TwinCAT machine pages](../_docs/context/).
