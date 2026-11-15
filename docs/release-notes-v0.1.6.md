# SpongeBobRecomp v0.1.6

Native RVZ input. Players can pick their Dolphin `.rvz` directly; there is no
RVZ-to-ISO conversion step.

No game data is included.

## RVZ support

- **RecompLauncher accepts `.iso` or `.rvz`.** The manifest label names both,
  and `check.ids ["GSQE78"]` reads the GameCube disc ID from the RVZ header at
  0x58. RecompLauncher's compressed-image gate accepts the file when the label
  names `.rvz`.
- **The app and `--extract` read RVZ natively.** They use Dolphin DiscIO, so
  the existing custom launcher path needs no conversion.
- **The Python tools read RVZ natively.** `tools/gcdisc.py` and
  `tools/verify_dol.py` detect `RVZ\x01` by magic and decompress zstd groups
  on demand. `gcdisc.py extract` writes the same `sys/` + `files/` tree as the
  app. `tools/rvz_extract.py` is now only for another tool that requires a
  raw ISO.
- The RecompLauncher manifest remains at 14 settings, including **Controller
  layout**.

## Controller support

- **GUID-first detection.** The controller table keys on SDL's standard-form
  VID/PID from the 32-character GUID, not on product names. USB, Bluetooth and
  XInput variants resolve the same way.
- **DualSense Edge** (`054c:0df2`) uses the standard PlayStation layout.
- **Xbox Elite Series 1/2** (`045e:02e3`, `0b00`, `0b05`, `0b22`) use the
  standard Xbox layout.
- **8BitDo Nintendo layout is detected from the live SDL mapping.** Pro 2 in
  Nintendo/Switch mode reports `a:b1,b:b0` (Switch mode `a:b3,b:b2`), so it
  uses the printed A/B/X/Y labels. Ultimate (`a:b0,b:b1`) and 64 stay
  standard. Detection reads `SDL_GetGamepadMappingForID`, not the product
  name. A reversed `dpleft`/`dpright` sets `dpad_swap` and writes corrected
  Left/Right bindings.
- **Paddles and Fn/extra buttons are deliberately unbound.** The game has no
  extra actions; face buttons, triggers, sticks and D-pad behave exactly like
  a standard DualSense/Xbox pad.
- **Startup diagnostics** print:
  `controller: "<name>" guid=<32 hex> bus=<...> vid=<...> pid=<...>
  layout=<...> source=<guid|type> dpad_swap=<yes|no> face_swap=<yes|no>
  [paddles=unbound] [extras=unbound] [family="..."]`
  Players should send that line if a pad maps wrongly.

## Verified

- Project RVZ SHA-256:
  `974260E409B7A712184FD5CD2146C11EBC6A7C627EF50F817AAF2615ABB06E80`
  (489,157,208 bytes).
- RVZ-to-ISO export SHA-256:
  `FFDEB4FD370CB357A5F110D3E77C3E8BE7DB5A395818480C4308A1B820039A5D`,
  identical to the ISO.
- Launcher ISO vs RVZ: 343 files / 604,947,746 bytes, tree SHA-256
  `78BD825AF9DD03818984D7E06F945C40DB949AEAB369039FF5A4C62BD37159B6`
  identical.
- `sys/main.dol`:
  `DCA4F72B57E8BF3F540E694F01CC23EF687D2B25028D974B67356E15F1C2E009`.
- `sys/fst.bin`:
  `A957E4F067711256F9C7161256CCD7E02BD2ED201C5C656736CE79894DFDF529`.
- Controller-layout unit test: 62 PASS, 0 FAIL. Covers Edge USB/Bluetooth,
  Elite 02E3/0B00/0B05/0B22, all four 8BitDo Pro 2 Nintendo GUIDs, Pro 2
  Switch mode, Ultimate/64 standard, a synthetic reversed D-pad, profile
  migration/custom preservation and standard DualSense/Xbox One/360/Switch Pro
  regression.
- SDL DB check: Edge USB/Bluetooth standard actions are identical to a
  standard DualSense; Elite USB/Bluetooth entries contain every standard Xbox
  action. Raw indices vary by firmware, SDL action names do not.
- Hardware confirmation was unavailable (the test host reported 0 SDL
  gamepads); the startup diagnostic line is the support handoff.
- Packaged candidate extraction matched the same tree hash; no game data in
  the zip.

## Please verify

- **8BitDo Pro 2, Nintendo/Switch mode:** printed A/B/X/Y and D-pad.
- **8BitDo Ultimate and 64:** standard face-button positions (unchanged).
- **DualSense Edge:** face buttons, triggers, sticks; paddles/Fn intentionally
  do nothing.
- **Xbox Elite Series 1/2:** face buttons, D-pad, triggers; paddles
  intentionally do nothing.
- If anything is off, send the startup line beginning `controller:` with the
  name, GUID, layout, `dpad_swap` and `face_swap` values.

Controllers were verified offline against the SDL gamecontrollerdb and the
unit suite; physical confirmation is requested.

## Download

`SpongeBobRecomp-v0.1.6-Windows-x64.zip` (28,810,819 bytes).

SHA-256:

```text
581CF8F0E14B80F8C8F429E8D40FF5365742AA3870658FF58E615688DB3B0413  SpongeBobRecomp-v0.1.6-Windows-x64.zip
```
