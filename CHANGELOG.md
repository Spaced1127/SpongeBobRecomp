# Changelog

## v0.1.0 - 2026-11-08

First public build.

- Standalone Windows x64 launcher + runner + recompiled module for
  `GSQE78` (SpongeBob SquarePants: Revenge of the Flying Dutchman, NTSC-U).
- No game data in the package; the user imports their own ISO or RVZ.
- Built-in ISO/RVZ extraction with disc-ID and retail-DOL verification.
- Graphical launcher with PLAY / GRAPHICS / PERFORMANCE / AUDIO / CONTROLLER
  pages, animated procedural underwater backdrop and persisted settings.
- Graphics: Vulkan/OpenGL, 1x-12x internal resolution, MSAA, SSAA, anisotropic
  filtering, VSync, aspect ratio, widescreen hack, EFB 2D compatibility.
- Performance: native 60 FPS (PGO + x86-64-v3 module) and Unlock frame rate.
- Audio: mute all audio and master volume.
- Cross-chunk direct calls in the recompiler: intro movies now run at 1.0x with
  continuous audio (previously 0.41x with distorted audio); gameplay improved
  from ~54.6 to ~59.7 fps.
- Verified: ISO/RVZ import, legal/title, intro movies, bedroom -> living room,
  HUD, pause/Options, save/load, memory card.
