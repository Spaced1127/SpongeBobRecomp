# Project state

Updated: 2026-11-16

## Working rules in force

- **Quiet mode is LIFTED** (user directive, 2026-11-16). Do not use
  `H:\Orchestration\tools\run-hidden.ps1`; launch test apps normally with
  visible windows. Do not minimise, move, hide or kill test-app windows, and do
  not re-introduce window-suppression scripts or daemons. A run that is
  disruptive is the user's call to stop, not ours to hide. Everything below
  that says "hidden desktop" describes how the evidence was captured before
  this directive.
- **GUI/TEST LAUNCHES ARE PAUSED** (hub directive, 2026-11-16, effective now).
  The user is on the machine. Do not launch the launcher, the runner, a game,
  or any window, visible or hidden, and do not start a test cycle until the hub
  lifts the pause. Host-side work only: code, analysis, builds that produce no
  window, docs. Verified at pause time: no SpongeBob/Rocket Power/ModernGekko
  process was left running by this session.

### Blocked next actions (need the pause lifted)

1. **In-game memory card round trip** (v0.1.7, ~2 minutes):
   launch `dist/SpongeBobRecomp-Release-v0.1.7/SpongeBobRecompRunner.exe`
   (or the installed app), check the log line
   `memory card: slot A = raw, slot B = none, ...`; Options -> Save Game to a
   new slot; close the game normally (not task manager); relaunch;
   Options -> Load Game -> slot A must list and load the save. Report the
   `MemoryCardA.USA.raw` size (16,777,216) and, if it fails, the card SHA-256.
2. **Hardware pad confirmation** for the v0.1.7 controller fix: Xbox 360 /
   One / Series, Elite S1/S2, DualSense, DualSense Edge, 8BitDo Pro 2
   (Nintendo + standard), Ultimate, 64, Switch Pro. Collect the
   `controller:` and `controller configuration:` lines from any that misbehave.
3. Re-run `moderngekko_controller_layout_test.exe` (console only, no window) if
   the shared tree changes again before the next release.

## Latest verified result

The standalone PC app runs the real game end to end:

- Asset-free launcher, runner and recompiled module (no disc data).
- Built-in ISO and RVZ import; RVZ is read natively, and ISO/RVZ extraction
  produces the same 343-file tree (`78BD825A...59B6`) and `main.dol`
  (`dca4f72b...e009`).
- Actual levels load: bedroom intro with dialogue, pants pickup, bedroom ->
  living room transition, full HUD, Gary NPC, all at ~60 fps.
- Pause menu, Options, Save Game, Load Game and the memory card all work:
  `78-GSQE-SpongeBob RFD.gci` is written and read back by the game.
- Intro/logo movies now run at **1.00x** (previously 0.41x) with continuous
  48 kHz audio; the fix is cross-chunk direct calls in the C generator.
- Gameplay: 59.7 fps / 0.995 (PGO + x86-64-v3 module).
- Graphical launcher: PLAY / GRAPHICS / PERFORMANCE / AUDIO / CONTROLLER pages,
  animated underwater backdrop, custom fonts, all options persisted.
- Audio mute + master volume in the launcher; mute reaches the backend
  (`MAIN_AUDIO_MUTED`, volume 0). Unlock-frame-rate toggle on PERFORMANCE.
- Release: `dist/SpongeBobRecomp-Release.zip`, no game data.

Open verification item: automated input did not cover the main menu's
flower-mat interaction. The game itself is unchanged; levels, pause/save menus
and the memory card work normally. A human playthrough should exercise the
menu path and the full story.

Evidence: `work/evidence/20..24-*.png`, `docs/notes/05-test-log.md`,
`docs/notes/07-performance.md`.

## Fullscreen close fix (2026-11-09)

Closing a fullscreen session with ALT+F4 could hang and then exit with
`0xC0000005` (access violation). It was not the v0.1.1 window-proc config bug;
that one was `0xC000041D` and remains fixed.

Crash evidence from WER and minidumps (`SpongeBobRecompRunner.exe.223320.dmp`
and `.226984.dmp`):

- Faulting module: `SpongeBobRecompRunner.exe`, RVA `0x2ffd00`.
- Instruction: `mov dword ptr [rcx+0x40], edx` with `rcx = 0`; exception
  information `[1, 0x40]` (write to address `0x40`).
- Thread: `CPU-GPU thread` (single-core mode).
- Stack: `VKGfx::BindBackbuffer` -> `Presenter::Present` -> `ViSwap` ->
  `Video_OutputXFB` -> `VideoInterface::OutputField`/`Update`.
- The null pointer was `SwapChain::m_swap_chain_images[index].texture`: a
  swap-chain recreation had cleared the images, but
  `SwapChain::IsCurrentImageValid()` still returned true. The subsequent
  present wrote through the null texture.

A failed `RecreateSwapChain()` also called `PanicAlertFmt("Failed to
re-configure swap chain images, this is fatal (for now)")`. During a close that
opened a modal "Warning" dialog (confirmed by enumerating the process windows),
so the process sat in a hidden message box instead of exiting.

Fix (ModernGekko/Dolphin runtime):

- `PlatformWin32::Init()` creates the window windowed and defers fullscreen to
  the first `MainLoop` iteration, after `VideoBackend::Initialize()`. The
  window is borderless fullscreen, not an exclusive display mode.
