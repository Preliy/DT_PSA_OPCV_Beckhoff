# Reference — TwinCAT HMI against the SPT PLC

Project: `Beckhoff/TwinCAT_1/HMI`. Framework 14.5.1, Controls 14.7.1, PackML 14.4.5,
BaseTemplate 14.5.1. PLC runtime `PLC1` → `PLC_1` (SPT 3.9.x, `Tc3_PackML_V2`).

## Read the contract from the compiled type model

`PLC_1.tmc` is the authority on struct names, namespaces and members — it is what the PLC actually
exports. Documentation is not.

```bash
python -c "
import re
t=open(r'Beckhoff/TwinCAT_1/PLC/PLC_1/PLC_1.tmc',encoding='utf-8',errors='ignore').read()
m=re.search(r'<DataType><Name Namespace=\"([^\"]+)\"[^>]*>ST_Cylinder_HMI</Name>(.*?)</DataType>',t,re.S)
print('namespace',m.group(1))
print(re.findall(r'<SubItem><Name>(\w+)</Name><Type[^>]*>(\w+)</Type>',m.group(2)))"
```

Namespaces, confirmed this way:

| Type | Namespace |
|---|---|
| `ST_Cylinder_HMI`, `ST_DigitalSensor_HMI` | `SPT_Components` |
| `ST_ComponentBase_HMI` | `SPT_PackMLBase` |

(The library's *source* refers to itself as `SPT_BaseTypes` and the Beckhoff VFFS demo used
`SPT_PackMLBase` — only the `.tmc` decides.)

## PLC-side HMI structs

| FB | Member | Type |
|---|---|---|
| `FB_ComponentBase` (base of all components) | `ComponentBase_HMI` | `ST_ComponentBase_HMI` |
| `FB_SingleSolenoid` / `FB_*SolenoidFeedback` | **`SolenoidHMI`** — no underscore | `ST_Cylinder_HMI` |
| `FB_DigitalSensor` | **`DigitalSensor_HMI`** — with underscore | `ST_DigitalSensor_HMI` |
| `FB_PackML_BaseModule` | `PackMLBaseModule_HMI` | `ST_PackMLBaseModule_HMI` |

```
ST_ComponentBase_HMI   Config  : Name : STRING
                       Command : SimulatedOperation, StandardOperation, Reset : BOOL
                       Status  : InSimulation, Busy, Error : BOOL; ErrorID : UDINT;
                                 HMIControlAvailable : BOOL

ST_Cylinder_HMI        Config  : ExtendTime, RetractTime : LREAL
                       Command : Extend, Retract : BOOL; ExtendTime, RetractTime : LREAL
                       Status  : Extended, Retracted, Extending, Retracting : BOOL

ST_DigitalSensor_HMI   Config  : DebounceMode, DebounceTime, Inverted,
                                 SimulationMode, SimulationTimebase
                       Command : (empty struct - a sensor takes no commands)
                       Status  : Active : BOOL; TimeActive, TimeInactive : LREAL
```

`FB_SingleSolenoid.HMICommunication` acts on its own struct, gated by the base flag:

```
IF ComponentBase_HMI.Status.HMIControlAvailable THEN
	IF SolenoidHMI.Command.Extend THEN
		Extend();
	ELSIF SolenoidHMI.Command.Retract THEN
		Retract();
```

So jogging a cylinder from the panel is **zero PLC code** — bind to the struct and let the module's
`HMIPermissions` open the gate in Manual/Maintenance mode.

## Bind the control source directly — there is no machine-level mirror

`FB_ControlSource` already publishes machine state and mode in the standard PackML types, so the
panel binds to the control-source instance. Adding a GVL mirror would only be a second copy to keep
in step, and would convert well-typed enums into anonymous integers.

| Bind | Symbol | Type |
|---|---|---|
| actual state | `MAIN.ControlSource_HMI_Web.MainPMLControl_Standard.CurrentState` | `E_PMLState` |
| actual mode | `…MainPMLControl_Standard.CurrentMode` | `E_PMLUnitMode` |
| state command (write) | `…MainPMLControl_Standard.StateCommand` | `E_PMLCommand` |
| mode command (write) | `…MainPMLControl_Standard.ModeCommand` | `E_PMLUnitMode` |
| button permissives | `…MainPMLControl_Simplified.{Reset,Start,Stop}Permissive` | `BOOL` |

A command button writes a **static enum value** to `StateCommand` on `onPressed`:

```json
{ "objectType": "WriteToSymbol", "active": true,
  "symbolExpression": "%s%ADS.PLC1.MAIN.ControlSource_HMI_Web.MainPMLControl_Standard.StateCommand%/s%",
  "value": { "objectType": "StaticValue",
             "valueType": "tchmi:server#/definitions/ADS-PLC1.Tc3_PackML_V2.E_PMLCommand",
             "value": 2 },
  "asyncWait": true }
```

