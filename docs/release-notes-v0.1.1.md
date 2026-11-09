# SpongeBobRecomp v0.1.1

Patch release for the fullscreen and shutdown fixes.

## Fixed

- **Start in fullscreen now applies.** The Windows NoGUI platform previously
  created the window and ignored the fullscreen setting. It now enters
  borderless fullscreen during startup, using the monitor's full resolution.
- **No more "Session failed" after closing a fullscreen game.** Closing a
  fullscreen window could deliver a focus-loss message after Dolphin's Config
  layers had already been destroyed, causing an access violation
  (`0xC000041D`). Window callbacks now skip configuration writes once the
  platform has stopped, and the window leaves fullscreen before it is
  destroyed.
- **Removed the white frame around the fullscreen game.** The window was
  created with a client edge and a white background brush; both are removed
  in fullscreen now, so the client area is exactly the monitor size. The
  windowed client edge is restored when leaving fullscreen.
- The runner now writes the applied video settings to the log at startup:

  ```
  [video] backend=Vulkan scale=4 msaa=4 ssaa=0 af=4 vsync=1 aspect=1 widescreen=0 fullscreen=1
  ```

  This makes it possible to confirm that the launcher settings reached the
  game. Graphics changes are applied on the next Play, not while the game is
  already running.

## Package

`SpongeBobRecomp-Release.zip` (Windows x64, ~28 MB). No game data is
included; you must supply your own original NTSC-U disc image (ISO or RVZ).

SHA-256:

```
02B7EB0A671B8BD3B654893EAA7A9131727456AC7A023CB0F8469C43FA9BAB92  SpongeBobRecomp-Release.zip
```

## Verified

- Start in fullscreen: game window covers the monitor (`0,0,2560x1440` at the
  tested resolution) and reports `fullscreen=1`.
- Fullscreen startup, close: exit code `0`, no crash dump.
- Windowed startup, F11 to fullscreen, close: exit code `0`, no crash dump.
- Launcher `--play` fullscreen session, close: launcher exits `0`, no
  "Session failed" dialog.
- The clean release zip contains no `Game/`, ISO, RVZ, DOL, save or texture
  data.