- `~PlatformWin32()` no longer calls `ToggleFullscreen()` before
  `DestroyWindow()`. Destroying the borderless window directly avoids the
  `WM_SIZE` -> swap-chain recreation during teardown.
- `SwapChain::IsCurrentImageValid()` now checks the image index, texture and
  framebuffer; the current-image getters return null/`VK_NULL_HANDLE` when
  invalid; `DestroySwapChainImages()` clears the validity flag; and
  `AcquireNextImage()` refuses a null swap chain.
- `VKGfx::BindBackbuffer()` caches and checks the current texture/framebuffer
  before use. `CheckForSurfaceResize()`/`CheckForSurfaceChange()` honor a
  failed recreation.
- Swap-chain recreation failures now log an error and skip the frame instead
  of opening a blocking panic dialog.
- `Platform::UpdateRunningFlag()` gives the game 3 seconds to honor the
  power-button event, then clears `m_running`; one close is enough even when
  the game does not install the STM event hook.

This is the same principle as the Rocket Power recomp: do not let the runtime's
built-in fullscreen teardown own the window-close path.

The first v0.1.4 build still intermittently hung on close. The CPU thread could
enter a long frame-pacing sleep in `Presenter::Present` while `CPU::Stop` was
waiting for it to acknowledge `PowerDown`. `Present.cpp` now skips
`CoreTiming::SleepUntil()` when `Core::IsRunning()` is false. An 8-second
shutdown watchdog also force-exits if a Vulkan/shader/driver wait blocks a
processed close. Stress test: 10/10 packaged fullscreen closes, 0.5-0.8 s each,
no new crash dumps. The v0.1.5 release contains this final fix.

Verified with the patched runner at 2560x1440, scale=4, MSAA 8x, widescreen,
Vulkan, JIT:

| Scenario | Result |
|---|---|
| Fullscreen startup, one close | window `0,0,2560,1440`; clean exit |
| Fullscreen + loaded gameplay state, one close | clean exit |
| F11 leave -> F11 re-enter -> close | `182,182,1738,1116` -> `0,0,2560,1440`; clean exit |
| Windowed close | clean exit |
| Fullscreen double-close | clean exit |
| New crash dumps | none |

## Controller layouts (2026-11-14)

RecompLauncher starts the runner directly and never opens the custom launcher,
so controller selection cannot live only in the launcher UI. The runner now
owns it:

- The runner enumerates SDL gamepads at startup, reads
  `SDL_GetGamepadTypeForID` (with a product-name fallback) and writes
  `GCPadNew.ini` with the Xbox, PlayStation, Switch or generic layout.
- Switch uses the printed A/B/X/Y labels (`Button B`, `Button A`, `Button Y`,
  `Button X` in the profile); Xbox, PlayStation and generic use physical
  positions.
- `controller_profile=auto` regenerates the profile on every launch, replacing
  a stale device or positional layout. `manual` preserves a custom launcher
  selection. `xbox`, `playstation`, `switch` and `generic` force a layout.
- The custom launcher's controller page detects the selected pad's type,
  writes the matching layout and sets `controller_profile=manual`.
- RecompLauncher's manifest now has 14 settings, including **Controller
  layout** (Auto-detect / Xbox / PlayStation / Switch / Generic).
- Controller enumeration initializes only `SDL_INIT_GAMEPAD|SDL_INIT_JOYSTICK`;
  initializing SDL video before the platform window changed the window
  geometry and left the fullscreen window offset.
- Fullscreen placement now waits about one second after the main loop starts,
  so the borderless window lands at `0,0,2560,1440` instead of keeping the
  default windowed offset.

Verified on the packaged v0.1.5 build:

- Auto with the connected Xbox pad: `Device = SDL/0/Xbox One Controller`,
  `(xbox layout)`.
- Explicit `switch`: `Buttons/A=Button B`, `B=Button A`, `X=Button Y`,
  `Y=Button X`.
- Stale `auto` profile: Old Pad replaced with the connected device and layout.
- `manual`: existing profile preserved.
- Packaged fullscreen: `0,0,2560,1440`, fullscreen style, menu removed, clean
  close.

v0.1.5 asset: `SpongeBobRecomp-v0.1.5-Windows-x64.zip`, 28,803,228 bytes,
SHA-256 `1A0CEBD909F4D522D1FC376F445EBBD3CC1A63634959432074B28AF759E81F31`.

Published 2026-11-15 as the latest GitHub release:
<https://github.com/Spaced1127/SpongeBobRecomp/releases/tag/v0.1.5>
Release commit `d1634a5` (main), guide commit `ec95be6`. Download-back hash,
14-setting manifest and no-game-data scan all verified.

## Native RVZ (2026-11-15)

Players can use a Dolphin `.rvz` directly; no RVZ→ISO step. RVZ is detected
by magic `RVZ\x01`, and `tools/rvz_extract.py` exposes a random-access ISO view
that decompresses zstd groups on demand. `tools/gcdisc.py` and
`tools/verify_dol.py` use it; the custom launcher and RecompLauncher path use
Dolphin DiscIO.

Evidence with the project RVZ (`974260E4...B06E80`, 489,157,208 bytes):

- RVZ → ISO export: ISO SHA-256
  `FFDEB4FD370CB357A5F110D3E77C3E8BE7DB5A395818480C4308A1B820039A5D`,
  identical to `work/disc/game.iso`.
- Launcher `--extract` ISO vs RVZ: 343 files, 604,947,746 bytes, tree SHA-256
  `78BD825AF9DD03818984D7E06F945C40DB949AEAB369039FF5A4C62BD37159B6`
  identical.
