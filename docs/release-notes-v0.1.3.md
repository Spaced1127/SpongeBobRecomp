# SpongeBobRecomp v0.1.3

Fixes the frame-rate dips in the static recomp and caps the game at its native
60 FPS.

## What changed

- **Frame-limiter fix.** The game waits for the next VI/audio event in a tight
  loop at `0x800F5F90`. The runtime now uses `StaticRecompIdlePC` to advance
  CoreTiming to that event instead of running millions of host loop iterations
  per frame. In the living-room benchmark the recompiled module now matches
  Dolphin's JIT CPU speed: about **1.21x**, up from **1.02x**.
- **60 FPS cap.** The Unlocked, 150% and 200% options are removed from the
  custom launcher and from RecompLauncher. Existing `config.ini` files that
  still contain `emulation_speed=0`, `1.5` or `2` load at 60 FPS automatically.
- **Ships the idle-loop setting** in `Sys/GameSettings/GSQE78.ini`, so both
  the custom launcher and RecompLauncher get the fix.
- RecompLauncher now shows 12 settings instead of 13; its `always` block keeps
  `emulation_speed=1`.
- Still no game data in the package.

## Measurements

Living room, Vulkan, no VSync, unlocked only for the benchmark:

| Configuration | Before | After |
|---|---:|---:|
| 1080p, MSAA 8x + SSAA | 61.9 fps / 1.038x | **67.7 fps / 1.119x** |
| 1440p, MSAA 8x + SSAA | - | **64.7 fps / 1.070x** |
| 1x, no MSAA/SSAA (CPU test) | 61.0 fps / 1.024x | **72.3 fps / 1.207x** |

With the shipped 60 FPS cap the living room holds 60 FPS. If another app is
using the GPU heavily, close it or lower MSAA/SSAA; the game can still dip
under external GPU load.

## Download

`SpongeBobRecomp-v0.1.3-Windows-x64.zip` (about 28 MB).

SHA-256:

```text
B719F8455A2568D4B8A3DA68F78BEF7D8DB9E10855E6EE0EC8ACBC2140169474  SpongeBobRecomp-v0.1.3-Windows-x64.zip
```
