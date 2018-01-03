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

Download SJASMPlus:
  https://sourceforge.net/projects/sjasmplus

Install Python if you don't have it already:
  http://python.org

And then run:
  python patch.py

This should produce a new file: vkiller_scc.rom which is the patched version
of Vampire Killer with SCC music.



TurboFix Support
----------------
This patch is applied on top of the Vampire Killer 'TurboFix' patch by FRS, which
means it has improved controls (N key for jumping), has support for the R800,
and fixes the flickering sprites problem.
Unfortunately the TurboFix patch removes Game Master support, however you
can use Game Master 2 to select the stage and lives. To do this, put the
Game Master in slot 1 and the game in slot 2.
For more information about the TurboFix patch, see turbofix_readme.txt.


Cheats
------
This patch includes some cheats to make sure everyone can play through the game
and enjoy the new music. The cheats are as follows:

Press 'G' to GIVE all weapons and items and restore your health
The screen won't update immediately, so it might seem as if it's doesn't
do anything, but it does.

Press 'I' for INVINCIBILITY.
This will temporarily make you glow red. It's the same effect as picking up an 
invincibility ring.


KSS File
--------
Apart from producing a patched ROM, patch.py also produces vkiller_scc.kss,
which is a KSS version of the new SCC Vampire Killer soundtrack. You can
use this together with the provided .m3u playlist file to listen to the
new SCC Vampire Killer soundtrack (for example in Winamp).


How was this made?
------------------
All the songs in this new version of Vampire Killer have been re-arranged
to take advantage of the extra SCC channels and the different SCC sounds.
So it's much more than a simple "PSG to SCC" conversion.
The SCC music is played on the Nemesis 3 SCC player code, which has been
integrated into Vampire Killer. All sounds effects are still played
using Vampire Killer's own PSG music player.

The new SCC music has been written in a MML-style language (see
mml/vkiller_scc.mml) and then compiled into the Konami music format and
written into the ROM.

First I reverse engineered the Konami sound format. I wrote some code that
can decode the sound format to MIDI files. I have this working for many
Konamis including Solid Snake and SD Snatcher. It's fascinating to see how
the file format changed from game to game, what all the different commands
are that the music composers had access to, and how they used it to make
their music. I intend to release more information about this in the future,
and I also will release the tools I wrote to decompile Konami music.

To generate the new music I decompiled the Vampire Killer music into MIDI,
and then loaded them up into Ableton Live where I added extra harmonies
and chords. I then converted the MIDI to a text representation of Konami's
SCC music data format. This text file format is similar to MML.
I then edited the MML, adding instruments and commands (volume, envelope,
tremolo) and then converted that back into konami SCC music format which
is then written into the ROM.