- `gcdisc.py extract` ISO vs RVZ: same tree hash; 338 FST files plus 5
  system files.
- `sys/main.dol`
  `DCA4F72B57E8BF3F540E694F01CC23EF687D2B25028D974B67356E15F1C2E009`;
  `sys/fst.bin`
  `A957E4F067711256F9C7161256CCD7E02BD2ED201C5C656736CE79894DFDF529`.
- RecompLauncher manifest: `check.ids ["GSQE78"]`, label `.iso or .rvz`,
  14 settings, valid against the live schema.
- RecompLauncher source confirms the gate: `profile.rs` accepts a compressed
  image only when `game.label` names `.rvz`, and `roms.rs` reads the GameCube
  ID from RVZ offset 0x58. The project RVZ returns `GSQE78` at that offset.

Deployment note: the published v0.1.5 zip still carries the old `.iso`-only
manifest. RecompLauncher installs from that zip, so the v0.1.6 release carries
this manifest; the repo-root manifest is also updated.

Published 2026-11-15 as v0.1.6 (latest):
<https://github.com/Spaced1127/SpongeBobRecomp/releases/tag/v0.1.6>
Asset: `SpongeBobRecomp-v0.1.6-Windows-x64.zip`, 28,810,819 bytes, SHA-256
`581CF8F0E14B80F8C8F429E8D40FF5365742AA3870658FF58E615688DB3B0413`.
Release commit `29fae2d`, guide commit `320b5c8`. Download-back hash,
14-setting manifest, no-game-data scan and packaged boot smoke (`booted=1`)
verified. v0.1.5 is superseded.

## Special controllers (2026-11-15)

GUID-first detection lives in `tools/controller_guid.hpp` and
`tools/controller_layout.hpp`. The table keys on SDL standard-form VID/PID, not
product names, so USB, Bluetooth and XInput variants resolve the same way.

| Family | VID:PID | Layout | Extra buttons |
|---|---|---|---|
| DualSense Edge | `054c:0df2` | PlayStation | paddles/Fn unbound |
| Xbox Elite Series 1 | `045e:02e3` | Xbox | paddles unbound |
| Xbox Elite Series 2 | `045e:0b00`, `0b05`, `0b22` | Xbox | paddles unbound |
| 8BitDo Pro 2 (Nintendo/Switch mode) | live SDL `a`/`b` mapping | Switch | paddles unbound |
| 8BitDo Ultimate / 64 | live SDL `a`/`b` mapping | standard | - |

- Standard DualSense (`054c:0ce6`), DualShock 4/3, Xbox 360/One/Series and
  Switch Pro/Joy-Con stay in the table. SDL's database-backed type is the
  fallback; there is no product-name matching.
- Edge/Elite use the same `ControllerLayout` as a standard DualSense/Xbox pad,
  so `GenerateControllerConfig` emits the same `GCPadNew.ini` bindings.
- Live SDL mappings are read with `SDL_GetGamepadMappingForID`. A Nintendo-style
  mapping (`a` button index > `b`) selects the printed-label Switch layout;
  `Ultimate` and `64` report `a:b0,b:b1` and stay standard. A reversed D-pad
  (`dpleft` index > `dpright`, or reversed hat/axis) sets `dpad_swap`, and the
  generated profile writes corrected `D-Pad/Left`/`D-Pad/Right`.
- Startup line for support:
  `controller: "<name>" guid=<32 hex> bus=<...> vid=<...> pid=<...>
  layout=<...> source=<guid|mapping|type> dpad_swap=<yes|no>
  face_swap=<yes|no> [paddles=unbound] [extras=unbound] [family="..."]`
- Offline test `moderngekko_controller_layout_test.exe`: 62 PASS, 0 FAIL.
  Covers Edge USB/Bluetooth, Elite 02E3/0B00/0B05/0B22, all four 8BitDo Pro 2
  Nintendo GUIDs, Pro 2 Switch-mode, Ultimate/64 standard, a synthetic reversed
  D-pad, profile migration/custom preservation and standard-pad regression.
- SDL DB evidence `work/verify-controller/check_sdl_db.py`: Edge USB/BT
  standard actions equal standard DualSense; Elite USB/BT have every standard
  Xbox action. 8BitDo Pro 2 Nintendo entries report `a:b1,b:b0`; Ultimate/64
  report `a:b0,b:b1`.
- Hardware confirmation is unavailable here (the current host reports 0 SDL
  gamepads). Players should confirm face buttons, both sticks, triggers,
  shoulders, D-pad and Start; send the `controller:` line if anything is wrong.

## Controller hotfix, Xbox reports (2026-11-16)

Players on v0.1.6 reported Xbox pads not working. The detection/generation walk
against the vendored SDL DB found no Microsoft row that changed layout: every
Xbox 360/One/Series/Elite GUID still resolves `xbox` and the generated
`GCPadNew.ini` is **byte-identical** to the v0.1.5/v0.1.6 profile. What broke
were two live-mapping heuristics that v0.1.6 applied to **every** pad and to
pads the GUID table does not cover:

- `a` index > `b` index selected the Switch layout unconditionally, even over a
  GUID or SDL-type verdict. Of the 797 vendored DB rows, 110 became "Switch"
  (printed-label A/B and X/Y swapped) — the "USB Gamepad", PS2-adapter, Steam
  virtual-pad and third-party Xbox-shape rows that Windows and Steam present in
  place of a plain Xbox pad.
