# SpongeBobRecomp v0.1.5

Follow-up to v0.1.4. This release completes the fullscreen ALT+F4 close fix
and adds controller layouts that work when RecompLauncher starts the runner
directly. No game data is included.

## Why v0.1.5

v0.1.4 fixed the `0xC0000005` swap-chain crash, but a close could still
intermittently hang: the CPU thread was inside the presenter's frame-pacing
sleep while `CPUManager::Stop()` waited for it to acknowledge `PowerDown`.
When that happened, the window stayed open and the user had to close it again.

## Fixed

- **Presenter sleep is skipped during shutdown.** `Presenter::Present()` now
  calls `CoreTiming::SleepUntil()` only while `Core::IsRunning()` is true.
  The CPU thread acknowledges `PowerDown` immediately, so `CPU::Stop()` can
  join it.
- **Shutdown watchdog.** A processed close now has an 8-second last-resort
  watchdog. If a Vulkan/shader/driver wait still blocks the normal shutdown,
  the process exits cleanly instead of staying unresponsive. The watchdog does
  nothing on a normal close, which completes in under a second.
- **v0.1.4 remains in this build:** windowed creation followed by delayed
  borderless fullscreen, no `ToggleFullscreen()` in the destructor, swap-chain
  image validation, non-modal failed-recreation handling, and the 3-second
  power-button grace period.
- **Fullscreen placement is delayed until the window is placed.** The style
  change waits about one second after the main loop starts, so Windows cannot
  overwrite the monitor-origin position. The window now covers exactly
  `0,0,2560,1440` on the test monitor.
- No game data; JIT default, static module optional, 60 FPS cap, 14
  RecompLauncher settings and icons are unchanged.

## Controller support

RecompLauncher never opens the custom launcher, so controller selection cannot
live only in that UI. The runner now owns it:

- **Auto-detection.** The runner enumerates SDL gamepads, reads the SDL gamepad
  type (with a product-name fallback) and selects Xbox, PlayStation, Switch or
  generic.
- **Switch uses the printed labels.** Switch A/B/X/Y map to GameCube A/B/X/Y;
  Xbox, PlayStation and generic use the physical positions. This fixes the
  common Switch A/B and X/Y swap.
- **Stale profiles are regenerated.** `controller_profile=auto` writes the
  correct device and layout on every launch, so changing controllers does not
  leave an old `GCPadNew.ini` behind. `manual` preserves a profile chosen in
  the custom launcher; `xbox`, `playstation`, `switch` and `generic` force a
  layout.
- **RecompLauncher setting.** The manifest now exposes **Controller layout**
  (Auto-detect / Xbox / PlayStation / Switch / Generic), bringing it to 14
  settings. The same value can be written directly as
  `controller_profile=...` in `config.ini`.
- The custom launcher's CONTROLLER page still selects a specific device and
  writes `controller_profile=manual` so the runner keeps that choice.

## Verified

At 2560x1440, internal scale 4x, MSAA 8x, widescreen, Vulkan, JIT:

- 10/10 consecutive fullscreen closes from the packaged build; each completed
  in about 0.5-0.8 seconds with no new crash dumps.
- Fullscreen close, loaded-state close, F11 leave/re-enter then close,
  windowed close and fullscreen double-close all exit cleanly.
- Packaged controller tests: auto selected the Xbox layout, explicit Switch
  wrote `Buttons/A=Button B`, `B=Button A`, `X=Button Y`, `Y=Button X`, a
  stale profile was replaced with the connected device, and `manual` preserved
  the existing profile.

The window reports `0,0,2560,1440` in fullscreen.

## Download

`SpongeBobRecomp-v0.1.5-Windows-x64.zip` (28,803,228 bytes).

SHA-256:

```text
1A0CEBD909F4D522D1FC376F445EBBD3CC1A63634959432074B28AF759E81F31  SpongeBobRecomp-v0.1.5-Windows-x64.zip
```
