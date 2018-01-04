; -----------------------------------------------------------
; Code for hooking in calls to the nemesis 3 SCC player

        output  vkiller_patch00038.bin
        org     04038h

        call    music_update_shim



        output  vkiller_patch010ac.bin
        org     050ach

        pop     af
        ld      e, a  ; save song index for later
        push    af
        nop
        call    music_start_shim
        nop
        nop
        nop


        output vkiller_patch01c8a.bin
        org     05c8ah

music_update_shim:
        di

        ; read keyboard
        in      a, (0aah)
        and     0f0h
        or      3
        out     (0aah), a
        in      a, (0a9h)

        bit     4, a
        jr      nz, skip_give_cheat
        ; give full health + various items
        ld      a, 020h
        ld      (0c415h), a
        ld      a, 2
        ld      (0c416h), a
        ld      a, 018h
        ld      (0c431h), a
        ld      a, 0ffh
        ld      (0c700h), a
        ld      a, 081h
        ld      (0c702h), a
        ld      a, (0c701h)
        or      0FEh
        ld      (0c701h), a
        jp      end_cheats

skip_give_cheat:
        bit     6, a
        jr      nz, end_cheats
        ; invincible
        ld      a, 0ffh
        ld      (0c434h), a

end_cheats:
        ld      a, 16
        ld      (07000h), a
        call    music_update
        ld      (07000h),a
        ret

music_start_shim:
        ld      a, 0ffh
        ld      (0e600h), a  ; game master detected = TRUE (enables F5 continue)
        ld      a, e
        cp      08dh
        jr      nz, not_ending
        ld      a, 1
        call    04107h  ; prevent gfx corruption in ending titles
        ld      a, e
not_ending:
        di
        ld      a, 16
        ld      (07000h), a
        call    music_start
        ld      (hl), a
        ret

initialize:
        xor     a
        call    0509fh
        jp      05dabh


; -----------------------------------------------------------
; hook to initialize music player on game boot

        output vkiller_patch00099.bin
        call    initialize


; -----------------------------------------------------------
; The code below lives in nemesis 3 SCC player mapper banks

        output vkiller_patch21ee8.bin
        org     07ee8h

write_psg:
        cp      4
        ret     z
        cp      5
        ret     z

        cp      10
        ret     z

        cp      7
        jr      nz, not_register_seven

        ; if the game is paused, don't write PSG ch7
        ; this is to prevent interference with the game paused jingle
        ld      a, (02280h)
        and     2
        ret     nz  ; paused

        ; combine vkiller player bits with our own bits
        push    de
        push    hl
        ld      a, e
        or      00100100b
        ld      e, a
        ld      hl, 0c097h
        ld      a, (hl)
        or      00011011b
        and     e
        ld      (hl), a  ; write combined bits back to vkiller state
        pop     hl
        pop     de
        ld      e, a
        ld      a, 7
not_register_seven:
        out     (0A0h), a  ; set register
        push    af
        ld      a, e
        out     (0A1h), a  ; write value
        pop     af
        ret

map_slots:
        ; map RAM into bank 0000-3fff
        ; returns original value of #ffff in a
        ; returns original slot select in b/c
        ld      c, 0a8h
        in      b, (c)
        push    bc
        push    hl
        ld      a, b
        or      03h
        out     (c), a

        ; SOFAROM uses these addresses for SCC patching
        ; to take into account that we map RAM into page 0, we need
        ; to change these values. this is a SOFAROM specific hack
        ld      (0f6ebh), a
        ld      a, (0f6eah)
        or      03h
        ld      (0f6eah), a

        ; get subslot from page 3 (c000-ffff) and apply to page 0 (0000-3fff)
        ld      hl, 0ffffh
        ld      a, (hl)
        cpl
        push    af
        ld      b, a
        and     011000000b
        rlca    
        rlca
        ld      c, a
        ld      a, b
        and     011111100b
        or      c
        ld      (hl), a

        ; map music data using konami SCC mapper
        ld      a, 17
        ld      (09000h), a
        ld      a, 18
        ld      (0b000h), a

        ld      a, 1
        out     (0fch), a

        pop     af
        pop     hl
        pop     bc
        ret

