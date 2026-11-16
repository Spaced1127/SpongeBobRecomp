# Development helper scripts

These are the small tools used while building and validating the port. They do
not contain game data.

- `verify_dol.py` - compare an extracted `main.dol` with the disc's DOL
  (size, SHA-256, SHA-1 and byte differences). Accepts `.iso` or `.rvz`.
- `gcdisc.py` - inspect, list, extract or dump the DOL from a GameCube disc.
  Reads `.iso` and `.rvz` directly; `extract` writes the same `sys/` + `files/`
  tree as the app.
- `rvz_extract.py` - native RVZ reader and optional RVZ-to-ISO export. The app
  and `gcdisc.py` do not need the export; it is only for another tool that
  requires a raw ISO.
- `card_report.py` - read a SpongeBobRecomp user directory and report the
  memory card: slot A/B device, raw card size + SHA-256, and every save
  directory entry (game code, company, file name, blocks). Host-side only;
  useful in a support report.

The recompiler and runtime are separate upstream projects (DolRecomp,
ModernGekko/Dolphin); see the main README.
