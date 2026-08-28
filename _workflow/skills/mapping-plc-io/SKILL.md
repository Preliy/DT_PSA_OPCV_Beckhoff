---
name: mapping-plc-io
description: Use when wiring the control PLC to EtherCAT terminals - allocating channels for a functional group's I/O, adding links to Mapping_PLC.xml, checking what is really linked versus what a pragma only claims, or extending the SIM_1 twin mapping to match. Reads the compiled process image and the real terminal inventory; refuses to allocate a channel that does not exist.
allowed-tools: [Bash, Read, Edit]
---

# Wiring the control PLC to EtherCAT

Two projects, two masters, one machine:

- **`PLC_1`** (AmsPort 851) drives the real master `EtherCAT_1`. Its devices are SPT
  components that own their process image.
- **`SIM_1`** (AmsPort 852) drives `EtherCAT_1_SIM`, the Beckhoff EtherCAT simulation.
  It sees `GVL_EtherCAT_1_SIM`, one struct per terminal.

**The box names are identical on both masters.** Only the box id differs — the real master
uses 1–14, the simulated one 26–39. That is why the SIM addresses terminals numerically as
`TIIB(n)` and the control side uses the symbolic `TIID^EtherCAT_1^...` path, and why a
`TIIB` number copied from the wrong master compiles and silently links to the wrong device.

## There are no I/O GVLs

Do not look for `GVL_IO_<FG>`. It does not exist and never did on this project. Every
device is an SPT component that declares its own hardware variables:

| FB type | Inputs | Outputs |
|---|---|---|
| `FB_DigitalSensor` | `.HardwareInput` | — |
| `FB_SingleSolenoidFeedback` | `.ExtendedSensor`, `.RetractedSensor` | `._ExtendOutput` |
| `FB_DoubleSolenoidFeedback` | `.ExtendedSensor`, `.RetractedSensor` | `._ExtendOutput`, `._RetractOutput` |
| `FB_TransferDrive` (project) | `._DriveActive` | `._Forward`, `._Backward` |

This table is documentation. The tools read the property, not the table — a member is a
process-image leaf when it carries `TcDataArea` in the compiled model, so a new component
type works without anyone updating anything.

Signals with no component that fits — a bare coil — are declared in the module itself with
`AT %Q*`, as `FG_01._LaserFire` is.

## What a `TcLinkTo` pragma actually links

The rule, established by reading `AutoLink="true"` (which marks a pragma-produced link)
across every revision of the tsproj:

> A **member-path** `TcLinkTo` (`.Member := ...`) resolves on a variable whose type is a
> **STRUCT/DUT**. It does **not** resolve on a variable whose type is a **FUNCTION_BLOCK**.
> A **single-target** `TcLinkTo` resolves on any plain located `AT %I*` / `AT %Q*` scalar,
> wherever it is declared.

The evidence:

| Site | Form | Links produced |
|---|---|---|
| `GVL_EtherCAT_1_SIM` — 12 STRUCT globals | member path | **136**, all `AutoLink="true"` |
| `FG_01._LaserFire` / `._ReaderTrigger` — plain `AT %Q*` | single target | **2**, `AutoLink="true"` |
| `FG_01.Y_Gripper` … — 10 FUNCTION_BLOCK instances | member path | **0**, in every revision |

`FG_01.TcPOU` carries ten member-path pragmas on FB instances that look like they work.
They do not — the 19 links they appear to have made all come from `Mapping_PLC.xml`.
`108 + 2 = 110`, the whole of `<OwnerA Name="TIPC^PLC_1^PLC_1 Instance">`.

**Two caveats, stated because they are not settled.** TwinCAT may simply decline to
auto-link a variable that already carries an imported manual link — those pragmas have
coexisted with those links throughout, so this evidence cannot exclude it. And the
FG_Transport failure had a second, independent cause recorded at `FG_Transport.TcPOU:44`:
it named `FG_Transport_EL1809_1`, a box that does not exist.

None of that changes what to do here. `FB_TransferIndex` is instantiated five times, so a
pragma inside the reusable unit block would apply to all five and cannot express a
per-instance channel at all. **The link file is the mechanism for anything inside a
reusable unit; the pragma is for bare located scalars.**

## The workflow

### 0. Establish the baseline

```bash
python Beckhoff/_private/tools/plc_io.py reconcile
```

Refuses on a channel booked twice, a direction mismatch, a channel the terminal does not
carry, a link to a symbol that is not in the process image, and — the check that did not
exist before — drift between `Mapping_PLC.xml` and the tsproj, which means the file was
edited and never imported on the Mappings node.

If it refuses, fix that first. There is nothing to add to a wiring that does not add up.

### 1. See what needs a channel, and what is free

```bash
python Beckhoff/_private/tools/plc_io.py instance --group FG_02
python Beckhoff/_private/tools/plc_io.py terminals --free
```

### 2. Propose — then review it with the user

```bash
python Beckhoff/_private/tools/plc_io.py propose --group FG_02
```

**This is the half-automatic boundary and it is deliberate.** The tool computes the
allocation; a human accepts it. Which card a signal lands on encodes intent that no file
records — `FG_Transport.TcPOU:46-55` keeps Index, Stopper, Lift and Drive channels on
separate cards so a section can be wired, tested and swapped without touching another's.
`propose` refuses to allocate onto a terminal belonging to another group unless you pass
`--allow-foreign-terminal`, and refuses outright when a group has no terminal at all,
printing what to add in XAE instead.

### 3. Write

```bash
python Beckhoff/_private/tools/plc_io.py write-mapping --group FG_02
```

Merges the allocation into `Mapping_PLC.xml` byte-exactly — CRLF, tabs, sorted, no
`AutoLink`, no `<MappingInfo>` — so the diff shows your change and nothing else. It refuses
if the file has uncommitted edits, which a rewrite would silently discard.

### 4. Import in XAE — carefully

**The import is additive, not a replace.** Importing a file whose links already exist
produces *two* links on the same variable. Export the Mappings node first, diff it against
the file, clear the node, then import. (TwinCAT's exact merge semantics here are not
verified; treat "additive" as the safe assumption.)

Then rebuild, activate, and re-run `plc_io.py reconcile`.

### 5. The SIM side

`GVL_EtherCAT_1_SIM` already declares all 12 terminals with bulk pragmas covering all 136
channels, so **no GVL edit is normally needed**. What changes is the `Mapping` action of
`SIM_1/<FG>/<FG>.TcPOU`, which copies between the twin device FBs and the simulated slave
image.

**Never touch the `{region generated code}` block.** OC Assistant owns it and overwrites it
on the next twin regeneration. The `Mapping` action is the only part of an `SIM_1` POU
that is ours.

Direction is already baked into the struct choice, so nobody hand-inverts anything — see
`reference.md`.

### 6. Report

Channels used, channels free, and every signal still unlinked. `plc_io.py reconcile` prints
all three.

## Rules

- **Never invent a channel.** A device with no allocation gets a `// TODO`, not a guess.
- **Count component-owned channels.** `FB_DigitalSensor` carries its own `HardwareInput`, so
  a sensor consumes a real channel. Allocating around it double-books.
- **A signal is linked when the project says so**, not when a pragma claims it.
  `reconcile` counts from the tsproj `<Mappings>`, never from source text.
- **Never edit `_docs/context/`.** `plc-io.md` is generated by `plc_io.py build`.

## Related

- `exporting-plc-symbols` — what exists before you wire it.
- `generating-plc-code` — write the module that declares the signals.
- `reference.md` — terminal image structs, the `TcLinkTo` grammar, OC_Core FB members.
