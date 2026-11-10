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

## v0.1.4: delayed fullscreen and swap-chain hardening

The v0.1.1 fix was not the end of the story. Closing a fullscreen session with
ALT+F4 could still hang and then fail with an access violation
(`0xC0000005`) instead of the old callback exception. The crash dump showed:

- `VKGfx::BindBackbuffer` writing to `[rcx+0x40]` with `rcx = 0`.
- `SwapChain::m_swap_chain_images[index].texture` was null after a swap-chain
  recreation had cleared the images, but `IsCurrentImageValid()` still
  returned true.
- A failed `RecreateSwapChain()` opened a modal "Warning" dialog, so the
  process sat in a hidden message box instead of exiting.

The v0.1.4 model:

1. Create the window **windowed** and let `VideoBackend::Initialize()` create
   the swap chain against that window.
2. Apply borderless fullscreen on the **first main-loop iteration**, after the
   video backend is ready. The runtime does not use an exclusive display mode.
3. Do not call `ToggleFullscreen()` in `~PlatformWin32()`; destroy the
   borderless window directly.
4. Validate the current swap-chain image (index, texture, framebuffer) before
   every present, and log/skip a failed recreation instead of dereferencing a
   null image or opening a panic dialog.
5. Give the emulated game 3 seconds to handle the power-button event, then
   force the stop; one close is enough even when the game has no STM hook.

This is the same approach the Rocket Power recomp uses: fullscreen belongs to
the window, and the runtime keeps its normal windowed shutdown path.

## Verification

- Fullscreen launch: window and client area `0,0,2560,1440` on a 2560x1440
  monitor, `fullscreen=1` in the `[video]` log line.
- Outer 6 px frame scan of a fullscreen capture: no near-white pixels.
- Fullscreen launch -> close: exit code `0`, no crash dump.
- Windowed -> F11 -> close: exit code `0`, no crash dump.
- Launcher `--play` -> fullscreen -> close: launcher exits `0`.
- v0.1.4: fullscreen single close, loaded-state close, F11 leave/re-enter and
  close, windowed close, and fullscreen double-close all exit cleanly at
  2560x1440/scale=4/MSAA 8x; no new crash dumps.

## Applied video settings log

The runner now prints the values it actually applied:

```text
[video] backend=Vulkan scale=4 msaa=4 ssaa=0 af=4 vsync=1 aspect=1 widescreen=0 fullscreen=1
```

This line is written at startup. Graphics option changes are applied on the
next Play, not while a game session is already running.
