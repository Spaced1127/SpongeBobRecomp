# Changelog

## v0.1.1 - 2026-11-08

Patch release for fullscreen and shutdown.

- **Start in fullscreen now applies.** The Windows NoGUI platform created the
  window but never entered fullscreen; it now uses the monitor's full
  resolution at startup.
- **Fixed the "Session failed" error on exit.** Closing a fullscreen window
  could deliver a focus-loss message after the config layers had been
  destroyed, causing an access violation (`0xC000041D`). Window callbacks now
  skip config writes after shutdown, and the window leaves fullscreen before
  it is destroyed.
- **Removed the white frame in fullscreen.** The client edge and white window
  background are removed in fullscreen; the client area now exactly covers the
  monitor and the windowed edge is restored when leaving fullscreen.
- The runner logs the applied video settings at startup, e.g.
  `[video] backend=Vulkan scale=4 msaa=4 ssaa=0 af=4 vsync=1 aspect=1 widescreen=0 fullscreen=1`.
- Rebuilt the clean release package; still no game data. See the release
  notes for the SHA-256.

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