music_start:
        di

        call    map_slots

        push    bc
        push    hl
        push    af

        ; interpret the command
        ld      a, e
        cp      0xfa  ; 0xfa and higher = commands: fade out, pause, etc.
        jr      nc, music_start_command
        or      a
        jr      z, music_stop
        and     0x80  ; 0x80 and higher = start song
        jr      z, music_start_skip  ; anything else = play SFX etc

        ; start playing a new song
        ld      a,e
        and     07fh
        add     a, 6

        ; clear music player state
        push    bc
        push    de
        ld      hl, 02000h
        ld      de, 02001h
        ld      bc, 00500h
        ld      (hl), 0
        ldir
        pop     de
        pop     bc

        jr      music_start_call

music_stop:
        ; clear music player state
        push    bc
        push    de
        ld      hl, 02000h
        ld      de, 02001h
        ld      bc, 00300h
        ld      (hl), 0
        ldir
        pop     de
        pop     bc

        ld      a, 081h
        jr      music_start_call

music_start_command:
        and     07h
        ld      d, 0
        ld      e, a
        ld      hl, command_convert_table
        add     hl, de
        ld      a, (hl)

music_start_call:
        push    bc
        call    06003h  ; nemesis 3 song start function
        pop     bc

music_start_skip:

        pop     af
        ld      (0ffffh), a
        pop     hl
        pop     bc

        ; restore BIOS ROM       
        out     (c), b

        di
        ld      a, 14
        ld      (09000h), a
        ld      (0f0f2h), a
        ld      a, 15
        ld      (0b000h), a
        ld      (0f0f3h), a
        ld      a, (0f0f1h)
        ld      hl, 07000h
        ret

music_update:
        push    bc
        push    de
        push    hl
        push    ix
        push    iy

        call    map_slots

        push    bc
        push    af

        call    06006h  ; nemesis 3 song update function

        pop     af
        ld      (0ffffh), a

        ; set a flag which vkiller uses to know whether music is playing
        ld      a,(020c0h)
        ld      (0c0a7h), a

        ; restore ROM
        pop     bc
        out     (c), b
ram_not_initialised:
        ld      a, 14
        ld      (09000h), a
        ld      a, 15
        ld      (0b000h), a
        ld      a, (0f0f1h)

        pop     iy
        pop     ix
        pop     hl
        pop     de
        pop     bc
        ret

command_convert_table:
        db      0     ; 0f8h = ?
        db      0     ; 0f9h = ?
        db      0     ; 0fah = ?
        db      082h  ; 0fbh = pause (hourglass)
        db      081h  ; 0fch = unpause (hourglass)
        db      082h  ; 0fdh = pause (F1)
        db      081h  ; 0feh = unpause (F1)
        db      084h  ; 0ffh = fade out

end_of_program:
        assert end_of_program < 0c000h


; -----------------------------------------------------------
; Disable SCC player PSG channel used for vkiller SFX

        ;output vkiller_patch203ad.bin
        ;org     063adh
        ;nop
        ;nop
        ;nop

        ;output vkiller_patch203b9.bin
        ;org     063b9h
        ;nop
        ;nop
        ;nop

        ;output vkiller_patch203c52.bin
        ;org     063c52h
        ;nop
        ;nop
        ;nop


;----------------------------------------------
; when SCC player is paused, pause ALL channels
; (original version keeps one channel playing (the SFX channel?)

        output vkiller_patch20399.bin
        ret nz
        nop
        nop


;--------------------------------------------------
; disable vampire killer PSG music-only channels

        ;output vkiller_patch1c9aa.bin  ; doesnt actually work!
        ;nop
        ;nop
        ;nop

        ;output vkiller_patch1c9b3.bin  ; doesnt actually work!
        ;nop
        ;nop
        ;nop

        ;output vkiller_patch1c9bc.bin
        ;nop
        ;nop
        ;nop


;------------------------------------------------
; stop vkiller music playing 

        output vkiller_patch010c6.bin
        jp      05131h

;-------------------------------------------------
; Data to make Game Master 2 work
; 
; This is a header at the start of the rom that contains the RC code
; and information about how to change the starting stage and number
; of lives.
; when we expand the vampire killer ROM to 256K, Game Master 2 no
; longer recognizes the game. to fix this we need to change
; the format of this header

        output vkiller_patch00010.bin
        db     043h, 044h, 007h, 044h, 0B8h, 000h, 0C0h, 004h
        db     000h, 011h, 0C3h, 010h, 0C4h, 005h, 0C4h, 000h
