Vampire Killer / Akumajo Dracula - Dynamic vsync patch
------------------------------------------------------
v1.0 (c) 2011 by FRS, all rights reserved

1) This patch implements the Dynamic Vsync timing routines on the game, greatly
reducing slowdowns on Z80A machines and allowing the game to be run on with the
turbo enabled on machines that have this feature. The turbo will be enabled by
default on any machine that has the standard CHGCPU routine on its BIOS (like
MSX Turbo-R machines).

2) The patch will also implements the following enhancements and fixes:

- Hold TAB to throttle the game speed
- Automatically sets the VDP to 60Hz on boot, to play the game at the correct
  speed even on european machines. If you have an old european TV that doesn't
  support this, keep SELECT pressed on boot to disable it.
- Fixed the 50Hz speed bug (which is the same as the turbo bug): the
  Z80A/3.57MHz was also too fast to run the game at 50Hz.
- Page flipping for the sprites: Fixes the sprite flickering that happened on
  the top the of the screen and eliminates tearing completely.
- Enhanced sprite cycling: sprites will be cycled as fast as your CPU is able
  to do it, up to 60Hz. This results in smoother flickering. 
- Removed the internal pseudo GameMaster-1 to release space for the
  enhancements. You can use GameMaster-2 with this game instead.
- Correct handling of non-VDP interrupts, that are now passed along to the
  interrupt chain.
- Fixed inconsistent keyboard vs joystick interface: now when playing on the
  keyboard the player also jumps by pressing the secondary trigger (M or N key).
  The UP key is now only used to climb stairs. This solves the frustrating
  jumping-instead-of-climbing situations that happened before.
- Added support for the Megadrive 3-button joypad connected though a joymega
  adapter. (START = pause, A-button = MAP). Don't connect the joypad directly
  to the MSX! The adapter *MUST* be used.
  http://frs.badcoffee.info/hardware/joymega-en.html


How to apply the patch
-----------------------

First, make sure you have the last release of the original japanese ROM,
which has the following checksum:

SHA1(VKILLER.ROM)= 5460a88c25386b1b950b57fc1325fd75587cc825

You can use the following tools to verify the SHA1 checksum:
- Windows:
  -MD5 & SHA-1 Checksum Utility 1.1
  - HashTab
- Mac OS-X:
  - DropHash
  - HashTab
  - (or use the Linux solution below)
- Linux:
  - Just type "openssl dgst -sha1 MYGAME.ROM" on a shell (without the quotes,
    off course).

Secondly, there are two versions of this patch: The IPS version and the XPC
version.

- For the IPS version, select an IPS patcher like IPSWin, LunarIPS or UIPS and
  use it following to the tool's instructions. The IPS patch is more
  recommended for emulator users.

- For the XPC version, on-the-fly patching: just place the XPC patch under the
  same directory of your ROM and make sure both have the same name
  (i.e: MYGAME.ROM and MYGAME.XPC). The bugfix will be applied automatically
  by ExecROM and you will be asked if you want to apply any optional patches
  included (usually cheating/trainer patches).

==============================

Special Thanks

- OpenMSX team, for their excellent emulator and debugger
- MRC crew, for the place where MSX hobbysts can meet and exchange ideas
- Sjoerd Mastijn and Aprisobal, for the SjASMPlus assembler
- FiXato, for compiling many development tools I use on Mac OS-X

==============================

FAQ
---

Q: Will the patched game run on non-turbo machines?
A: Yes, the patch implements a new timing routine that supports any CPU speed,
   including of course the standard 3.57MHz Z80A.

Q: I applied the patch and the resulting ROM doesn't work! What is wrong?
A: You're probably trying to apply the patch on a ROM with the incorrect
   checksum. If you used the XPC version, try the IPS version instead.

Q: I applied the XPC patch using XPCTools and some undesired features (like
   invulnerability) are being enabled by default! How can I select which
   patches will be applied?
A: You forgot to add the "-ask" parameter to the xpcapply command-line.

Q: Why there are IPS and XPC patches? Do I need to apply both?
A: Its the same patch in two different formats. You only need to use the format
   you think is more suitable to your needs. IPS files only support one single
   patch per file and need to be pre-applied, while XPC files support multiple
   different patches in a single file and can be used for on-the-fly patching.
   Usually emulator users should apply the IPS patches.


===========================================================================
	                     License
                           Terms of use
---------------------------------------------------------------------------

1) This patch is free (gratis) for non-commercial purposes. You can only run,
   make backup copies or distribute the patch under this strict condition.

2) You are only allowed distribute the patch files (online or on a removable
   media) under the following conditions:
   2.1) No commercial transaction of any kind is involved
   2.2) All the included files are distributed together inside the same
   compressed file.

3) If you want to use this patch for commercial purposes you MUST contact me
   first to negotiate the terms and conditions. Use the e-mail supplied at
   the beginning of this document for contacting me.

4) This software is provided free of charge for non-commercial purposes, and the
   author retains its copyright.

5) You cannot distribute ROMs with my patches applied on them.

6) This software is provided ‘as-is’, without any express or implied warranty.
   In no event will the author be held liable for any damages arising from the
   use of this software.

7) USE THIS SOFTWARE SOLELY AT YOUR OWN RISK.




==============================

I hope you enjoy these fixes.

