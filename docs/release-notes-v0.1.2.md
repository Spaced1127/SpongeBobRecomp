# SpongeBobRecomp v0.1.2

Adds **RecompLauncher** support and ships the SDK manifest in the release.

## RecompLauncher

`SpongeBobRecomp-v0.1.2-Windows-x64.zip` now contains `recomplauncher.json` at
the top, next to `SpongeBobRecomp.exe`.

- **Level 1 - plays from RecompLauncher.** RecompLauncher asks for the USA
  GameCube ISO (`GSQE78`), checks the full image, runs the setup step and then
  starts the game directly.
- **Level 2 - settings in the launcher.** Window mode, internal resolution,
  frame rate, MSAA, SSAA, anisotropic filtering, VSync, aspect ratio,
  widescreen hack, graphics backend, FPS in the title bar, mute and volume are
  shown on the game's page. They are written to the same
  `%LOCALAPPDATA%\SpongeBobRecomp\config.ini` the app uses.
- **Level 3 - full setup.** The setup step extracts the disc without opening a
  window and prints `progress <0-1> <text>` lines. The manifest includes the
  Redump USA dump (size `1459978240`, CRC-32 `f2facf74`) for the verified
  badge.

## How it runs

- **Prepare:** `SpongeBobRecomp.exe --extract {game}` extracts the disc to
  `Game/` next to the executable and writes `default-game.txt`.
- **Start:** `SpongeBobRecompRunner.exe --module {install}/gGSQE78_recomp.dll
  --user-dir {local}/SpongeBobRecomp`. This skips the custom launcher and boots
  the game directly.
- **Controller:** the runner detects the first SDL gamepad and writes the same
  `GCPadNew.ini` profile the custom launcher would, so a fresh RecompLauncher
  install is controller-ready.
- **Settings:** `%LOCALAPPDATA%\SpongeBobRecomp\config.ini`; the runner reads
  the values on Play.
- **Saves:** `%LOCALAPPDATA%\SpongeBobRecomp\GC` (memory card),
  `%LOCALAPPDATA%\SpongeBobRecomp\StateSaves`, and `config.ini`.
- **Logs:** `%LOCALAPPDATA%\SpongeBobRecomp\Logs`.

The package still contains no game data. You must supply your own disc image.

## Notes

- GameCube discs are not ISO 9660, and the RecompLauncher SDK's checks cover
  `file`, `xdvdfs` and `iso9660` only. The manifest therefore has no `check`;
  it relies on the Redump CRC-32 in `game.dumps` and the setup step's disc-ID
  and retail-DOL validation. The player picks the ISO manually.
- The RecompLauncher entry advertises an ISO. RVZ remains supported by the
  custom launcher; the extractor itself also understands RVZ.
- This is a Windows x64 release; there is no AppImage.

## Download

`SpongeBobRecomp-v0.1.2-Windows-x64.zip` (about 28 MB).

SHA-256:

```text
D9C8CE801ACE8C298044C622C20999DB06346802DC3B4287C86E7B21D8A70764  SpongeBobRecomp-v0.1.2-Windows-x64.zip
```
