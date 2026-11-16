# Changelog

## v0.1.7 - 2026-11-16

Controller hotfix for the v0.1.6 Xbox reports, plus the shared memory-card fix.

- **Raw memory card in slot A, empty slot B.** The runtime now writes
  `[Core] SlotA = 1` (raw `MemoryCardA.<region>.raw`, 16 MiB) and
  `SlotB = 255` (None) into `Config/Dolphin.ini` on every launch, after the
  user-path tree exists and before the EXI devices initialise. Earlier builds
  left `SlotA` unset, so Dolphin's GCI folder default was used and
  `Dolphin.ini` was never created.
- **Existing saves are migrated, not abandoned.** A `.gci` folder card from
  v0.1.6 or older is imported into the raw card once and the old files are
  left as a backup; if the import fails the game keeps using the folder card.
- RecompLauncher's manifest now also writes `Core/SlotA = 1` and
  `Core/SlotB = 255` for launcher-only installs.
- Startup line: `memory card: slot A = raw, slot B = none, ...` with the file
  and byte size or the migration count.

- **Every Xbox pad resolves Xbox.** Detection falls back to the SDL GUID
  vendor word (`045E` Xbox, `054C` PlayStation, `057E` Nintendo), so a Xbox 360,
  One, Series or Elite pad is classified correctly even when its product ID is
  newer than the table (`0B20`, `0B2A`, ...). Reported as
  `source=guid-family` in the startup line.
- **The Nintendo layout needs a Nintendo signal.** The `a`-after-`b` mapping
  rule now requires an 8BitDo vendor, SDL's printed-label hint or a paddle, and
  never overrides a GUID/Xbox/PlayStation verdict. In v0.1.6 that rule flipped
  110 of the 797 SDL database rows to printed-label A/B and X/Y — the generic
  "USB Gamepad", PS2-adapter, Steam virtual-pad and third-party Xbox-shape rows.
- **Button-order D-pads are no longer inverted.** Only a reversed hat/axis sets
  the D-pad correction; 34 rows (DualShock 3, PS2 adapters, Steam pads) had
  left/right swapped.
- **The generated device matches the runtime.** The runner sets Dolphin's own
  SDL hints before enumerating, so the `Device = SDL/...` line it writes is the
  device the runtime creates.
- Startup diagnostics add the device and profile path to the
  `controller configuration:` line; the `controller:` line is unchanged.
- Offline: 130 checks pass (34-row real SDL DB matrix, byte-identical Xbox
  profile, unknown-PID fallback, non-8BitDo `a>b`, button D-pad).

## v0.1.6 - 2026-11-15

- Native RVZ input. RecompLauncher's setup screen advertises `.iso or .rvz`
  and checks `GSQE78` by content with `check.ids`; the launcher and tools read
  RVZ by its `RVZ\x01` magic with no conversion step.
- `tools/gcdisc.py` and `tools/verify_dol.py` read RVZ directly;
  `gcdisc.py extract` writes the same `sys/` + `files/` tree as the app.
- DualSense Edge (`054c:0df2`) and Xbox Elite Series 1/2 (`045e:02e3`,
  `0b00`, `0b05`, `0b22`) are detected from the SDL GUID and use the standard
  DualSense/Xbox layouts. Paddles and Fn/extra buttons are deliberately
  unbound.
- Startup diagnostics now print name, GUID, bus, VID/PID, layout, source,
  D-pad/face swap and paddle/Fn status; standard DualSense, Xbox and Switch
  pads are regression-tested.
- 8BitDo Pro 2 in Nintendo/Switch mode is detected from the live SDL `a`/`b`
  mapping and uses printed A/B/X/Y labels; Ultimate and 64 stay standard.
  Reversed D-pad bindings are corrected, auto profiles migrate, and manual
  profiles are preserved.

## v0.1.5 - 2026-11-14

Completes the fullscreen ALT+F4 close fix and adds controller layouts that
work when RecompLauncher starts the runner directly. Use this instead of
v0.1.4.

- **Presenter sleep is skipped during shutdown.** The CPU thread could enter a
  long frame-pacing sleep in `Presenter::Present()` while `CPUManager::Stop()`
  waited for it to acknowledge `PowerDown`, so a close could still hang.
  `Present.cpp` now calls `CoreTiming::SleepUntil()` only while
  `Core::IsRunning()` is true.
- **8-second shutdown watchdog.** If a Vulkan/shader/driver wait still blocks a
  processed close, the process exits cleanly instead of staying unresponsive.
  Normal closes finish in under a second and never reach it.
- **Fullscreen placement is delayed.** The borderless style change waits about
  one second after the main loop starts, so the window covers exactly
  `0,0,2560,1440` instead of keeping its default windowed offset.
- **Controller layouts are runner-owned.** The runner auto-detects Xbox,
  PlayStation, Switch and generic SDL pads, writes the matching
  `GCPadNew.ini`, and uses printed Switch A/B/X/Y labels. `auto` regenerates
  stale profiles; `manual` preserves a custom launcher selection; the other
  values force a layout.
- RecompLauncher now exposes **Controller layout**, bringing the manifest to
  14 settings.
- v0.1.4's delayed borderless fullscreen, no destructor fullscreen toggle,
  swap-chain image validation, non-modal failed-recreation handling and
  3-second power-button grace remain.
- Verified 10/10 packaged fullscreen closes at 2560x1440/scale 4/MSAA 8x; no
  new crash dumps; auto/Switch/stale/manual controller tests pass.
- No game data; JIT default, static module optional, 60 FPS cap and icons
  unchanged.

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
