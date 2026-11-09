# Fullscreen, window border and shutdown fixes (v0.1.1)

These are the runtime changes behind the v0.1.1 patch. The source lives in the
ModernGekko/Dolphin-derived runtime; the release package contains the rebuilt
`SpongeBobRecompRunner.exe`.

## Files

- `lib/ModernGekko-Template/lib/ModernGekko/vendor/dolphin/Source/Core/DolphinNoGUI/PlatformWin32.cpp`
- `lib/ModernGekko-Template/lib/ModernGekko/src/runtime/dolphin_runtime.cpp`

## Start in fullscreen

`PlatformWin32::Init()` previously checked `MAIN_FULLSCREEN` but only called
`ProcessEvents()`; it never entered fullscreen. It now calls
`ToggleFullscreen()` after the render window and menus are created.

`ToggleFullscreen()` now saves and restores the extended window style as well
as the normal style, and removes `WS_EX_CLIENTEDGE` while fullscreen:

```cpp
m_windowed_ex_style = GetWindowLongPtr(m_hwnd, GWL_EXSTYLE);
SetWindowLongPtr(m_hwnd, GWL_EXSTYLE,
                 m_windowed_ex_style & ~WS_EX_CLIENTEDGE);
```

The window class background brush changed from the white `COLOR_WINDOW` brush
to `BLACK_BRUSH`, so no bright frame or flash remains around the Vulkan
surface. The client area is now exactly the monitor size.

## Shutdown crash

Closing a fullscreen window could deliver `WM_KILLFOCUS` while
`Core::Shutdown` was already tearing down the Config layers. The handler called
`Config::SetCurrent(MAIN_EMULATION_SPEED, 1.0f)` on a destroyed config, which
produced an access violation and the launcher's "Session failed" dialog
(`0xC000041D`).

The window procedure now returns early if the platform pointer is missing, and
all configuration-changing handlers (`WM_KEYDOWN`, `WM_KEYUP`,
`WM_KILLFOCUS`, `WM_INITMENUPOPUP`, `WM_COMMAND`) check
`platform->IsRunning()` first. The platform destructor also leaves fullscreen
before `DestroyWindow()`.

## Verification

- Fullscreen launch: window and client area `0,0,2560,1440` on a 2560x1440
  monitor, `fullscreen=1` in the `[video]` log line.
- Outer 6 px frame scan of a fullscreen capture: no near-white pixels.
- Fullscreen launch -> close: exit code `0`, no crash dump.
- Windowed -> F11 -> close: exit code `0`, no crash dump.
- Launcher `--play` -> fullscreen -> close: launcher exits `0`.

## Applied video settings log

The runner now prints the values it actually applied:

```text
[video] backend=Vulkan scale=4 msaa=4 ssaa=0 af=4 vsync=1 aspect=1 widescreen=0 fullscreen=1
```

This line is written at startup. Graphics option changes are applied on the
next Play, not while a game session is already running.
