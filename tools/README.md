# Development helper scripts

These are the small tools used while building and validating the port. They do
not contain game data.

- `verify_dol.py` - compare an extracted `main.dol` with the disc's DOL
  (size, SHA-256, SHA-1 and byte differences).
- `rvz_extract.py` - decompress a Dolphin RVZ image to an ISO. The app has its
  own ISO/RVZ importer; this script is only for inspecting a disc offline.

The recompiler and runtime are separate upstream projects (DolRecomp,
ModernGekko/Dolphin); see the main README.
