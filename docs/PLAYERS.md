# Players

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

The runner detects Xbox, PlayStation, Switch and generic SDL pads and applies
the matching layout even when RecompLauncher starts it directly. Switch uses
the printed A/B/X/Y labels; Xbox, PlayStation and generic pads use the physical
positions. You can override the layout on the RecompLauncher game page
(**Controller**) or in `config.ini` with
`controller_profile=auto|xbox|playstation|switch|generic`.
Connect the controller before launching. Two players are supported (port 1 and
port 2) for the game's multiplayer modes. Touch controls are not part of the PC
build.

## Save data

The game uses a folder-based memory card (GCI) created on first launch:

```
<app folder>\User\GC\USA\Card A\
```

If the app folder is read-only, the card lives in
`%LOCALAPPDATA%\SpongeBobRecomp\GC\USA\Card A`.

To bring saves from an emulator, copy the GCI files from your Dolphin memory
card into that folder. Card images (`.raw`, `.mcd`, `.ps2`) are not read
directly by this build.

## Save states

The runner supports save states through the automation and in-game menu. They
are stored beside the game's user data and are not portable between builds of
the recompiled module.
