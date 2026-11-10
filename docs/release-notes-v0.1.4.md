# SpongeBobRecomp v0.1.4

Fixes the fullscreen ALT+F4 close error. No game data is included.

## Fixed

- **Fullscreen close no longer hangs or crashes.** Closing a fullscreen session
  with ALT+F4 could hang and then exit with `0xC0000005` (access violation) in
  `VKGfx::BindBackbuffer`: a swap-chain recreation had cleared the current
  image, but `IsCurrentImageValid()` still returned true, so the next present
  wrote through a null texture.
- **Fullscreen is applied after the graphics backend is ready.** The runner
  creates its window windowed, lets the video backend initialize, then switches
  the same window to borderless fullscreen. The runtime keeps its normal
  windowed shutdown path, which is the same model the Rocket Power recomp uses.
- **Swap-chain data is validated before every present.** The current image
  index, texture and framebuffer are checked; a failed resize or surface
  recreation now logs an error and skips the frame instead of dereferencing a
  null image or opening a modal warning dialog that blocks shutdown.
- **One close is enough.** If the emulated game does not handle the
  power-button event, the runner waits up to 3 seconds and then exits instead
  of requiring a second ALT+F4.
- **F11 / Alt+Enter still toggles fullscreen.** Leaving fullscreen restores the
  previous windowed size and style; entering it again uses the monitor size.
  Windowed mode is unchanged.

## Unchanged

- JIT is the default playable core; the static DolRecomp module is included and
  selectable.
- 60 FPS cap, RecompLauncher Level 3 manifest with 13 settings, distinct
  launcher and runner icons, and saves/logs in the same folders.
- No game data in the package.

## Verified

At 2560x1440, internal scale 4x, MSAA 8x, widescreen, Vulkan, JIT:

| Scenario | Result |
|---|---|
| Fullscreen startup, one close | clean exit |
| Fullscreen + loaded gameplay state, one close | clean exit |
| F11 leave -> F11 re-enter -> close | clean exit |
| Windowed close | clean exit |
| Fullscreen double-close | clean exit |
| New crash dumps | none |

The window reports `0,0,2560,1440` in fullscreen and returns to the previous
windowed rectangle after F11.

## Download

`SpongeBobRecomp-v0.1.4-Windows-x64.zip` (about 28.8 MB).

SHA-256:

```text
6F22280B185ADC580A048A7DE5B5E80A3236175BE4C3080EAF7A41A69EFAEA37  SpongeBobRecomp-v0.1.4-Windows-x64.zip
```