- `dpleft` index > `dpright` set `dpad_swap` for button-order D-pads that SDL
  already had right (DualShock 3, PS2 adapters, Steam pads): 34 rows got an
  inverted D-pad.
- A Microsoft PID missing from the table (`0B20`, `0B2A`, `0B30`, ...) had no
  fallback, so it depended on those heuristics.

Fix (`controller_layout.hpp`, `moderngekko_run.cpp`):

- Vendor-family fallback on the standard-form GUID: `045E` -> Xbox,
  `054C` -> PlayStation, `057E` -> Switch, reported as `source=guid-family`.
  Every Xbox PID now resolves `xbox` whatever PID/firmware/driver it uses.
- The Nintendo mapping rule requires a Nintendo signal (8BitDo vendor `2DC8`,
  SDL's `SDL_GAMECONTROLLER_USE_BUTTON_LABELS` hint, or paddles) and never
  overrides a GUID/Xbox/PlayStation verdict.
- A button-order D-pad is never read as reversed; only a reversed hat/axis
  sets `dpad_swap` (the 8BitDo case).
- The runner now sets Dolphin's own SDL hints (WGI=0, DIRECTINPUT=1,
  ENHANCED_REPORTS, HIDAPI COMBINE/VERTICAL Joy-Con, PS5 player LED) before it
  enumerates, so the `Device = SDL/...` line it writes matches the device the
  runtime creates. Keep that list identical to
  `InputCommon/ControllerInterface/SDL/SDL.cpp`.
- Support lines now carry the device and the profile path:
  `controller configuration: 1 GameCube controller mapped (xbox layout)
  device="SDL/0/Xbox 360 Controller" profile=...\Config\GCPadNew.ini`, next to
  the existing `controller: "<name>" guid=... layout=... dpad_swap=...
  face_swap=...`.

Verification: `moderngekko_controller_layout_test.exe` **130 PASS, 0 FAIL**
(34-row real-DB matrix, byte-identity lock on the Xbox profile, unknown-PID
fallback, non-8BitDo `a>b`, button D-pad); `check_regression.py`:
150/797 rows change behaviour (20 Nintendo pads now correct, 110 wrong Switch
layouts gone, 34 D-pads fixed). Hidden-desktop boot with a seeded Xbox profile
and 0 SDL pads leaves the profile byte-identical. Hardware confirmation still
unavailable on this host (0 SDL gamepads).

Published 2026-11-17 as v0.1.8 (latest):
<https://github.com/Spaced1127/SpongeBobRecomp/releases/tag/v0.1.8>

| Item | Value |
|---|---|
| release commit | see `gh-release` tag v0.1.8 |
| folder | `dist/SpongeBobRecomp-Release-v0.1.8` (2,639 files, 100,983,184 bytes) |
| zip | `SpongeBobRecomp-v0.1.8-Windows-x64.zip` (28,817,632 bytes) |
| SHA-256 | `1DEB607039EC229DD49A9E3D2E362B1C1DC5DA00ABB0A94F35E2C05BAD00CA07` |
| runner | `78B93ED523C01B18F4BFD451405C05CE1AEA8C1F31B431FA91DB99505D9925A1` |
| canonical profile | `035B949038F3A2F8BA86734DA92EB9AB32812856C2E71E40879686EFC99B2A83` |
| game-data scan | 0 hits |

Packaged boot (visible window, real Xbox One pad): `booted=1`,
`vps=59.9401`, canonical profile written, raw memory card created, clean
`stop` shutdown.

## Controller hotfix, Xbox reports (2026-11-16)

Players on v0.1.6 reported Xbox pads not working. The detection/generation walk
against the vendored SDL DB found no Microsoft row that changed layout: every
Xbox 360/One/Series/Elite GUID still resolves `xbox` and the generated
`GCPadNew.ini` is **byte-identical** to the v0.1.5/v0.1.6 profile. What broke
were two live-mapping heuristics that v0.1.6 applied to **every** pad and to
pads the GUID table does not cover:

- `a` index > `b` index selected the Switch layout unconditionally, even over a
  GUID or SDL-type verdict. Of the 797 vendored DB rows, 110 became "Switch"
  (printed-label A/B and X/Y swapped) — the "USB Gamepad", PS2-adapter, Steam
  virtual-pad and third-party Xbox-shape rows that Windows and Steam present in
  place of a plain Xbox pad.
- `dpleft` index > `dpright` set `dpad_swap` for button-order D-pads that SDL
  already had right (DualShock 3, PS2 adapters, Steam pads): 34 rows got an
  inverted D-pad.
- A Microsoft PID missing from the table (`0B20`, `0B2A`, `0B30`, ...) had no
  fallback, so it depended on those heuristics.

Fix (`controller_layout.hpp`, `moderngekko_run.cpp`):

- Vendor-family fallback on the standard-form GUID: `045E` -> Xbox,
  `054C` -> PlayStation, `057E` -> Switch, reported as `source=guid-family`.
  Every Xbox PID now resolves `xbox` whatever PID/firmware/driver it uses.
