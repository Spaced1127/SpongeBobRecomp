SpongeBob SquarePants: Revenge of the Flying Dutchman
Standalone PC port (JIT default, static recompilation included) - Windows x64
================================================================

This package contains NO game data. There is no disc image, no ROM, no
textures, no audio and no level data in these files. The recompiled module is
program code only; the art, sound and levels are read at runtime from the game
files you supply.


WHAT YOU NEED
-------------
An original GameCube copy of "SpongeBob SquarePants: Revenge of the Flying
Dutchman" (USA, disc ID GSQE78), either as:

  * a .iso image (1.36 GiB, clean 1:1 dump), or
  * a .rvz image (Dolphin compressed format).

Both are imported by this app. Other regions and other games are rejected.


QUICK START
-----------
1. Put this folder anywhere you have write access (for example
   C:\Games\SpongeBobRecomp). Do not put it in Program Files: the extracted
   game is written into a "Game" folder next to the executable.

2. Run SpongeBobRecomp.exe.

3. Click "Browse for ISO / WBFS / RVZ", pick your disc image, then click
   "Extract and Play". The disc is extracted once into a "Game" folder beside
   the executable and remembered in default-game.txt.

   If you already extracted the disc elsewhere, click "Browse for extracted
   game folder" and pick the folder that contains "sys" and "files".

4. Click Play. The game window opens; Esc opens/closes the in-game menu.

The extracted folder needs about 1.4 GB. Re-importing the same disc reuses the
existing extraction.


SETTINGS
--------
All settings are stored in config.ini in
%LOCALAPPDATA%\SpongeBobRecomp\ and persist between sessions. The launcher reads and
writes them; you do not need to edit the file by hand.

The launcher has five pages: PLAY, GRAPHICS, PERFORMANCE, AUDIO and CONTROLLER.
Everything is saved automatically.

  Graphics backend        Vulkan (recommended) or OpenGL
  Internal resolution     640x528 (1x) up to 7680x4320 (12x)
  Anti-aliasing (MSAA)    Off / 2x / 4x / 8x, plus SSAA
  Anisotropic filtering   1x / 2x / 4x / 8x / 16x
  VSync                   on / off
  Aspect ratio            Auto (game native) / 16:9 / 4:3 / Stretch
  Widescreen hack         stretches 3D to the chosen aspect
  Frame rate              Fixed 60 (console timing)
  Audio                   Mute all audio, master volume 0-100%
  2D compatibility        EFB access, ON by default
  Show FPS in title       on / off
  Fullscreen, controller profile, netplay host/join

FRAME RATE
----------
The game runs at the console's 60 Hz timing. The old 150% / 200% / unlocked
options have been removed so the game cannot run faster than 60 fps. Existing
configuration files are loaded at 60 fps automatically.

CPU CORE
--------
PERFORMANCE page -> "Game core".

  * JIT (default) uses Dolphin's JIT core. It holds 60 fps in all tested
    scenes, including Bikini Bottom outside SpongeBob's house.
  * Static recomp runs gGSQE78_recomp.dll, the static-recompilation build.
    It is the faithful static artifact, but heavy 3D scenes can dip to
    around 40 fps.

Both modes read the same extracted game files. The static module ships in
this package and can be selected at any time.

AUDIO
-----
AUDIO page -> "Mute all audio" silences the game, movies and menu sounds; the
master volume slider sets the mix level. Mute is applied at the audio backend,
so it also silences the intro videos.

2D COMPATIBILITY (EFB ACCESS)
-----------------------------
Leave this ON. The legal notice, the "PRESS START" title screen and the menus
are drawn through the GameCube's embedded framebuffer and render black without
it. Accurate reads have no measurable cost in 3D scenes, so there is no reason
to turn it off.

Texture replacement mods are not required and not installed by default. Any
Dolphin-style texture pack placed in the user folder is ignored: this build
loads assets only from your own disc extraction.


CONTROLS (default)
------------------
  Left stick / D-pad      move
  A                       jump / confirm
  B                       cancel / attack
  X, Y                    game actions
  Start                   pause
  Esc                     open/close emulator menu
  F11                     toggle fullscreen

Controllers are auto-detected (Xbox, DualSense, Switch Pro and most SDL
gamepads). Pads are laid out in the launcher.


FILES
-----
  SpongeBobRecomp.exe          launcher, importer and settings
  SpongeBobRecompRunner.exe    game process
  gGSQE78_recomp.dll           optional static-recomp core (no assets)
  Sys\                         graphics shaders and runtime tables
  LICENSES\                    third-party licenses
  config.ini                   created on first run
  Game\                        created when you import your disc


TROUBLESHOOTING
---------------
"expected disc ID GSQE78; selected ..."
    The image is a different game or a different region.

"game root is not a readable directory"
    The selected extracted folder is wrong. Pick the folder that directly
    contains "sys" and "files".

"main DOL does not match the pinned release"
    The extracted program file is not the retail build this port was compiled
    for. Re-extract from a clean, unmodified disc image.

The launcher window is black.
    Update your graphics driver. The launcher itself uses a software renderer
    and does not need a GPU; the game window needs Vulkan or OpenGL 4.4.

Low frame rate
    Lower the internal resolution, turn off MSAA/SSAA, and check the GPU driver.
    The default settings target 60 fps at 1080p.

Save states and controller profiles are per-user in %LOCALAPPDATA% or beside
the executable when the folder is writable.
