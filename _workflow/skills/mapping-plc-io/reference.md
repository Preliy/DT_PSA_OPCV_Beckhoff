# Reference — PLC ↔ EtherCAT I/O

Projects: `Beckhoff/TwinCAT_1/PLC/{PLC_1, SIM_1}`. Libraries: `OC_Core 1.3.1`,
**`OC_EtherCAT 1.1.8`** (SIM_1 only), `SPT Components 3.9` (PLC_1 only).

The live inventory — every terminal, every channel, what is on it and what is free — is
generated into `Beckhoff/_docs/context/plc-io.md`. **Read that, not a table in this file.**
Everything here is the grammar and the library shape, which change far more slowly.

## Terminal image structs — `OC_EtherCAT`

Direction is baked in **from the simulation PLC's point of view**: a slave's *input*
channel is something the simulation must produce, so it is `AT %Q*`; a slave's *output*
channel is something the master produced, so the simulation reads it at `AT %I*`. That is
why nobody hand-inverts a direction — picking the right struct is the whole decision.

| Struct | Members | Dir | Type |
|---|---|---|---|
| `ST_Beckhoff_4DI` | `bIn1..bIn4` | `%Q*` | `BIT` |
| `ST_Beckhoff_8DI` | `bIn1..bIn8` | `%Q*` | `BIT` |
| `ST_Beckhoff_16DI` | `bIn1..bIn16` | `%Q*` | `BIT` |
| `ST_Beckhoff_4DO` | `bOut1..bOut4` | `%I*` | `BIT` |
| `ST_Beckhoff_8DO` | `bOut1..bOut8` | `%I*` | `BIT` |
| `ST_Beckhoff_16DO` | `bOut1..bOut16` | `%I*` | `BIT` |
| `ST_Beckhoff_4DI_4DO` | `bIn1..4` + `bOut1..4` | `%Q*` / `%I*` | `BIT` |
| `ST_Beckhoff_8DI_8DO` | `bIn1..8` + `bOut1..8` | `%Q*` / `%I*` | `BIT` |
| `ST_Beckhoff_2AI` | `nStatusN`, `nValueN` ×4 | `%Q*` | `UINT` / `INT` |
| `ST_Beckhoff_4AI` | `nStatusN`, `nValueN` ×2 | `%Q*` | `UINT` / `INT` |
| `ST_Beckhoff_4AO` | `nAnalogOut1..4` | `%I*` | `UINT` |
| `ST_Beckhoff_EL3403` | `nCurrentN`, `nVoltageN`, `nActivePowerN` | `%Q*` | `UINT` |
| `ST_Beckhoff_EL5002` | `nStatusN`, `nCounterN` | `%Q*` | `UINT` / `UDINT` |
| `ST_Beckhoff_EL9110` | `bPowerOk` | `%Q*` | `BIT` |
| `ST_Beckhoff_EL9410` | `bUsUndervoltage`, `bUpUndervoltage` | `%Q*` | `BIT` |

Members are `BIT`, not `BOOL`. Assignment between the two is accepted; if the compiler
objects on a particular member, that is the first thing to check.

The library also carries FBs for terminals with protocol behaviour — `FB_Beckhoff_EL1904`,
`EL2904`, `EL1918`, `EJ1918`, `EK1914` (safety), `EL6001` (serial), `EL5152`, plus
`FB_DS402_*`, `FB_Sercos_*`, `FB_FSOE_19`, `FB_Mitsubishi_MRJ4TM` for drives.

## `TcLinkTo`

Links a variable to the I/O tree from PLC source. Verbatim, from
`SIM_1/Hil/EtherCAT_1_SIM/GVL_EtherCAT_1_SIM.TcGVL`:

```
{attribute 'linkalways'}
{attribute 'qualified_only'}
{attribute 'subsequent'}
{attribute 'pack_mode' := '1'}
VAR_GLOBAL
{attribute 'TcLinkTo' := '
.bIn1 := TIIB(37)^Channel 1^Input;
.bIn2 := TIIB(37)^Channel 2^Input;
 ...
.bIn8 := TIIB(37)^Channel 8^Input'}
FG_01_EL1008_1 : ST_Beckhoff_8DI;
END_VAR
```

Grammar: `.<member> := TIIB(<boxId>)^<channel>^<process image>;` — entries separated by
`;`, the last one **without** a trailing `;`, the whole block inside one attribute string.
For a single scalar the leading `.` is dropped and the pragma names the target directly.

The four GVL attributes matter: `linkalways` keeps unused variables in the image so a link
never silently disappears; `subsequent` and `pack_mode := '1'` keep the struct byte-packed
in declaration order so channel *n* stays channel *n*.

**The two forms are not interchangeable.** See the SKILL's "What a `TcLinkTo` pragma
actually links": the member-path form works on a STRUCT and not on a FUNCTION_BLOCK
instance.

### Box ids

`TIIB(n)` is the `<Box Id="n">` in the tsproj, under the right `<Device>`. Both masters
carry identically-named boxes, so the id is the only thing distinguishing them — and
`TIIB(2)` where you meant `TIIB(37)` compiles and links to the wrong device.

Do not grep for them. The generated map has them:

