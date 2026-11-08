# Players

## Controls

| Action | Keyboard | GameCube pad | Xbox pad | DualSense | Switch Pro |
|---|---|---|---|---|---|
| Move | Arrow keys | Left stick / D-pad | Left stick / D-pad | Left stick / D-pad | Left stick / D-pad |
| Camera | I / J / K / L | C stick | Right stick | Right stick | Right stick |
| Jump / confirm | Z | A | A | Cross | B |
| Cancel / attack | X | B | B | Circle | A |
| Action 1 | A | X | X | Square | Y |
| Action 2 | S | Y | Y | Triangle | X |
| Pause | Enter | Start | Menu | Options | Plus |
| Emulator menu | Esc | — | — | — | — |
| Fullscreen | F11 | — | — | — | — |

The launcher shows the detected controller and lets you pick a profile per
player. Two players are supported (port 1 and port 2) for the game's
multiplayer modes. Touch controls are not part of the PC build.

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
