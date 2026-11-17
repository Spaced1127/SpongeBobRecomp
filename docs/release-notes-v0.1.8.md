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

`SpongeBobRecomp-v0.1.8-Windows-x64.zip` (28,824,025 bytes).

SHA-256:

```text
A08000F34C160C865C4C55272E0D75E1DED247E7922D0CE4993A412E1B7C686C  SpongeBobRecomp-v0.1.8-Windows-x64.zip
```