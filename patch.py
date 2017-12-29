"""
Patch a .rom file from Konami4 to Konami5 (SCC) mapper
"""
import glob
import subprocess
import hashlib

from konami_scc.compile import compile
from konami_scc.games import nemesis3


def loadrom(filename):
    """Load a rom file"""
    with open(filename, 'rb') as stream:
        return bytearray(stream.read())


def check_hash(data, expected_hash):
    """Check that the data is what we expect"""
    h = hashlib.md5(data).hexdigest()
    assert h == expected_hash, 'Incorrect hash. Are you using the right ROM?'


def patch_mapper(rom):
    """Patch mapper writes from Konami4 to Konami5"""
    for offset in range(len(rom) - 2):
        if (rom[offset] == 0x32 and
            rom[offset + 1] == 0x00 and
            rom[offset + 2] in [0x60, 0x80, 0xa0]):
            rom[offset + 2] += 0x10

PATCH_IGNORE_LIST = [0x20daa, 0x23340, 0x20beb]
CHANNEL_OFFSET = -0xc0  # 0e00h -> 02000h

def patch_music_channel_locations(rom):
    """Patch scc player to move channel data locations"""
    for offset in range(0x20000, 0x213f0):
        if offset in PATCH_IGNORE_LIST:
            continue
        if (rom[offset] == 0xdd and
            rom[offset + 1] == 0x21 and
            (rom[offset + 3] & 0xfc) == 0xe0):
            rom[offset + 3] += CHANNEL_OFFSET
        if (rom[offset] in [0x01, 0x11, 0x21, 0x32, 0x3a, 0x22, 0x2a] and
            (rom[offset + 2] & 0xfc) == 0xe0):
            rom[offset + 2] += CHANNEL_OFFSET


def patch_bios_psg_calls(rom):
    """Patch replace calls to bios psg_write function with our own function"""
    for offset in range(0x20000, len(rom) - 4):
        if (rom[offset] == 0xcd and
            rom[offset + 1] == 0x93 and
            rom[offset + 2] == 0x00):
            rom[offset + 1] = 0xe8;
            rom[offset + 2] = 0x7e;


rom = loadrom('vkiller.rom')
scc_rom = loadrom('nemesis3.rom')
check_hash(rom, '66da3107684286d1eba45efb8eae9113')
check_hash(scc_rom[0x14000:0x1a000], '61c33112a5a2cefd1df81dc1434aa42a')

rom = rom + scc_rom[0x14000:0x1a000] + b' ' * 0x1a000

patch_mapper(rom)
patch_music_channel_locations(rom)
patch_bios_psg_calls(rom)


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

compile('mml\\vkiller_scc.mml', rom, nemesis3, 0x1a000, 0x7510, 0x8000)

with open('vkiller_scc.rom', 'wb') as stream:
    stream.write(rom)

kss = loadrom('nemesis3.kss')
compile('mml\\vkiller_scc.mml', kss, nemesis3, -0x5fb0, 0x7506, 0x7ea4, hack=True)

with open('vkiller_scc.kss', 'wb') as stream:
    stream.write(kss)

print('done')