`E_PMLCommand`: Undefined 0, Reset 1, Start 2, Stop 3, Hold 4, Unhold 5, Suspend 6, Unsuspend 7,
Abort 8, Clear 9, Complete 10.

⚠️ **The base edge-detects a command as `StateCommandLast <> StateCommand`**, so the same command
twice in a row is swallowed. `FB_ControlSource_HMI.ReleaseCommandLatch` clears both after the base
has acted, which makes every press count. Anything deriving from `FB_ControlSource` needs that, or
must accept the limitation.

`ST_PackML_Control_Simplified.{Reset,Start,Stop}Pressed` are `AT %I*` — hardware buttons, not
HMI-writable. Use `StateCommand` from a panel.

## Project GVL contract

`GVL_HMI` carries only what has no component and no PackML struct of its own — currently the FG_01
laser and reader manual commands. Devices and machine control both bind directly.

```
Machine.Control.CntrlCmd      DINT   PackTags ST_PMLc.CntrlCmd - TwoWay from TcHmiStateMachineV2
Machine.Control.UnitMode      DINT   1 Production | 2 Maintenance | 3 Manual
Machine.Command.<10 x BOOL>          Reset Start Stop Hold Unhold Suspend Unsuspend Abort Clear Complete
Machine.Command.Mode<3 x BOOL>       ModeProduction ModeMaintenance ModeManual
Machine.Status.StateCurrent   DINT   PackTags ST_PMLs.StateCurrent
Machine.Status.UnitModeCurrent DINT
Machine.Status.StateName / ModeName  STRING(31)
Machine.Status.{Reset,Start,Stop}Permissive  BOOL
FG01.Command.LaserFire / ReaderTrigger
FG01.Status.LaserPermissive / SequenceStep / ManualControlActive / ...
```

Every `Control.*` and `Command.*` is consumed and cleared by `FB_ControlSource_HMI` in the same scan.
The HMI sets a bit and never clears it.

## Binding grammar

| Form | Means |
|---|---|
| `%s%ADS.PLC1.MAIN.Machine.FG_Transport.HMI::Status::StateName%/s%` | server symbol: published anchor, then `::` members |
| `%pp%Cylinder::Status::Extended%/pp%` | user-control parameter, members below it |
| `%ctrl%Cyl_BusyLamp::BackgroundColor%/ctrl%` | another control's property |
| `%f%!%s%…%/s%%/f%` | expression (JS) |
| `%l%L_FG_01%/l%` / `%tr%TR_Icon_X_normal%/tr%` | localisation / themed resource |

**A server symbol is one name.** The framework says so — in
`Packages/Beckhoff.TwinCAT.HMI.Framework.14.5.1/runtimes/native1.12-tchmi/dist/API/SymbolExpression.d.ts`:

> `getName()` — *In case of an expression of type Server getName will also contain the path.*
> `getPath()` — *In case of an expression of type Server getPath will return null.*

That is precisely **why `::` works here**: the whole string is handed to the server as one
name, and the server resolves the member walk itself — which it can do for a symbol it has
mapped. So the canonical form is a published anchor followed by `::` members:

```
%s%ADS.PLC1.<AddSymbol'd struct>::<Member>::<Member>%/s%
```

Mapping one struct therefore reaches every field under it. You do **not** need an entry per
leaf. `MAIN.Machine.FG_Transport.HMI` is published once by the pragma; `HMI::Status::Starved`
and its twenty-five siblings all resolve from that single entry.

`::` is *also* the client-side separator (`dist/API/ObjectPath.js`) used in `%pp%`, `%ctrl%`,
`%i%` and `%ctx%`, where the value is already in the browser and is walked as a JS object.
Same punctuation, two different resolvers — which is why a device tile can take one struct
parameter and address `%pp%Unit::Status::StateName%/pp%` inside it.

> ⚠️ Two earlier versions of this entry were wrong, and both cost a page of blank controls
> because `binding.symbolError` is `"Ignore"`. It first read *"dots down to the mapping
> boundary, `::` below it"*, then over-corrected to *"`::` never appears in `%s%`"*. The
> settled rule is the one above, and `python Beckhoff/_private/tools/hmi_check.py` now resolves every
> `%s%` against the compiled type model rather than against anybody's rule of thumb.
>
> Still open: whether a **bare dotted** deep path resolves with whitelisting off. Several are
> in the project and appear to work. `hmi_check.py` reports them as a note with the anchored
> rewrite, not as an error, until somebody settles it on a live panel.

## Symbol mapping

**The PLC owns this list. Nothing here is written by hand or by a tool in this repo.**