```bash
python Beckhoff/_private/tools/plc_io.py terminals --device EtherCAT_1
python Beckhoff/_private/tools/plc_io.py terminals --device EtherCAT_1_SIM
```

### The control side does not use `TIIB`

`PLC_1` uses the full symbolic path, which survives a renumbering:

```
TIID^EtherCAT_1^FG_01 (EK1100)^FG_01_EL1008_1^Channel 1^Input
```

Note the coupler segment. The real master **nests** terminals under their `EK1100`; the
simulated master is **flat**. The OwnerB path in `Mapping_PLC.xml` mirrors that nesting,
which is why it cannot be derived from the box name alone.

## `Mapping_PLC.xml`

Root `<VarLinks>`, one `<OwnerA Name="TIPC^PLC_1^PLC_1 Instance">`, one `<OwnerB>` per
terminal box, `<Link>` sorted by `VarA` within it. No BOM, header exactly
`<?xml version="1.0"?>` with no `encoding`, CRLF throughout including the last line, tab
indentation, `<Link .../>` self-closing with no space before the slash, no `<MappingInfo>`
and no `AutoLink` attribute.

```xml
<Link VarA="PlcTask Inputs^MAIN.Machine.FG_01.P_Reader.HardwareInput" VarB="Channel 7^Input"/>
```

`VarA` is `<data area name>^<symbol path>`. The area name comes from the `.tmc`'s
`<DataArea><Name>` — `PlcTask Inputs` / `PlcTask Outputs` — and is named after the task, so
a renamed task orphans every link. `plc_io.py` reads it; never hardcode it.

**Do not hand-write this file.** `python Beckhoff/_private/tools/plc_io.py write-mapping` emits it
byte-exactly, and `write-mapping --no-op` proves the round-trip reproduces the current file
before you trust it with a change.

`TIPC^SIM_1^SIM_1 Instance` is the other `<OwnerA>` in the tsproj — 136 `AutoLink` links
produced by the SIM GVL's pragmas. Read it, never write it.

## OC_Core device FB members — the twin half of every line

From `SIM_1/<FG>/<FG>.TcPOU`'s generated `VAR_INPUT` block. "in" = the PLC commands it
(`%Q*` side), "out" = the twin reports it (`%I*` side).

| FB | In (twin reads) | Out (twin writes) |
|---|---|---|
| `FB_Cylinder` | `bRetract`, `bExtend` | `bRetracted`, `bExtended` |
| `FB_SensorBinary` | — | `bValue` |
| `FB_Drive` | `nControl.0` fwd, `nControl.1` rev, `fTargetValue` | `nStatus.6` active, `nStatus.7` valid, `fActualValue` |
| `FB_Reader` | `nControl`, `nCommand` | `nStatus`, `nResult` |
| `FB_DeviceByte` | `nControl`, `nControlData` | `nStatus`, `nStatusData` |
| `FB_Lamp` | `bEnable` | — |
| `FB_Button` | `bEnable` (feedback lamp) | `bValue` |
| `FB_Lock` | `bLock`, `nControlData` | `bClosed`, `bLocked`, `nStatusData` |
| `FB_Panel` | `nControlData` (DWORD) | `nStatusData` (DWORD) |
| `FB_SensorAnalog` | — | **`nValue` (UINT, raw)**, `fValue` (REAL, scaled) |

Bit access on a `BYTE` member is valid ST and is how a single channel reaches a packed
device:

```
Y_LaserMark.nControlData.0 := GVL_EtherCAT_1_SIM.FG_01_EL2008_1.bOut6;
```

For an analog device map the **raw** member — a terminal channel carries counts, not
engineering units. `FB_SensorAnalog` scales `nValue` into `fValue` itself via `stConfig`,
so `... .nValue1 := B_Pressure.nValue;` is right and `fValue` is not.

**When a type is missing from the `.tmc`** — because no instance of it exists in the
machine yet — read it from the library source instead: `OC_Core.library` is a ZIP whose
`__shared_data_storage_string_table__.auxiliary` holds the real ST. That is how the analog
rows above were confirmed.

## Component-owned hardware, and why it bites

SPT components on the control side own their process-image variable.
`FB_DigitalSensor` declares `HardwareInput AT %I* : BOOL`; `FB_SingleSolenoidFeedback`
declares `_ExtendOutput AT %Q* : BOOL`.

So a sensor consumes a real terminal channel that appears in no GVL anywhere. Counting only
the signals you can see declared in the module under-counts the group, and allocating
around a component-owned channel double-books it. `plc_io.py` counts from the process
image, which includes them; a human counting by eye does not.

## Traps

- **`TIIB(2)` where you meant `TIIB(37)`** compiles and links to the wrong master.
- **A member-path pragma on an FB instance** is accepted, reports nothing, and links
  nothing.
- **Importing `Mapping_PLC.xml` on top of existing links** adds duplicates rather than
  replacing. Clear the Mappings node first.
- **Editing `Mapping_PLC.xml` and forgetting to import it** leaves the links on disk and
  nowhere in the running configuration. `plc_io.py reconcile` is the only thing that
  notices.
- **The `.tmc` is read only by `plc_io.py build`**, to refresh the committed snapshot after an
  XAE rebuild. Everything else reads the snapshot, whose validity is checked by a comment-stripped
  code digest rather than by a timestamp.
