; -----------------------------------------------------------
; Code for hooking in calls to the nemesis 3 SCC player

        output  vkiller_patch00038.bin
        org     04038h

        call    music_update_shim



        output  vkiller_patch010b2.bin
        org     050b2h

        pop     af
        ld      e, a  ; save song index for later
        push    af
        nop
        call    music_start_shim



        output vkiller_patch013bf.bin
        org     053bfh  ; space: 18 bytes

        db      018h  ; jr 05383h
        db      0c2h
music_update_shim:
        ld      a, 18
        ld      (0b000h), a
        call    music_update
        ld      (0b000h),a
        ret



        output vkiller_patch0139b.bin
        org     0539bh  ; space: 12 bytes

        db      018h  ; jr 0539bh
        db      0ech
music_start_shim:
        ld      a, 18
        ld      (0b000h), a
        call    music_start
        ld      (hl), a
        ret


; -----------------------------------------------------------
; The code below lives in nemesis 3 SCC player mapper banks

        output vkiller_patch25f30.bin
        org     0bf30h

music_start:
        ld      a, 16
        ld      (07000h), a
        ld      a, 17
        ld      (09000h), a

        ; if we are starting a sound effect, ignore
        ld      a, e
        and     0x80
        jp      z,music_start_skip

        ld      a,6
        call    06003h  ; nemesis 3 song start function

music_start_skip:
        ld      a, (0f0f1h)
        ld      (07000h), a
        ld      a, 14
        ld      (09000h), a
        ld      hl, 0b000h
        ld      a, 15
        ret

music_update:
        ld      a, 16
        ld      (07000h), a
        ld      a, 17
        ld      (09000h), a

        push    bc
        push    de
        push    hl
        push    ix
        push    iy
        call    06006h  ; nemesis 3 song update function
        pop     iy
        pop     ix
        pop     hl
        pop     de
        pop     bc

        ld      a, (0f0f1h)
        ld      (07000h), a
        ld      a, 14
        ld      (09000h), a
        ld      a, 15
        ret

end_of_program:
        assert end_of_program < 0c000h



;--------------------------------------------------
; disable vampire killer PSG music-only channels

        output vkiller_patch1c9aa.bin
        nop
        nop
        nop

        output vkiller_patch1c9b3.bin
        nop
        nop
        nop


;------------------------------------------------
; stop vkiller music playing 

        output vkiller_patch010cc.bin
        jp      0513fh