- The Nintendo mapping rule requires a Nintendo signal (8BitDo vendor `2DC8`,
  SDL's `SDL_GAMECONTROLLER_USE_BUTTON_LABELS` hint, or paddles) and never
  overrides a GUID/Xbox/PlayStation verdict.
- A button-order D-pad is never read as reversed; only a reversed hat/axis
  sets `dpad_swap` (the 8BitDo case).
- The runner now sets Dolphin's own SDL hints (WGI=0, DIRECTINPUT=1,
  ENHANCED_REPORTS, HIDAPI COMBINE/VERTICAL Joy-Con, PS5 player LED) before it
  enumerates, so the `Device = SDL/...` line it writes matches the device the
  runtime creates. Keep that list identical to
  `InputCommon/ControllerInterface/SDL/SDL.cpp`.
- Support lines now carry the device and the profile path:
  `controller configuration: 1 GameCube controller mapped (xbox layout)
  device="SDL/0/Xbox 360 Controller" profile=...\Config\GCPadNew.ini`, next to
  the existing `controller: "<name>" guid=... layout=... dpad_swap=...
  face_swap=...`.

Verification: `moderngekko_controller_layout_test.exe` **130 PASS, 0 FAIL**
(34-row real-DB matrix, byte-identity lock on the Xbox profile, unknown-PID
fallback, non-8BitDo `a>b`, button D-pad); `check_regression.py`:
150/797 rows change behaviour (20 Nintendo pads now correct, 110 wrong Switch
layouts gone, 34 D-pads fixed). Hidden-desktop boot with a seeded Xbox profile
and 0 SDL pads leaves the profile byte-identical. Hardware confirmation still
unavailable on this host (0 SDL gamepads).

Published 2026-11-16 as v0.1.7 (latest):
<https://github.com/Spaced1127/SpongeBobRecomp/releases/tag/v0.1.7>

| Item | Value |
|---|---|
| release commit | `46bc372` (main) |
| tag | `v0.1.7` |
| folder | `dist/SpongeBobRecomp-Release-v0.1.7` (2,639 files, 100,993,650 bytes) |
| zip | `SpongeBobRecomp-v0.1.7-Windows-x64.zip` (28,823,888 bytes) |
| SHA-256 | `D6660377F5D3B15A38F7BA0E414E990E90C0C23CE954FDD23513D9F5C3E1BC0E` |
| runner | `263C4AD6D384FB198A833AC567B450C4292068587B01FFFADB9483DEE019BEDB` (15,835,648 bytes) |
| launcher | `CD03A4DDD8C0F2EAB58CC34DB5ADA950B6598C0E6B89199EDA2BD6D0DCA785F7` |
| SHA256SUMS.txt | published beside the zip (106 bytes) |
| game-data scan | 0 hits |
| download-back hash | identical to the uploaded asset |

Packaged boot smoke (hidden desktop, before the quiet-mode lift):
`--game work\game --automation-dir <dir>` -> `status.txt` `booted=1`,
`vps=59.9268`, `speed=1.00033`, raw memory card created. A second run with the
automation `stop` command exited on its own (clean card flush).

Shared-tree warning: `H:\Projects\Agressive Inline Static Recompile\lib\
ModernGekko` is a junction to this tree's
`lib\ModernGekko-Template\lib\ModernGekko`, and that project's session edited
`controller_layout.hpp` / `moderngekko_run.cpp` during this hotfix (SDL hint
list, button D-pad rule). Rebuild and re-run the layout test before packaging
any release built from this tree.

## Memory card fix (2026-11-16)

Shared pattern from Aggressive Inline, applied here. v0.1.0-v0.1.6 never wrote
`SlotA`, so Dolphin's default `MemoryCardFolder` (8) was used and saves landed
in `GC/<region>/Card A/*.gci`; `Config/Dolphin.ini` did not exist at all.

- `src/runtime/memcard_bootstrap.cpp` runs after
  `UICommon::SetUserDirectory` + `UICommon::CreateDirectories` and before
  `UICommon::Init`, so `GC/USA` and the card exist before
  `ExpansionInterface::Init`:
  - slot A = raw 128 Mbit card (`MemoryCardA.<region>.raw`, 16,777,216 bytes),
    created and formatted on a fresh install (region from the disc ID);
  - slot B = `None` (255), never `Dummy` (0);
  - both keys are forced into `Config/Dolphin.ini` (`[Core] SlotA`,
    `[Core] SlotB`) on every launch, overwriting rather than inserting;
  - a legacy GCI folder card is imported once into the raw card; the old
    `.gci` files stay as a backup. If the import fails the runtime keeps the
    folder device (SlotA=8) so no player starts with an empty card.
- `dolphin_runtime.cpp` also sets `Config::SetBase(MAIN_SLOT_A/B)` after
  `UICommon::Init` so no other layer can re-enable the folder device.
- RecompLauncher manifest: second config block for
  `{local}/SpongeBobRecomp/Config/Dolphin.ini` with `Core/SlotA = 1` and
  `Core/SlotB = 255` in `ensure`, `always` and `new`.
- Startup line: `memory card: slot A = raw, slot B = none, ...` with the file
  name, byte size or the migration count.

Verified (hidden desktop / headless, this host):

| Case | Result |
|---|---|
| fresh user dir | `created MemoryCardA.USA.raw bytes=16777216`, SHA-256 `81DF7FED...00DA`, `GC/USA` + `EUR` + `JAP` exist, `[Core] SlotA = 1 / SlotB = 255` |
| legacy folder card (`dist/SpongeBobRecomp/UserSave` copy, real `78-GSQE-SpongeBob RFD.gci`) | `migrated 1 save(s)`, card `DA7AA9CA...77B6`, directory entry at `0x4000`: `GSQE78` / company `78` / `SpongeBob RFD` / 8 blocks; `.gci` kept |
| second launch | card SHA unchanged (`DA7AA9CA...77B6`), no re-import, keys intact |
| packaged v0.1.7, fresh dir, hidden desktop, 20 s | raw card 16,777,216 bytes, keys written |