`Server/ADS/ADS.Config.default.json` sets `USE_WHITELISTING: false` on runtime `PLC1`, so
every symbol at port 851 is already reachable. The mapping list in
`Server/TcHmiSrv/TcHmiSrv.Config.default.json` exists for labelling, typing and access
control, and `{ attribute 'TcHmiSymbol.AddSymbol' }` on the PLC declaration fills it:

```json
"ADS.PLC1.MAIN.Machine.FG_Transport.Index01.HMI": {
  "ACCESS": 3, "DOMAIN": "ADS", "DYNAMIC": true, "HIDDEN": false,
  "MAPPING": "PLC1::MAIN::Machine::FG_Transport::Index01::HMI",
  "SCHEMA": { "allOf": [
    { "$ref": "tchmi:server#/definitions/ADS-PLC1.ST_HMI_TransferIndex" },
    { "addSymbol": true,
      "comment": "One struct for the whole tile. Filled by PublishHMI after the base has run.",
      "propertyOrder": 65 } ] },
  "USEMAPPING": true
}
```

Note `"addSymbol": true` and `"comment"` — **the comment is the ST doc comment above the
declaration**. Writing a good one is how a symbol gets a readable label in the designer.

Project DUTs carry no namespace, so they are declared as `ADS-PLC1.<Type>`; library types
keep theirs (`ADS-PLC1.SPT_Components.ST_Cylinder_HMI`). `$ref` is
`tchmi:general#/definitions/{BOOL,DINT,LREAL,UDINT,String}` for primitives.

**Do not hand-edit `TcHmiSrv.Config.default.json`, and do not open the project in the
designer expecting it to survive.** The running server holds the file in memory and writes
it back, keeping only entries it created — it has silently reduced a hand-written
165-symbol file to the 16 it recognised. The generator that used to write it
(`hmi_symbols.py`) was removed for exactly this reason: it kept losing the argument.

The `DEFINITIONS.ADS` type schemas are likewise server-generated. If they go stale, stop the
server, delete the stale entries, restart and activate — do not fabricate them.

### Adding a symbol

1. Declare `HMI : ST_HMI_<Owner>;` with the pragma and a one-line comment, in the FB.
2. Write it — a `PublishHMI` action after `SUPER^.CyclicLogic()`.
3. Register any new `ST_HMI_*.TcDUT` in `PLC_1.plcproj`.
4. Rebuild and activate. The server writes its own entry.
5. `python Beckhoff/_private/tools/hmi_check.py`.

## User controls

`X.usercontrol` (markup, root `TcHmi.Controls.System.TcHmiUserControl`) plus `X.usercontrol.json`.
Required parameter fields: `name`, `displayName`, `visible`, `type`, `category`, `readOnly`,
`bindable`, `heritable`.

```json
{
  "name": "data-tchmi-cylinder", "propertyName": "Cylinder",
  "propertySetterName": "setCylinder", "propertyGetterName": "getCylinder",
  "displayName": "Cylinder", "visible": true,
  "type": "tchmi:server#/definitions/ADS-PLC1.SPT_Components.ST_Cylinder_HMI",
  "category": "PLC", "readOnly": false, "bindable": true, "heritable": true, "refTo": ""
}
```

Hosted with `TcHmi.Controls.System.TcHmiUserControlHost` +
`data-tchmi-target-user-control="UserControls/Cylinder.usercontrol"`, then one attribute per
parameter. Live examples: `UserControls/TransferIndex.usercontrol` and its three siblings, placed in
`Pages/FGTransport_Index.content`, `_Stopper`, `_Lift` and `_Drive`.

## Indicating state by colour

`tchmi:framework#/definitions/Color` is an **object**:

```json
{ "color": "rgba(10, 255, 0, 1)" }
```

`ConvertBooleanToEnum` returns a `String`, so it cannot drive `data-tchmi-background-color`. Use a
`TcHmiRectangle` with a trigger **keyed on the symbol value** (not on a control event) writing the
control's own property:

```json
[{ "event": "%pp%Component::Status::Busy%/pp%",
   "actions": [{ "objectType": "Condition", "active": true, "parts": [
     { "if": [{ "compare1": { "objectType": "Symbol", "valueType": "tchmi:general#/definitions/BOOL",
                              "symbolExpression": "%pp%Component::Status::Busy%/pp%" },
                "compare2": { "objectType": "StaticValue", "valueType": "tchmi:general#/definitions/BOOL",
                              "value": true },
                "compareOperator": "==", "logic": null }],
       "then": [{ "objectType": "WriteToSymbol", "active": true,
                  "symbolExpression": "%ctrl%Cyl_BusyLamp::BackgroundColor%/ctrl%",
                  "value": { "objectType": "StaticValue",
                             "valueType": "tchmi:framework#/definitions/Color",
                             "value": { "color": "rgba(10, 255, 0, 1)" } },
                  "asyncWait": true }] },
     { "else": [ /* same shape, grey */ ] }
   ], "asyncWait": true }] }]
```

