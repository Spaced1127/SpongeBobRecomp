# Players

## Disc image

Use your own USA `.iso` or Dolphin `.rvz` directly. There is no RVZ-to-ISO
conversion step: the launcher and the bundled tools detect RVZ by its
`RVZ\x01` magic and read the zstd-compressed groups natively. RecompLauncher
accepts either format on its setup screen.

## Controls

| Action | Keyboard | GameCube pad | Xbox pad | DualSense | Switch Pro |
|---|---|---|---|---|---|
| Move | Arrow keys | Left stick / D-pad | Left stick / D-pad | Left stick / D-pad | Left stick / D-pad |
| Camera | I / J / K / L | C stick | Right stick | Right stick | Right stick |
| Jump / confirm | Z | A | A | Cross | A |
| Cancel / attack | X | B | B | Circle | B |
| Action 1 | A | X | X | Square | X |
| Action 2 | S | Y | Y | Triangle | Y |
| Pause | Enter | Start | Menu | Options | Plus |
| Emulator menu | Esc | — | — | — | — |
| Fullscreen | F11 | — | — | — | — |

There is **one controller profile** and it is never rewritten. The runner
creates it once (`Config\GCPadNew.ini`) and every pad is bound to it, so no pad
needs to be connected on the first launch and a sleeping wireless pad cannot
break the next one.

The profile is always positional (A/B/X/Y in the Xbox/PlayStation positions).
The **layout class** decides which pads print Nintendo labels and therefore need
A<->B and X<->Y swapped so the printed label matches the action:

- **Auto** (default) picks the class per pad from its SDL type. Xbox 360 / One /
  Series / Elite, DualSense, DualSense Edge, DualShock 4/3 and generic pads are
  positional; Switch Pro and Joy-Cons are Nintendo. 8BitDo pads in Switch mode
  are recognised by their vendor/product ID (2dc8:6006 and the 05ac:0004 Switch
  clone); the same pads in XInput mode stay positional.
- **Positional** and **Nintendo** force one class for every pad if the automatic
  choice is wrong for you (RecompLauncher page or `controller_class=` in
  `config.ini`). `--controller-layout` accepts the same values, and the old
  `standard` / `switch` spellings still work.

Only the face buttons swap. D-pad, sticks, triggers, Start and Z never do, and
paddles/Fn buttons are deliberately unbound (no GameCube equivalent).

A pad plugged in after launch is picked up within about two seconds; if the
configured pad is missing the first pad is bound instead. Neither case touches
the profile file. **Delete `Config\GCPadNew.ini` once if you want the canonical
profile regenerated** - it is optional (an old generated profile still binds,
because the runtime resolves the first pad and the class comes from the pad, not
the file).

If a pad maps wrongly, send the one startup line, which carries everything
needed to triage it:

```text
controller: name="..." guid=... type=xboxone class=positional override=auto device="SDL/0/..." source=sdl profile=static
```

## Save data

Slot A is a raw 128 Mbit GameCube memory card (16 MiB, 2043 blocks) created on
first launch; slot B is empty:

```
<app folder>\User\GC\MemoryCardA.USA.raw
```

If the app folder is read-only, the card lives in
`%LOCALAPPDATA%\SpongeBobRecomp\GC\MemoryCardA.USA.raw`.

Saves made by v0.1.6 and older live as `.gci` files in `GC\USA\Card A\`. The
first launch of this build imports them into the raw card automatically and
leaves the `.gci` files in place as a backup, so existing saves keep working.
If the import cannot complete, the game keeps using the old folder card rather
than starting empty.

To bring saves from an emulator, add the `.gci` to `GC\USA\Card A\` before the
first launch of this build (it is imported), or use Dolphin's memory card
manager to import it into `MemoryCardA.USA.raw`.

## Save states

The runner supports save states through the automation and in-game menu. They
are stored beside the game's user data and are not portable between builds of
the recompiled module.