Not verified: an in-game `Save Game` -> `Load Game` round trip on the raw card.
Reaching the game's menu needs scripted input this session did not have; the
last verified save (v0.1.6, folder device) is the fixture that was migrated, so
a human can confirm load in one step (Options -> Load Game -> slot A).

In-game check with the packaged v0.1.7 runner (visible window, paused lifted):
title -> START -> the game enters the bedroom and shows
"Now accessing the Memory Card in Memory Card Slot A. Do not touch the Memory
Card or the POWER Button." and continues normally — the raw card in slot A is
read without the hang or the "device not supported" error that the folder /
Dummy configurations produce. Evidence:
`%TEMP%\opencode\savecheck\shots2\02-menu.png` (access banner) and `04/06-*.png`
(bedroom after access). The pause menu did not open from scripted START during
the scripted intro, so the actual Save/Load menu was not reached.

Test caveats from the pattern doc apply: savestates restore the EXI device type,
so a state made while slot A was the GCI folder re-enables the folder device;
the automation `stop` command must be used instead of a force-kill, because a
force-kill skips the card flush.

Support tool: `python tools\card_report.py "<user dir>"` (also published in the
repo as `tools/card_report.py`) prints the SlotA/SlotB device, the raw card
size and SHA-256, and every save directory entry. It is read-only and launches
nothing. Current fixtures report `slot A = 1`, `slot B = 255`, card
16,777,216 bytes, entry `GSQE`/`78`/`SpongeBob RFD`/8 blocks, and the legacy
`.gci` still present.

## Widescreen and frame pacing (2026-11-16)

Player report relayed from the RecompLauncher page (v0.1.3): "stuttering and
widescreen still doesn't render properly".

### Widescreen: real defect, fixed

The launcher and the RecompLauncher manifest exposed **two independent
controls**: the aspect ratio (`auto/wide/standard/stretch`) and a "Widescreen
hack" checkbox. Picking "16:9 widescreen" without ticking the hack renders the
4:3 image stretched to 16:9 - exactly the report.

Measured with the packaged v0.1.7 runner (visible window, PrintWindow captures
in `work/evidence` style: `%TEMP%\opencode\ws\shots`):

| Setting | Result |
|---|---|
| `standard`, hack off | 4:3 image with side bars; HUD ring 107x116 px (AR 0.92) |
| `wide`, hack off (the reported case) | full 16:9, 3D stretched: HUD ring 142x116 px (1.33x wider), wall pictures become wide rectangles, SpongeBob squashed |
| `wide`, hack on | full 16:9, 3D correct (pictures square, SpongeBob normal, more room visible), HUD ring 142x116 |
| `wide` in `config.ini` with `widescreen_hack=false`, new build | identical to `wide`+hack: log `aspect=1 widescreen=1` |

Fix: the widescreen hack is part of the 16:9 choice.
- `frontend_config.cpp`: `aspect=wide` forces `widescreen_hack=true` when the
  config is parsed; the explicit `stretch` mode is how you ask for a plain
  stretch.
- `moderngekko_launcher.cpp`: choosing "16:9 widescreen" ticks the hack, and
  the checkbox is relabelled "Widescreen hack (correct 3D at 16:9)".
- `recomplauncher.json`: the 16:9 choice sets `aspect=wide` **and**
  `widescreen_hack=true`; the hack help no longer claims it stretches 3D.
- Known limitation, documented: the 2D HUD (screen-space overlays) still
  scales to 16:9, so HUD art is ~1.33x wider at 16:9. `aspect=auto/standard`
  keeps the HUD pixel-correct with side bars; the 3D view is correct either
  way.

### Stutter: not reproducible here

Measured with the packaged runner (visible window, automation `status.txt`
`frame_count`/`speed`, 200 ms resolution):

| Run | Result |
|---|---|
| cold (shader cache deleted) | 59.86 fps average, `speed_min` 0.9961, no frame deficit |
| warm, 25 s walking across the room | 59.97 fps average, 1,493 frames vs 1,492 expected, `speed_min` 1.0000 |

- Shader compilation is not the cause: the runtime already sets
  `GFX_SHADER_COMPILATION_MODE = AsynchronousUberShaders` with the shader cache
  on, and the cold-cache run holds 59.9 fps.
- One real hitch: the START -> bedroom transition (scene load + card access)
  drops ~11 frames (~190 ms), once per transition.
- Environmental candidates for the reporter's machine (RTX 4080 / 9800X3D /
  126 GB, three displays): VRR plus desktop composition, MPO overlays, video
  playing on another display, or the older v0.1.3 build (before the PGO module
  and the audio/animation fixes). Nothing in this build's pacing reproduces it.

## Generic controller system (2026-11-17)

Ported from WWE WrestleMania X8 v0.1.4 (`controller-generic-design.md`). The
per-device tables, launch-time profile generation and migration are gone.

- **One static `GCPadNew.ini`**, written only when missing, never rewritten:
  canonical SDL positional bindings (`Buttons/A = Button A`, ...).