Project palette: busy/active **green** `rgba(10, 255, 0, 1)`, error **red** `rgba(255, 6, 6, 1)`,
off **grey** `rgba(125, 125, 125, 1)`. Also give the control a static grey
`data-tchmi-background-color` so it renders grey before the first value arrives.

## PackML state machine control

`TcHmi.Controls.Beckhoff.TcHmiPackML.TcHmiStateMachineV2` — V2 matches `Tc3_PackML_V2`.

| Attribute | Bind to | Mode |
|---|---|---|
| `data-tchmi-state-current` | `Machine.Status.StateCurrent` | OneWay |
| `data-tchmi-unit-mode-current` | `Machine.Status.UnitModeCurrent` | OneWay |
| `data-tchmi-command` | `Machine.Control.CntrlCmd` | TwoWay — the control writes here |

Its enums are **numeric**: `State` Undefined 0, Clearing 1, Stopped 2, Starting 3, Idle 4,
Suspended 5, Execute 6, Stopping 7, Aborting 8, Aborted 9, Holding 10, Held 11, Unholding 12,
Suspending 13, Unsuspending 14, Resetting 15, Completing 16, Complete 17. `UnitMode` Invalid 0,
Production 1, Maintenance 2, Manual 3. `Command` stops at Clear 9, so the control cannot issue
`Complete`; a button covers that.

**Bind the PLC enum symbols directly.** The ADS extension generates a PLC enum as
`"type": "integer"` with an `options[]` list supplying labels for the designer only — the value on the
wire is the number. `E_PMLState` and `E_PMLUnitMode` are numbered identically to the control's own
enums, so `MainPMLControl_Standard.CurrentState` / `.CurrentMode` / `.StateCommand` bind straight in.
There is no need for a `DINT` mirror, and mirroring only creates a second copy to keep in step.

To render an enum as text, `TcHmi.Functions.Beckhoff.EnumToMemberName(ctx, symbol)` resolves the
member name from the generated schema.

## Navigation

`Desktop.view` → `Accordion_Navigation_Right`, a
`TcHmi.Controls.BaseTemplate.TcHmiAccordionNavigation` with `data-tchmi-navigation-items`.

Item schema: **`name` and `id` required**; optional `content`, `subItems` (nested list),
`accessRights`, `icon` / `iconActive` / `iconPressed`, `function`, icon size.

```json
{ "id": "FunctionalGroups", "name": "%l%L_FunctionalGroups%/l%",
  "icon": "%tr%TR_Icon_FunctionalGroups_normal%/tr%",
  "subItems": [ { "id": "FG_01", "name": "%l%L_FG_01%/l%",
                  "content": "Pages/FGTransport_Index.content" } ] }
```

⚠️ The Beckhoff VFFS reference HMI uses a **different** control — `TcHmiNavigation` with
`data-tchmi-navigation-structure`, `subItem` (singular) and `icon_n`/`icon_a`/`icon_p`. Its JSON does
not paste into this project.

Icons are themed resources in `Properties/tchmiconfig.json` → `symbols.themedResources`; every nav
icon in this project points at the same placeholder pair:

```json
"TR_Icon_FunctionalGroups_normal": {
  "type": "tchmi:framework#/definitions/Path",
  "description": "Normal Icon of page: Functional Groups",
  "values": { "Base": "Themes/Base/Images/Placeholder/placeholder_normal.svg",
              "Base-Dark": "Themes/Base-Dark/Images/Placeholder/placeholder_normal.svg" } }
```

## Standard controls used here

`TcHmiButton` (`data-tchmi-state-symbol`, `data-tchmi-is-enabled`, `data-tchmi-text`),
`TcHmiTextblock` (`data-tchmi-text`), `TcHmiNumericInput` (`data-tchmi-value`,
`data-tchmi-is-read-only`), `TcHmiCombobox` (`data-tchmi-srcdata`, `data-tchmi-selected-value`,
`onSelectionChanged` trigger), `TcHmiRectangle`, `TcHmiCheckbox` (`data-tchmi-state-symbol`).

Access rights use the same shape on a control (`data-tchmi-access-config`) and on a nav item
(`accessRights`):

```json
[ { "accessright": "operate", "group": "Operator", "permission": "Deny" } ]
```

## Traps

- `binding.symbolError: "Ignore"` in `tchmiconfig.json` — bad bindings fail **silently**. Set it
  stricter while commissioning.
- A struct-typed user-control parameter needs its type mapped once before the ref resolves.
- New files must be registered in `HMI.hmiproj` as `<Content Include="…">`.
- `%l%` keys must exist in **both** `en.localization` and `de.localization`.
- A symbol-value trigger may not fire until the first *change*; give colour-driven controls a static
  default so they never render unstyled.
