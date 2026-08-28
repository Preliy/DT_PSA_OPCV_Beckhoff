---
name: exporting-plc-symbols
description: Use when you need the control PLC's own truth rather than the twin's - the PLC Instance variable list, the process image, which symbols exist for an HMI binding or a link, or which of a group's signals are still unlinked. Reads the compiled type model offline; no TwinCAT and no Unity needed.
allowed-tools: [Bash, Read]
---

# Reading the PLC's own symbols

The twin says what the machine *has*. The PLC says what it *exposes*. They are not the
same set, and the paths differ. Everything here answers the second question.

## Three different symbol sets

Confusing these is the single most common way a link or a binding ends up pointing at
nothing, so get the vocabulary right before anything else.

| Set | Where | Example path | What it is |
|---|---|---|---|
| **Twin symbol** | `_docs/context/plc-symbols.md` | `MAIN.FG_01.P_Camera` | A device in the Unity twin that OC Assistant generates a simulation FB for |
| **PLC symbol** | `fg-XX.md` → **Components** | `MAIN.Machine.FG_01.P_Camera` | Anything the control PLC declares — reachable over ADS |
| **Process-image symbol** | `fg-XX.md` → **Mapping** | `MAIN.Machine.FG_01.P_Camera.InputData` | The subset that can be linked to a terminal channel |

**The twin path is not the PLC path.** They differ by the `Machine.` segment, because the
control program nests every group inside a `Machine` block that the twin has no equivalent
for. A twin path in a `<Link>` or a `%s%` binding resolves to nothing and reports nothing.

A process-image symbol is one whose member carries the `TcDataArea` property in the
compiled model. That is read, never assumed — a new SPT component type is picked up
without anyone updating a table.

## Where the answers already are

Read the document first. It answers most questions with no command at all:

- `Beckhoff/_docs/context/fg-XX.md` — that group's verified control paths (**Components**) and its
  full process image with terminal and link mechanism (**Mapping**).
- `Beckhoff/_docs/context/plc-io.md` — which terminal channel each signal is on, what is free.

## Step 1 — check freshness before you trust any of it

```bash
python Beckhoff/_private/tools/plc_io.py instance | head -3
```

> **This section describes `plc_io.py build` only.** Every other command, and every generated
> document, reads the committed `.plc-image.json` snapshot and never touches the `.tmc`.

`PLC_1.tmc` is a **build artifact** and is git-ignored. If a source has been edited since
the last build, the tool refuses:

```
REFUSED: PLC_1.tmc is stale - .../FG_Transport.TcPOU is newer than PLC_1.tmc.
```

Two honest ways forward, and no third:

- **Rebuild `PLC_1` in XAE**, then re-run. This is the right answer when you are about to
  generate code or wire I/O against the result.
- **`--from-snapshot`** is the default for everything except `build`. It renders from
  `Beckhoff/_docs/context/.plc-image.json`, the committed
  mirror of the last good build. Correct when TwinCAT is not available, and it works on a
  fresh clone. Say so in your report — it describes the PLC as of that build, not as of now.

Never work around the refusal with `--allow-stale` and then quote the result as current.

## Step 2 — query

```bash
python Beckhoff/_private/tools/plc_io.py instance --group FG_01     # one group's process image
python Beckhoff/_private/tools/plc_io.py instance --all-symbols     # the whole ADS tree, offline
python Beckhoff/_private/tools/plc_io.py instance --format json     # for further processing
python Beckhoff/_private/tools/plc_io.py terminals --free           # what channels are available
python Beckhoff/_private/tools/plc_io.py reconcile                  # does the wiring add up
```

`--all-symbols` expands every path reachable from `MAIN`, following `EXTENDS`. That is the
list the HMI server would offer, computed without a running server — use it to confirm a
binding target exists before writing it, rather than grepping `PLC_1.tmc` by hand.

## Step 3 — refuse to invent

If a symbol is not in the model, **it does not exist**. Do not put it in a link, a binding
or a document. `binding.symbolError` is `"Ignore"` in the HMI project and an unlinked
signal compiles cleanly, so nothing downstream will contradict you — which is exactly why
the check has to happen here.

When a name looks close but does not resolve, `python Beckhoff/_private/tools/hmi_check.py` names
the exact segment that broke and the rewrite that fixes it.

## The reconciliation identity

```
process image = linked + unlinked
```

`plc_io.py reconcile` asserts it and prints the parts. It also refuses on a channel booked
twice, a direction mismatch, a channel a terminal does not carry, and drift between
`Mapping_PLC.xml` and the tsproj. **Every one of those is silent in TwinCAT** — they
produce a build that succeeds and a machine where one device never moves.

Unlinked signals are reported, not refused: they are the normal work queue. The few that
are unlinked on purpose live in `Beckhoff/_docs/reference/plc-io-exceptions.md`, which is
hand-written — adding a row there silences a real check, so it needs a reason from the
project, not an assumption.

## Related

- `mapping-plc-io` — allocate channels and write the links.
- `generating-plc-code` — write the module that declares the symbols.
- `building-hmi-elements` — bind them on a panel.
