# SpongeBobRecomp v0.1.8 - controllers, widescreen and pacing

Follow-up to v0.1.7: one canonical controller profile, the widescreen fix and
the frame-pacing result. No game data is included.

## Controllers: one canonical profile

Every pad with a GameCube-shaped layout now uses **one profile**,
`Config/GCPadNew.ini`, written once and never rewritten:

- **Positional** (default) binds A/B/X/Y to the Xbox/PlayStation positions.
  Xbox 360 / One / Series / Elite, DualSense, DualSense Edge, DualShock 4/3
  and generic pads are positional.
- **Nintendo** swaps A<->B and X<->Y so the printed label matches the
  action. Switch Pro, Joy-Cons and 8BitDo pads in Switch mode are Nintendo.
  D-pad, sticks, triggers, Start and Z are never swapped.
- The class is resolved per pad from SDL's gamepad type with one explicit
  8BitDo ID fallback, at input time. The profile text does not change, so a
  sleeping pad, a new pad or a pad plugged in later cannot break the file.
- If the configured pad is missing, the **first pad is bound instead**, and
  a pad plugged in after launch is picked up within ~2 seconds. No restart,
  no profile rewrite.
- Override with **Controller layout** in RecompLauncher, or
  `controller_class=auto|positional|nintendo` in `config.ini`.

Already had a profile from an older build? Nothing to do - it still binds,
and the class comes from the pad, not the file. Deleting
`Config/GCPadNew.ini` once regenerates the canonical one (optional).

## Widescreen

**16:9 now always includes the widescreen hack.** Before, the aspect ratio and
the "Widescreen hack" checkbox were independent. Picking "16:9 widescreen"
without ticking the hack stretched the 4:3 image horizontally: SpongeBob and
every wall picture became 1.33x wider in the wrong direction. That is the "it
still doesn't render properly" report.

- Choosing **16:9** in the launcher or the RecompLauncher page now enables the
  hack, and a `config.ini` with `aspect=wide` turns it on at load time.
- The checkbox reads "Widescreen hack (correct 3D at 16:9)".
- **Stretch** is still there if you want a plain horizontal stretch.
- Measured: at 16:9 with the hack the 3D world keeps its proportions (wall
  pictures square, SpongeBob normal, more of the room visible); without it the
  whole 3D view is 1.33x too wide.
- **Known limitation:** the 2D HUD (screen-space art such as the camera icon)
  still scales to the screen at 16:9, so HUD art is ~1.33x wider. It is
  pixel-correct in Auto/4:3, which adds side bars.

### Controller verification

- Offline: 46 checks - a 23-family class matrix (Xbox 360 USB/Bluetooth, One,
  One S/Series, Elite, unknown-PID Xbox, DualSense, DualSense Edge, DualShock
  4/3, a Sony pad reporting STANDARD, generic DirectInput, generic unknown,
  8BitDo XInput / Ultimate / Pro 2 Nintendo mode / SN30 Pro / Switch-mode clone,
  Switch Pro and all three Joy-Cons), override precedence in both directions,
  the canonical profile text, write-once behaviour and legacy key handling.
- Live on this build: a real Xbox One pad resolves `class=positional`, the
  Nintendo override flips it to `class=nintendo`, and the profile file is
  byte-identical in every case (`035B9490…2A83`).
- The shared input layer is **validated on real hardware**: the same code in
  WWE WrestleMania X8 Recomp v0.1.4 binds and plays with a physical Xbox pad
  (user-tested), and SpongeBob v0.1.8 uses it unchanged. PlayStation pads use
  the same positional class they always did.
- Still worth confirming on your own pad: A/B/X/Y, both sticks, triggers,
  shoulders, D-pad, Start. If anything is off, send the single `controller:`
  startup line - it carries name, GUID, SDL type, class, device and source.

## Stutter

Measured on this build with the packaged runner:

- **Cold shader cache** (cache deleted): 59.86 fps average, `speed_min`
  0.9961, no frame deficit. Shader compilation is not the cause - the runtime
  already uses asynchronous ubershaders with a shader cache.
- **25 s walk across the room:** 59.97 fps average, 1,493 emulated frames
  against 1,492 expected, `speed_min` 1.0000.
- One real hitch exists: the START -> scene transition (level load plus the
  memory card access) costs about 190 ms, once per transition.
- Anything beyond that is environmental on the player's machine (variable
  refresh plus desktop composition, multi-plane overlays, video on another
  display, or the older v0.1.3 build before the PGO module and audio fixes).
  If it persists, send the `[video]` line from the runner log, the display
  setup and whether V-Sync is on.

## Please verify

- 16:9: the picture fills the screen and nothing looks horizontally squashed;
  the HUD is slightly wide (known), 4:3 keeps it exact.
- Stutter: if you still see it, note the scene, whether it is the first visit
  to that scene, and your display/V-Sync setup.

## Download

`SpongeBobRecomp-v0.1.8-Windows-x64.zip` (28,817,632 bytes).

SHA-256:

```text
1DEB607039EC229DD49A9E3D2E362B1C1DC5DA00ABB0A94F35E2C05BAD00CA07  SpongeBobRecomp-v0.1.8-Windows-x64.zip
```