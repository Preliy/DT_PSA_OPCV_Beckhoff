---
name: building-hmi-elements
description: Use when building or changing TwinCAT HMI (TE2000) content for this machine - device tiles, machine control pages, PackML panels, user controls, navigation, symbol bindings against the SPT framework PLC, or publishing a PLC struct to the panel with TcHmiSymbol.AddSymbol. Derives page structure and device labels from the machine knowledge base.
allowed-tools: [Bash, Read, Edit]
---

# Building TwinCAT HMI elements on SPT

## Overview

The HMI project is `Beckhoff/TwinCAT_1/HMI` (TE2000, Framework 14.5.1). It binds over ADS to
**`PLC_1`**, the SPT control program, as runtime `PLC1`.

The framework does most of the work already. `FB_ComponentBase` and `FB_PackML_BaseModule` publish
HMI structs, compute permissives and decide who may command what. **An HMI element renders those
decisions; it does not make them.** Almost every mistake in this area is a panel trying to be clever.

**Read [reference.md](reference.md) before writing markup.** It holds the binding grammar, the PLC
struct contracts, the colour mechanics and the traps. Do not generate bindings from memory of the
Beckhoff docs — they disagree with the shipped libraries in places.

## The HMI DUT pattern

From SPT's own guidance (`SPT_Components/index.html`): an FB intended for HMI control gets a DUT
holding **Configuration variables, Commands, Status information**, plus a wrapper `_HMI` DUT
aggregating the three.

> The idea is to give all components/PackML modules the same basic capabilities. Component or
> Equipment Module-specific functions should be exposed through their own group of DUTs. This pattern
> makes the development of User Controls on the HMI side much smoother.

So every component already offers `ComponentBase_HMI` (Config/Command/Status, including `Reset` and
`HMIControlAvailable`), and every module offers `PackMLBaseModule_HMI`. A device-specific struct sits
alongside it — `SolenoidHMI`, `DigitalSensor_HMI`.

**Consequence for design: one user control per device *type*, parameterised by those structs.** Never
a hand-drawn widget per instance. Placing a device is two bindings; adding the 80th device changes no
control.

## Rules that keep panels correct

- **No PackML logic in the HMI.** `FB_ControlSource` computes `Start` / `Stop` / `Reset` permissives
  and owns the awkward transitions (`Reset` while `Aborted` sends `Clear`; `Start` while `Held` sends
  `Unhold`). Bind `data-tchmi-is-enabled` to a permissive; never re-derive one.
- **Mode decides who may command, and the PLC decides that too.** `HMIPermissions` sets
  `ComponentBase_HMI.Status.HMIControlAvailable` from the PackML mode. A jog button binds its
  `is-enabled` to that flag and needs no knowledge of modes.
- **Momentary command bits.** `data-tchmi-state-symbol` makes a button *be* the PLC bit. The PLC
  self-clears, so the HMI never has to. Reserve `onPressed` + `WriteToSymbol` for writing a *specific
  value* (an enum, a setpoint).
- **Bind to a published struct, not to POU internals.** The contract is the module's own
  `HMI : ST_HMI_<Owner>` struct, which travels with the module when it is refactored.
  `GVL_HMI` was the older, hand-mapped version of the same idea and is being retired — while
  both exist, the module writes `HMI` and mirrors it to the GVL. Device tiles bind straight to
  component structs (`SolenoidHMI`, `DigitalSensor_HMI`); that is what makes them scale.
- **Navigation mirrors the PLC hierarchy**: machine → functional group → device.

## Workflow

0. **Check the group has something to render.** `Beckhoff/_docs/context/fg-XX.md` answers both halves:
   its **PLC_1** section (on the Beckhoff page) says whether the module exists, is registered and publishes an HMI struct,
   and its **Components** and **Unity** sections give the devices, their types and what each one is
   *for* — the source for tile labels and page structure, with no Unity Editor needed.

   **An HMI page for a group with no module has nothing to bind to.** Its components publish no
   structs until `generating-plc-code` has run. Build the PLC side first.
1. **Know the contract.** Read the struct from the compiled type model, not from documentation.
   Ask the tool rather than grepping the `.tmc`:

   ```bash
   python Beckhoff/_private/tools/plc_io.py instance --all-symbols | grep FG_Transport.Index01
   ```

   The group page's **Components** table already gives each device's verified control PLC path,
   which is the prefix every binding on the tile hangs off.
2. **Publish, don't map.** See "How a symbol reaches the panel" below. Add the struct to the
   PLC with `{ attribute 'TcHmiSymbol.AddSymbol' }` and a one-line comment — *the comment
   becomes the label in the server's mapping list*. Rebuild and activate; the server writes
   its own entry. Do not hand-edit `TcHmiSrv.Config.default.json`.
3. **Build the element.** User control for anything appearing more than once; a page for layout.
4. **Register.** Every new file needs a `<Content Include="…">` entry in `HMI.hmiproj`, every
   `%l%` key needs an entry in **both** `en.localization` and `de.localization`, and every `%tr%` icon
   needs a `themedResources` entry in `Properties/tchmiconfig.json`.
