# Third-party components

This project builds on and is distributed with components from:

- **Dolphin** - GameCube/Wii emulator, GPLv2-or-later; the aggregate runtime is
  GPLv3-compatible. https://github.com/dolphin-emu/dolphin
- **ModernGekko** - Dolphin-derived static-recomp runtime/chassis used by the
  runner. Distributed here under the GPL.
- **DolRecomp** - static recompiler that generates the per-game module.
  GPLv3 (full text in `LICENSES-DolRecomp.txt`).
- **Dear ImGui**, **SDL3**, **cubeb** and other Dolphin externals, under their
  respective licenses, as shipped in the runtime.

The game module `gGSQE78_recomp.dll` is generated from the user's own retail
DOL by DolRecomp; no game assets are included in this repository or the release
package.