- **Two layout classes**: `positional` (default) and `nintendo` (A<->B, X<->Y
  only; D-pad/sticks/triggers untouched), applied in the input layer by
  `ciface::SDL::ResolveLayoutButton` at button-read time, so the profile text
  never changes.
- **Class resolution** is a pure policy in
  `vendor/dolphin/.../SDL/LayoutClass.h`: override -> SDL gamepad type ->
  explicit 8BitDo pair (`2dc8:6006`, `05ac:0004`). No tables, no mapping
  heuristics.
- **Override** `controller_class = auto|positional|nintendo` in `config.ini`
  wins; `--controller-layout` maps onto it (`xbox`/`playstation` ->
  positional, `switch` -> nintendo). Legacy `controller_profile` and
  `controller` keys stay parseable and are ignored, never fatal.
- **Device resolution without the file**: `EnsurePadBound()` binds the first
  enumerated pad when the configured one is absent (`SetDefaultDevice` +
  `UpdateReferences`), and a 2 s watcher repeats it, so hot-plug works with no
  profile write. The existing ModernGekko `DeviceContainer::FindDevice`
  fallback (exact -> same name -> first SDL pad) stays as the second line of
  defence.
- `tools/controller_layout.hpp` and `tools/controller_guid.hpp` are deleted;
  `GenerateControllerConfig`/`EnsureControllerConfig` and the profile
  migration helpers are removed from `frontend_config`.
- One startup line for triage:
  `controller: name="..." guid=... type=xboxone class=positional override=auto
  device="SDL/0/..." source=sdl profile=static|written`.

Verified offline (`moderngekko_controller_layout_test`): **46 PASS, 0 FAIL** —
23-family class matrix (Xbox 360 USB/BT, One, One S/Series, Elite, unknown-PID
Xbox, DualSense, Edge, DS4, DS3, Sony STANDARD, generic DInput, generic unknown,
8BitDo XInput/Ultimate/Pro 2 Nintendo/SN30 Pro/Switch clone, Switch Pro and all
three Joy-Con), override precedence in both directions, canonical profile text,
write-once and hand-edit preservation, legacy key handling.
`moderngekko_frontend_config_test` passes.

Live (real Xbox One pad on this host, GUID
`0300fa675e040000ff02000000007801`, product 0x02ff, SDL type `xboxone`):

| Run | Startup line | Profile |
|---|---|---|
| `controller_class=auto` | `class=positional override=auto` | `written`, SHA-256 `035B9490...2A83` |
| `controller_class=nintendo` | `class=nintendo override=nintendo` | identical SHA |
| `controller_class=positional` | `class=positional override=positional` | identical SHA |
| second launch, same dir | `profile=static` | identical SHA |

In-game: the packaged runner boots with the pad bound and the raw memory card;
no "configured device missing" line appears because the configured pad is
present. **Hardware validation (2026-11-17)**: the shared input layer is proven on real
hardware - the user tested WWE WrestleMania X8 Recomp v0.1.4 with a physical
Xbox pad and both binding and buttons work. SpongeBob v0.1.8 ships the same code
unchanged. Still open here: per-button confirmation on *this* title (one human
press pass), hot-plug (the pad was never unplugged) and the no-pad-at-boot
branch (a pad has been attached since the port; covered by the offline test).
PlayStation pads keep the positional class they have always used.

## Goal

A standalone, asset-free Windows PC application for the GameCube release of
*SpongeBob SquarePants: Revenge of the Flying Dutchman* (`GSQE78`, USA), with
ISO/RVZ import, configurable graphics and 60 fps gameplay; a Nintendo Switch
homebrew port follows.

## Goal constraint

A native static recompilation cannot produce a byte-identical GameCube DOL:
the output is host code (x86-64 PE/ELF). The retail DOL is preserved
bit-identically and verified; see
[`notes/03-objective-and-identity.md`](notes/03-objective-and-identity.md).

## Confirmed facts

### Disc

- File used: `Nickelodeon SpongeBob SquarePants - Revenge of the Flying Dutchman (USA).rvz`
- RVZ container: v1.00.00, Zstandard level 19, 128 KiB chunks, 11,139 groups.
- ISO size: 1,459,978,240 bytes.
- Game ID: `GSQE78`.
- Title: `SpongeBob SquarePants ROTFD`.
- Country byte: `0x00` (USA).
- GameCube magic at `0x1C`: `0xC2339F3D`.
- DOL offset: `0x1EC00`; FST offset: `0x316000`, size `0x2722`.
- Entry point: `0x80003140`.
- DOL SHA-256: `dca4f72b57e8bf3f540e694f01cc23ef687d2b25028d974b67356e15f1c2e009`.

### DOL sections

| Section | File offset | Virtual range | Size |
|---|---:|---|---:|
| text0 | `0x000100` | `0x80003100`–`0x80005620` | `0x2520` |
| text1 | `0x002620` | `0x8001F2C0`–`0x80299920` | `0x27A660` |
| data0 | `0x27CC80` | `0x80005620`–`0x80015F60` | `0x10940` |
| data1 | `0x28D5C0` | `0x80015F60`–`0x8001F2C0` | `0x9360` |
| data2 | `0x296920` | `0x80299920`–`0x80299980` | `0x60` |
| data3 | `0x296980` | `0x80299980`–`0x802999A0` | `0x20` |
| data4 | `0x2969A0` | `0x802999A0`–`0x802AFBA0` | `0x16200` |
| data5 | `0x2ACBA0` | `0x802AFBA0`–`0x802F3460` | `0x438C0` |
| data6 | `0x2F0460` | `0x80373E40`–`0x80377540` | `0x3700` |
| data7 | `0x2F3B60` | `0x803781C0`–`0x8037B9A0` | `0x37E0` |

