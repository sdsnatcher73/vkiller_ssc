        output vkiller_patch00038.bin
        org     04038h

        call    music_update_shim



        output  vkiller_patch010b6.bin
        org     050b6h

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



        output vkiller_patch25f30.bin
        org     0bf30h

music_start:
        ;di
        ;ld      a, 15
        ;ld      (05000h), a
        ;ld      a, 0
        ;ld      (05000h), a
        ld      hl, 0b000h
        ld      a, 15
        ret

music_update:
        ;di
        ;ld      a, 15
        ;ld      (05000h), a
        ;ld      a, 0
        ;ld      (05000h), a
        ld      a, 15
        ret
