# Changelog

## v0.1.4 - 2026-11-09

Fixes the fullscreen ALT+F4 close error.

- Closing a fullscreen session no longer hangs or exits with `0xC0000005`.
  The runner creates its window windowed, lets the video backend initialize,
  then applies borderless fullscreen, so the runtime keeps its normal windowed
  shutdown path. This is the same model the Rocket Power recomp uses.
- The swap chain now validates the current image index, texture and framebuffer
  before every present. A failed resize or surface recreation logs and skips
  the frame instead of dereferencing a null image or opening a modal warning.
- A single close is enough: if the game does not handle the power-button event,
  the runner exits after a 3-second grace period instead of requiring a second
  ALT+F4.
- F11 / Alt+Enter still toggles fullscreen; windowed mode is unchanged.
- JIT default, static module optional, 60 FPS cap, 13 RecompLauncher settings,
  icons and no game data: unchanged.

## v0.1.3 - 2026-11-09

This release replaces the earlier v0.1.3 static-only build.

- **JIT is the default playable path.** It holds the native 60 FPS in the
  Bikini Bottom section outside SpongeBob's house, where the static module
  drops to about 40 FPS. Choose **CPU core** in the custom launcher's
  PERFORMANCE page or on the RecompLauncher game page. The static module is
  still included and selectable.
- **Fixed frame-rate dips in the static recomp.** The game's frame limiter is a
  tight wait loop at `0x800F5F90`. The runtime now skips it with
  `StaticRecompIdlePC` and advances CoreTiming to the next VI/audio event
  instead of executing millions of host iterations per frame. This keeps the
  static core at 60 FPS in lighter scenes and improves the outdoor scene.
- **The game is capped at 60 FPS.** The Unlocked, 150% and 200% options are
  removed from the custom launcher and from RecompLauncher. Existing
  `config.ini` files that still contain `emulation_speed=0`, `1.5` or `2` load
  at 60 FPS automatically.
- **Ships the idle-loop setting** in `Sys/GameSettings/GSQE78.ini` so both the
  custom launcher and RecompLauncher get the fix.
- **Executable icons.** The launcher and runner now embed distinct multi-size
  icons.
- RecompLauncher now exposes 13 settings, including **CPU core**; its
  `config.new` writes `cpu_core=jit`.
- Still no game data in the package.

## v0.1.2 - 2026-11-08

- **RecompLauncher support.** The release ships `recomplauncher.json` at the
  top of the zip. Level 1 setup uses the player's USA ISO; level 2 exposes the
  graphics, frame-rate and audio settings; level 3 extracts the disc in a
  headless prepare step and includes the Redump USA size/CRC-32 for the
  verified badge.
- The custom launcher's `--extract` command now prints
  `progress <0-1> <text>` lines so RecompLauncher can show setup progress.
- The release asset is named `SpongeBobRecomp-v0.1.2-Windows-x64.zip` so
  RecompLauncher can identify the Windows x64 build.
- RecompLauncher starts `SpongeBobRecompRunner.exe` directly and uses the same
  `config.ini`, saves and logs as the app.
- The runner auto-detects the first SDL gamepad and generates the same
  `GCPadNew.ini` profile the custom launcher would, so a fresh install is
  controller-ready.
- Still no game data in the package.

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
