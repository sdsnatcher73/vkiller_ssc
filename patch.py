"""
Patch a .rom file from Konami4 to Konami5 (SCC) mapper
"""
import glob#
import subprocess


def loadrom(filename):
    """Load a rom file"""
    with open(filename, 'rb') as stream:
        return bytearray(stream.read())

def patch_mapper(rom):
    """Patch mapper writes from Konami4 to Konami5"""
    for offset in range(len(rom) - 2):
        if (rom[offset] == 0x32 and
            rom[offset + 1] == 0x00 and
            rom[offset + 2] in [0x60, 0x80, 0xa0]):
            rom[offset + 2] += 0x10

PATCH_IGNORE_LIST = [0x20daa, 0x23340, 0x21171]
CHANNEL_OFFSET = -0x16  # 0e00h -> 0cb00h

def patch_music_channel_locations(rom):
    """Patch scc player to move channel data locations"""
    for offset in range(0x20000, len(rom) - 4):
        if offset in PATCH_IGNORE_LIST:
            continue
        if (rom[offset] == 0xdd and
            rom[offset + 1] == 0x21 and
            (rom[offset + 3] & 0xfc) == 0xe0):
            rom[offset + 3] += CHANNEL_OFFSET
        if (rom[offset] in [0x01, 0x11, 0x21, 0x32, 0x3a] and
            (rom[offset + 2] & 0xfc) == 0xe0):
            rom[offset + 2] += CHANNEL_OFFSET
            print(hex(offset))


rom = loadrom('vkiller.rom')

patch_mapper(rom)
patch_music_channel_locations(rom)


subprocess.call(['cmd.exe', '/c', 'del', 'vkiller_patch*.bin'])

# compile patches
try:
    subprocess.check_output(['sjasmplus', 'vkiller_scc.asm'])
except subprocess.CalledProcessError as exc:
    print(exc.output)
    exit(-1)

# apply patches
patches = glob.glob('vkiller_patch*.bin')
for patch_filename in patches:
    offset = int(patch_filename[13:18], 16)
    data = loadrom(patch_filename)
    for i in range(len(data)):
        rom[offset + i] = data[i]

with open('vkiller_scc.rom', 'wb') as stream:
    stream.write(rom)

print('done')