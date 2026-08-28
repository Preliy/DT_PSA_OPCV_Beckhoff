# Architecture — the TwinCAT side

How this module is organised, and why.

For the twin and the vendor boundary in general, see [how it works](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/03-how-it-works.md);
for the context pipeline, [the engineering workflow](https://github.com/Preliy/DT_PSA_OPCV/blob/master/_docs/05-engineering-workflow.md).

## 1. Two PLC projects, one EtherCAT pair

![Unity and the TwinCAT emulation unit, with a TwinCAT machine PLC behind an emulated EtherCAT](https://raw.githubusercontent.com/Preliy/DT_PSA_OPCV/master/_docs/images/OC_Base_Beckhoff.svg)

The Open Commissioning base setup is the twin plus an emulation unit; what this module adds is the
control side — a second PLC project and the real hardware configuration behind an emulated bus.

```
   TwinCAT_1/PLC/TwinCAT.tsproj
     PLC_1   AmsPort 851   the control program (SPT framework), drives EtherCAT_1
     SIM_1   AmsPort 852   the twin device layer, OC Assistant's output, on EtherCAT_1_SIM

   Unity ── ADS ──> SIM_1
   PLC_1 ── EtherCAT ──> EtherCAT_1  ⇄  EtherCAT_1_SIM ── SIM_1
   TwinCAT_1/HMI (TE2000) ── ADS ──> PLC_1 as runtime PLC1 (bound by PORT 851)
```

**`PLC_1` never talks to Unity.** It talks to EtherCAT terminals, exactly as it would on the real
machine. `SIM_1` sits on the other end of those terminals holding one function block per twin device
— `FB_Cylinder`, `FB_SensorBinary`, `FB_Camera` and so on — and Unity binds *those* symbols.

That indirection is the entire point. The control program cannot tell it is running against a twin,
so nothing about it has to change when it runs against steel. A test rig that the program is aware
of proves much less.

## 2. What is generated and what is not

| Path | Written by |
|---|---|
| `TwinCAT_1/PLC/SIM_1/**` — the `{region generated code}` blocks | **OC Assistant.** Never edit; regenerated from the twin's device list |
| `TwinCAT_1/PLC/SIM_1/**` — the `Mapping` action | You |
| `TwinCAT_1/PLC/PLC_1/**` | You — the control program |
| `TwinCAT_1/PLC/Mapping_PLC.xml` | The I/O mapping build, imported in XAE |
| The machine pages | **A generator.** Swept on every run; never hand-edit |
| The curated reference | You — hand-written TwinCAT knowledge |

## 3. The control program

`PLC_1` is built on the **SPT framework** (V3.9 — note that the published SPT documentation describes
V4, and disagrees with the shipped binary in several places). One equipment module per functional
group, under `Modules/NN FG_xx/`.

How the framework is meant to be used, the official build order, and which third-party claims about
it are wrong: [SPT framework](../_docs/reference/spt-framework.md).

**When a source disagrees with the shipped binary, the binary wins.**

## 4. I/O and linking

Every twin device's process image is linked to an EtherCAT terminal channel. Which channel each
signal is on, what is still free, and whether the link file and the project agree:
[the I/O map](../_docs/context/plc-io.md).

Signals that are unlinked **on purpose** are listed in
[unlinked signals](../_docs/reference/plc-io-exceptions.md), so a real
gap is not hidden by a deliberate one.

One trap worth stating here because it fails silently: **a `TcLinkTo` member path resolves on a
STRUCT, not on a FUNCTION_BLOCK instance.** On an FB instance the compiler accepts the pragma,
reports nothing, and links nothing. A link is real when it appears in the `tsproj` `<Mappings>`.

## 5. How the TwinCAT description is produced

The per-group TwinCAT pages are **generated** from two inputs: the twin's structure, and this
module's own TwinCAT projects.

```
  the machine's structure       schema-versioned JSON, committed here
        +
  TwinCAT_1/PLC/**              the type model, read once into a committed snapshot
        ▼
  the machine pages             machine.md  fg-*.md  devices/*.md  plc-io.md
```

**That structure file is the whole coupling to the main repository.** This module never re-parses
the Unity export. The file is schema-versioned, and a consumer that does not recognise the schema
refuses rather than guessing — so a format change cannot be rendered from fields that may have
moved.

### Freshness is checked by code digest, not timestamp

The snapshot's validity is decided by hashing the `PLC_1` sources **with every comment stripped**.
Prose can be rewritten freely and the snapshot stays valid; a declaration, member, pragma or located
variable changes it.

This matters because `PLC_1.tmc` is a git-ignored build artifact whose timestamp is not a usable
signal — a checkout rewrites source mtimes around it, and a comment-only edit would mark it stale
for a change that cannot alter a single type. A group page banners itself only when the snapshot is
genuinely behind.

## 6. Where the boundary runs

| Fact | Lives |
|---|---|
| Which devices exist, their types and twin PLC paths | Main repo — generated from the twin |
| How a group sequences, interlocks, faults and recovers | Main repo — the behaviour contracts, platform-neutral |
| Which `FB_*` a device becomes, its terminal channel, its HMI struct | **Here** |
| The verified control PLC path `MAIN.Machine.<group>.<device>` | **Here** — it is a TwinCAT fact |

A machine-level fact placed in this module would be invisible to the Siemens port that has to honour
it. A TwinCAT fact placed in the main repository would have no generator to keep it true — the root
builder does not even import a vendor tool.