5. **Verify** with the checks below before claiming anything works.

## How a symbol reaches the panel

**Every PLC symbol is already reachable.** `Server/ADS/ADS.Config.default.json` sets
`USE_WHITELISTING: false` on runtime `PLC1`, so the ADS extension exposes the whole 851
symbol table. Being in `SYMBOLS` was never what made a binding resolve.

What the mapping list *is* for is labelling, typing and access control — and
`{ attribute 'TcHmiSymbol.AddSymbol' }` fills it from the PLC:

```pascal
	// --- HMI ----------------------------------------------------------------
	// One struct for the whole tile. Filled by PublishHMI after the base has run.
	{ attribute 'TcHmiSymbol.AddSymbol' }
	HMI	: ST_HMI_TransferIndex;
```

On activation the server writes its own entry, and the **declaration comment becomes the
`comment` field** — the label a designer sees:

```json
"ADS.PLC1.MAIN.Machine.FG_Transport.Index01.HMI": {
  "MAPPING": "PLC1::MAIN::Machine::FG_Transport::Index01::HMI",
  "SCHEMA": { "allOf": [ { "$ref": "tchmi:server#/definitions/ADS-PLC1.ST_HMI_TransferIndex" },
                         { "addSymbol": true, "comment": "One struct for the whole tile..." } ] }
}
```

The attribute is declared once on the **type**, so `FB_TransferIndex` publishes all five of
its instances.

Three consequences:

- **Never hand-edit `TcHmiSrv.Config.default.json`.** The running server holds it in memory
  and writes it back, keeping only the entries it created. It has silently pruned a
  hand-written 165-symbol file down to the 16 it recognised. Stop the server before touching
  it at all, and prefer not to.
- **Prefer a small `ST_HMI_*` struct to a whole FUNCTION_BLOCK instance.** `SYMBOL_COMPLEXITY_LIMIT`
  is 100 and an SPT FB carries interfaces, pointers and method entries, so a large one can be
  refused. It is not a hard rule: `MAIN.ControlSource_HMI_Web : FB_ControlSource_HMI` is published
  this way and the server accepts it, which is what lets `StartPage` bind
  `ControlSource_HMI_Web::MainPMLControl_Standard::CurrentState` without a mirror struct. Publish an
  FB only when the block's own members *are* the contract, as `FB_ControlSource`'s are; publish a
  struct whenever you would otherwise be exposing internals.
- **A published FB fills itself; a published struct does not.** `FB_ControlSource`'s base refreshes
  `MainPMLControl_*` every scan. A passive `ST_HMI_*` needs a `PublishHMI` action, and without one
  it reads zeros — `hmi_check.py` distinguishes the two cases and only flags the second.
- **Publishing is not filling.** Declaring the struct creates a live ADS symbol; something in
  the PLC still has to assign to it, normally a `PublishHMI` action called after
  `SUPER^.CyclicLogic()`. A published struct nobody writes reads zeros forever, and on a
  panel that looks exactly like an idle machine. `hmi_check.py` catches it.

## Verify before reporting

```bash
python Beckhoff/_private/tools/hmi_check.py          # add --from-snapshot if the PLC is mid-edit
```

That asserts all of it mechanically: markup and embedded JSON parse; every `%pp%` root is a
declared parameter; every `%ctrl%<id>::` resolves in the same file; **every `%s%` symbol
resolves in the compiled PLC type model, and any `::` member walk is anchored on a published
symbol**; every `%l%` / `%tr%` / `%i%` key exists; every file is registered in both
`HMI.hmiproj` and `tchmiconfig.json`; every user-control host passes every declared
parameter; and every published struct is actually written by the PLC.

When a name does not resolve it names the failing segment and the rewrite:

```
x Pages/FG_Transport.content: %s%ADS.PLC1....Index01.TransferIndex_HMI.Status.Ready%/s%
  - 'TransferIndex_HMI' is not a member of MAIN.Machine.FG_Transport.Index01 - the PLC
    calls it 'HMI'. Use %s%ADS.PLC1....Index01.HMI::Status::Ready%/s%
```

**A binding you cannot prove is a binding that fails silently** — `tchmiconfig.json` ships with
`binding.symbolError: "Ignore"`, so a typo renders a blank control and no error anywhere.

## Common mistakes

- **Guessing an HMI member name.** The library is inconsistent: `SolenoidHMI` has no underscore,
  `DigitalSensor_HMI` does. Read the `.tmc`.
- **Copying VFFS navigation JSON.** The Beckhoff reference uses `TcHmiNavigation` with
  `data-tchmi-navigation-structure` / `subItem` / `icon_n`. This project uses
  `TcHmiAccordionNavigation` with `data-tchmi-navigation-items` / `subItems` / `icon`. Different
  control, different keys.
- **Binding a colour to a string.** `Color` is an object; see `reference.md`.
- **Binding a state-machine control to a PLC enum.** Publish a `DINT` and bind that — the control's
  `State` and `UnitMode` are numeric enums.
- **Forgetting the `.hmiproj` entry.** The file exists on disk and is invisible to the build.
- **Adding an `%l%` key to `en` only.** The German locale then shows the raw key.
