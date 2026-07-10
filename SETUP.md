# Running LIMEN from the terminal

LIMEN installs as a real `limen` command. After `pip install -e .` (or a release
install) the binary lands on your `PATH` and you can run it from anywhere.

## Quick start

```bash
# From anywhere in your terminal:
limen                 # welcome banner
limen --help          # full command list
limen awaken          # wake the Soul Kernel (reads SOUL.md/IDENTITY.md/CONSTITUTION.md)
limen space inspect   # look at the three spatial realms
limen space hyper "smallest honest path to recurring income" --paths 4
```

## Home directory (where LIMEN lives)

LIMEN reads its canonical identity files (`SOUL.md`, `IDENTITY.md`,
`CONSTITUTION.md`) from the **project root**. That is normally the LIMEN
repository folder itself, or any folder that contains those files.

Two ways to point LIMEN at its home:

1. Run from inside the folder (default `--root` is the current directory):
   ```bash
   cd /path/to/limen
   limen awaken
   ```
2. Or set the `LIMEN_ROOT` environment variable once (then you never pass `--root`):
   ```bash
   export LIMEN_ROOT="/path/to/limen"
   limen space hyper "a question" --paths 5
   ```
   Add that `export` to your shell profile (`~/.bashrc`, `~/.zshrc`, or
   `$PROFILE` on PowerShell) to make it permanent.

LIMEN's private runtime state is written to `.limen/` inside that root and is
git-ignored. It never leaves your machine.

## Display

Output renders through a glowing Rich panel. Language-signals are color-coded:
`execution_authorized: [no]` (red), `authorized: [yes]` (green). This is a
display layer only — it does not change any behavior or permission gate.

## Requirements

- Python >= 3.11
- `rich>=13.0` (installed automatically)
- No mandatory cloud, no paid API, no network.