- BSS: `0x802F3460` + `0x84D54`.
- `data6` overlaps the BSS range; `data7` begins 12 bytes after BSS ends.
  Keep this in mind when constructing flat memory images.

### Engine and middleware

- **TotemTech Data v1.73**, `(c) 1999–2002 Kalisto Entertainment`.
- Big Sky Interactive credited in the executable.
- Nintendo **Dolphin SDK**: OS (`$Revision: 60 $`), DVD, VI, PAD, SI, AI, AR,
  ARQ, AX, DSP, CARD, FIO, GX modules are statically linked.
- **Embedded CPython** (2001 copyright; 1.5/1.6 compatibility text in the
  string table, so likely Python 2.1/2.2). Scripts are shipped as `.pyc`
  inside the TotemTech bigfiles.
- **TotemTech scripting** (`.tsc`, text): commands such as `OpenBF`,
  `LoadObjectLib`, `Source`, `SetDBPath`, `DisplayImage`, `SBPlayLogoMovie`.
- Asset containers: `.dgc` (TotemTech Data bigfile, 78 files), manifests
  `.ngc` (78 files), speech `.sgc`, audio `.vag/.wav/.pcm*`, FMV `.h4m`
  (CRI) and `.thp` (Nintendo).

### Filesystem

GameCube FST is the standard 12-byte-entry format: the first word packs an
8-bit type and a 24-bit name offset; the string table follows the entry array.
Dolphin's `FileSystemGCWii.cpp` confirms this layout. Extracted tree contains
425 FST entries / 338 files (601,702,268 bytes).

Top-level: `DATA/`, `DB/`, `LevelTSC/`, `Speech/`, `Music/`, `Costumes/`,
`EXTRAS/`, `enums/`, `axdemo/`, `thpdemo/`, plus `Init.tsc`, `User.tsc`,
`Screens.tsc`.

### Boot flow

`User.tsc` drives the first seconds:

1. `SetBFPath .\.` + `EnableBF Read`.
2. `OpenBF DATA\SPONGE` → `Source Init.tsc` → `Source Script.tsc`.
3. `OpenBF DATA\PRELOAD` → `SBPreloadData`.
4. `Source Screens.tsc`: legal screen, Nick/THQ/Big Sky logo movies,
   "Hit Start" screen.

The DOL entry (`0x80003140`) performs standard SDK startup plus a relocation
pass over a table reached through `[0x800000F4]`, then calls the engine entry
at `0x801EC128` (likely `main`) and exits through `0x80120FB0`.

## Recompilation

DolRecomp generated `work/game`-independent output in
`build/recomp/generated`:

- text0: 2,376 instructions (733 known, 1,643 embedded data).
- text1: 649,624 instructions (649,469 known, 155 embedded data, 0 unknown).
- 160 C chunks, portable C backend.
- 261 "possible patching instruction" sites, mostly cache-management
  (`dcbst`/`icbi`) and SDK relocation writes. Full list in
  `build/recomp/generated/generated_smc.txt`; review any site that writes to
  `.text` before assuming it is benign.

## Runtime

ModernGekko (Dolphin-derived RecompCore) is the chosen runtime:

- Dolphin's `BootManager` boots `sys/main.dol` directly.
- A `StaticRecompModuleSource` feeds the recompiled module into the
  PowerPC core; HLE covers OS/DVD/GX/AI/AX/DSP/input.
- The same runtime can supply the virtual disc from `work/game/files`.

Build tree: `build/moderngekko` (CMake + Ninja + MSVC).

## Next actions


1. Script level transitions and a longer story playthrough (hub room, menus,
   pause, memory-card save) to extend coverage beyond the tested sections.
2. Listen to the Cubeb audio output on hardware; the DSP thread runs without
   errors but audio content was not auditioned here.
3. Netplay smoke test between two instances.
4. Nintendo Switch port after the PC app is stable.

## Known risks

- **Self-modifying code**: 261 flagged sites; most are cache ops, but any real
  text patch needs an explicit DolRecomp patch.
- **CPython runtime**: exceptions use `setjmp`/`longjmp` and computed state;
  the recompiled Python VM must preserve those semantics.
- **FIO / host file I/O**: the SDK includes `HOST_OPEN`; retail code may call
  it through debug paths. The runtime may need to map it to the virtual disc
  or stub it.
- **AX/DSP audio**: game uses AX + DSP; first boot should be headless/muted.
- **GX**: TotemTech uses display lists, TEV, possibly paletted textures and
  odd vertex formats; expect rendering work after boot.
- **Memory card / saves**: CARD module is linked; save UI may probe the card
  early.

## Commands

```powershell
# Inventory and extract directly from ISO or RVZ (no conversion)
python tools\gcdisc.py info    "<disc>.rvz"
python tools\gcdisc.py list    "<disc>.rvz"
python tools\gcdisc.py extract "<disc>.rvz" work\game
python tools\gcdisc.py dol     "<disc>.rvz" work\disc\dol

# Disassemble the entry point
python tools\dol_disasm.py work\game\sys\main.dol 0x80003140 0x80003300

# Recompile only (already done once)
build\dolrecomp\dolrecomp.exe --gamecube work\disc\main.dol build\recomp
```