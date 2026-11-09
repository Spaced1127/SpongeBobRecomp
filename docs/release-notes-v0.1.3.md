# SpongeBobRecomp v0.1.3

This release replaces the earlier v0.1.3 build. The playable path now uses
Dolphin's **JIT core** at 60 FPS; the static recompilation module is still
included and can be selected as an optional core.

## What changed

- **JIT is the default playable path.** It holds the game's native 60 FPS in
  the Bikini Bottom section outside SpongeBob's house, where the static module
  drops to about 40 FPS. The selected core is shown under **CPU CORE** in the
  custom launcher and under **CPU core** on the RecompLauncher game page.
- **Static recompilation is still shipped.** `gGSQE78_recomp.dll` remains in
  the package and can be selected at any time. It is the faithful DolRecomp
  artifact, but heavy 3D scenes are CPU-limited.
- **Frame-limiter fix.** The static core skips the wait loop at `0x800F5F90`
  with `StaticRecompIdlePC` and advances CoreTiming to the next VI/audio event.
  This is why the static core now reaches about 42 FPS instead of 38 in the
  outdoor scene, and it still holds 60 FPS in lighter scenes.
- **60 FPS cap.** The Unlocked, 150% and 200% options are removed. Existing
  `config.ini` files load at 60 FPS automatically.
- **Executable icons.** `SpongeBobRecomp.exe` and `SpongeBobRecompRunner.exe`
  now embed distinct multi-size icons.
- RecompLauncher now exposes 13 settings, including **CPU core**; its
  `config.new` writes `cpu_core=jit`.
- Still no game data in the package.

## Measurements

Bikini Bottom outside SpongeBob's house, 1080p, MSAA 8x, no SSAA:

| Core | FPS | Speed |
|---|---:|---:|
| Static module | 42.1 | 0.704x |
| JIT | **59.94** | **1.000x** |

The static module at 1x with no AA is 42.8 FPS, which confirms the outdoor
section is CPU-limited; changing GPU settings does not recover it.

## Download

`SpongeBobRecomp-v0.1.3-Windows-x64.zip` (about 28.8 MB).

SHA-256:

```text
80F71165773E6333F4370D14A8B3C680D4E8FEED38657C1DA078A15A6AECEE63  SpongeBobRecomp-v0.1.3-Windows-x64.zip
```
