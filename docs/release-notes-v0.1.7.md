# SpongeBobRecomp v0.1.7 - controller + memory card hotfix

Fixes the Xbox controller reports on v0.1.6 and moves the memory card to the
shared slot A raw-card layout. No game data is included.

**Status: released.** No commit or release existed before this one; approval
was given by the user for the v0.1.7 hotfix.

## Memory card

The memory card now follows the shared runtime pattern used by the other
GameCube ports:

- **Slot A is a raw 128 Mbit card** (`GC/MemoryCardA.USA.raw`, 16 MiB,
  2043 blocks) and **slot B is empty** (`255`). Both keys are written to
  `Config/Dolphin.ini` on every launch. v0.1.6 and older never wrote them, so
  Dolphin's GCI-folder default was used and `Dolphin.ini` did not exist.
- **Your existing saves are imported automatically.** On the first launch of
  this build, the `.gci` saves in `GC\USA\Card A\` are copied into the raw card
  and the old files are left in place as a backup. If the import cannot
  complete, the game keeps using the folder card instead of starting empty.
- The card is created and formatted before the console's expansion interface
  initialises, so the first save cannot hit a "checking memory card" stall.
- Startup log now prints
  `memory card: slot A = raw, slot B = none, created MemoryCardA.USA.raw bytes=16777216`
  (or `migrated N save(s) ...`), which is the line to send if saving misbehaves.

### Memory card caveats

- Save states store the EXI device type. A state made while slot A was the GCI
  folder restores the folder device: delete that state or make a new one.
- Closing the game normally flushes the card. A force-kill (task manager) can
  skip the flush and lose the newest save.

## What went wrong in v0.1.6 (controllers)

The 8BitDo / DualSense Edge work added two rules that read the pad's live SDL
mapping. Both were applied to **every** pad:

- `a` after `b` -> printed-label (Switch) layout. Of the 797 rows in the SDL
  database this build ships, **110** flipped to printed-label A/B and X/Y —
  the generic "USB Gamepad", PS2-adapter, Steam virtual-pad and third-party
  Xbox-shape rows that Windows and Steam put in front of a real Xbox pad.
- `dpleft` after `dpright` -> D-pad correction. That inverted **34** rows that
  SDL already had right (DualShock 3, PS2 adapters, Steam pads).

A Microsoft product ID that is newer than the table (`0B20`, `0B2A`, ...) had
no fallback at all, so it depended on those rules.

Standard Xbox rows themselves were never flipped: every Xbox 360 / One /
Series / Elite GUID still generated the same `GCPadNew.ini` byte for byte.

## Fixed

- **Xbox pads resolve Xbox.** Vendor-family fallback from the standard-form
  GUID: `045E` -> Xbox, `054C` -> PlayStation, `057E` -> Switch. New or unknown
  Xbox product IDs (`0B20`, `0B2A`, ...) now resolve Xbox; the startup line says
  `source=guid-family`. Every Xbox 360 / One / Series / Elite GUID in
  `0B12`, `0B13`, `0B22` and the rest is covered by the table and the offline
  matrix.
- **8BitDo heuristic scoped correctly.** The Nintendo layout now needs a
  Nintendo signal — 8BitDo vendor (`2DC8`), SDL's
  `SDL_GAMECONTROLLER_USE_BUTTON_LABELS` hint, or paddles — and never overrides
  a GUID, Xbox or PlayStation verdict.
- **DualSense / DualSense Edge D-pad no longer mirrored.** A stock pad's SDL
  row already says which side `dpleft` is; only a reversed hat/axis on a
  Nintendo-mapped pad sets the D-pad correction. Button-order D-pads
  (DualShock 3, PS2 adapters, Steam pads) are never inverted.
- **Device line matches the runtime.** The runner enumerates with Dolphin's own
  SDL hints, so `Device = SDL/...` names the device the runtime creates.
- **The controller profile is only rewritten when a pad is present.** With no
  SDL gamepad the existing `GCPadNew.ini` is left byte-identical (verified).

Do you have a pad that still maps wrongly? Send us your startup controller
line — it is printed on every launch and contains everything needed:

```text
controller: "Xbox 360 Controller" guid=030000005e0400008e02000000000000 bus=usb
vid=045e pid=028e layout=xbox source=guid dpad_swap=no face_swap=no
family="Xbox 360"
controller configuration: 1 GameCube controller mapped (xbox layout)
device="SDL/0/Xbox 360 Controller" profile=...\Config\GCPadNew.ini
```

`layout=` should be `xbox`, `playstation` or `switch`; `dpad_swap=` and
`face_swap=` should be `no` for Xbox and PlayStation pads.

## Verified offline

- `moderngekko_controller_layout_test.exe`: **130 PASS, 0 FAIL**. 34 real SDL
  database rows (Xbox 360 USB/Bluetooth, One 02D1/02DD/02E0/02EA/02FD,
  Series 0B12/0B13, Elite S1/S2 USB+Bluetooth, DualSense, DualSense Edge, DS4,
  DS3, 8BitDo Pro 2 Nintendo/standard, Ultimate, 64, Switch Pro), each asserting
  the layout, the swaps and the generated profile; the Xbox profile is locked
  byte-for-byte to the v0.1.6 text.
- Memory card: fresh user dir creates `MemoryCardA.USA.raw` (16,777,216 bytes,
  SHA-256 `81DF7FED...00DA`) with `SlotA = 1` / `SlotB = 255`; the real v0.1.6
  save `78-GSQE-SpongeBob RFD.gci` is imported (directory entry `GSQE78` /
  company `78` / `SpongeBob RFD` / 8 blocks, card `DA7AA9CA...77B6`); a second
  launch leaves the card byte-identical.
- Packaged v0.1.7 runner, hidden desktop: raw card created, keys written,
  `booted=1`, `vps=59.9402`, `speed=1`, clean `stop` shutdown.
- **Not verified:** an in-game Save -> Load round trip on the raw card. The
  migrated save is in slot A, so this is one step to confirm
  (Options -> Load Game -> slot A).
- `work/verify-controller/check_regression.py`: 150/797 SDL rows change
  behaviour between v0.1.6 and v0.1.7 (20 Nintendo pads now correct, 110 wrong
  printed-label layouts gone, 34 inverted D-pads fixed).
- Hidden-desktop boot with a seeded Xbox profile and no connected pad leaves
  the profile byte-identical.
- Hardware confirmation is still unavailable here (the host reports 0 SDL
  gamepads); the two startup lines are the support handoff.

## Hardware caveat

Controllers are verified offline against the SDL database this build ships and
by the unit matrix, and one live Xbox pad report is what started this fix. The
memory card is verified at file and directory-entry level. Physical DualSense
Edge, Elite S2 and 8BitDo confirmation is still wanted: check A/B/X/Y, both
sticks, triggers, shoulders, D-pad and Start, and send the two startup lines if
anything is off.

## Please verify

- **Saving and loading:** Options -> Save Game (new file), quit, launch again,
  Options -> Load Game -> slot A. The startup log should say
  `memory card: slot A = raw, slot B = none, ...` and, on the first launch
  after upgrading, `migrated N save(s)`.
- Xbox 360 / Xbox One / Xbox Series: A/B/X/Y in Xbox positions, both sticks,
  triggers, shoulders, D-pad, Start.
- Xbox Elite S1/S2: same, paddles do nothing.
- DualSense / DualSense Edge: PlayStation positions, D-pad, triggers.
- 8BitDo Pro 2 (Nintendo and standard modes), Ultimate, 64, Switch Pro.