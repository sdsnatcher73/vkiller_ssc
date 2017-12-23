Vampire Killer SCC Version
==========================

What is this?
-------------
This is a patch which replaces the PSG music in Vampire Killer with SCC
music.


How to use it?
--------------
Here are the steps to apply the patch:

Save this rom as vkiller.rom:
  Akumajyo Drakyula. Vampire Killer (1986)(Konami)[a][RC-744]
  http://www.planetemu.net/roms/msx-msx2-various-rom

Save this rom as nemesis3.rom:
  Gofer no Yabou Episode II. Nemesis 3 - The Eve of Destruction (1988)(Konami)[a][RC-764] 
  http://www.planetemu.net/roms/msx-msx2-various-rom

Download the Vampire Killer TurboFix patch and apply it to vkiller.rom:
  http://frs.badcoffee.info/patches.html

Install Python 2.7 if you don't have it already:
  http://python.org

And then run:
  python patch.py

This should produce a new file: vkiller_scc.rom which is the patched version
of Vampire Killer with SCC music.



How does it work?
-----------------
This new version of contains new versions of all the Vampire Killer songs
which have been re-arranged to take advantage of the extra SCC channels and
the different SCC sounds. So it's much more than a simple "PSG to SCC"
conversion.
The SCC music is played on the Nemesis 3 SCC player code, which has been
integrated into the Vampire Killer ROM. All sounds effects are still played
using Vampire Killer's own PSG music player.
The new SCC music has been written in a MML-style language (see mml/vkiller_scc.mml)
and then compiled into the Konami music format and written into the ROM.


TurboFix Support
----------------
This patch is applied on top of the Vampire Killer 'TurboFix' patch, which
means it has improved controls (N key for jumping), has support for the R800,
and fixes the flickering sprites problem.
Unfortunately the TurboFix patch removes Game Master support, however you
can use Game Master 2 to select the stage and lives. To do this, put the
Game Master in slot 1 and the game in slot 2


Cheats
------
This patch includes some cheats to make sure everyone can play through the game
and enjoy the new music. The cheats are as follows:

Press 'G' to GIVE all weapons and items and restore your health
The screen won't update immediately, so it might seem as if it's doesn't
do anything, but it does.

Press 'I' for INVINCIBILITY.
This will temporarily make you glow red, the same as picking up an 
invincibility ring.

This is the same effect a picking up an invicibility