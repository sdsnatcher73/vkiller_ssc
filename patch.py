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
    """Patch file with given filename"""

    for offset in range(len(rom) - 2):
        if (rom[offset] == 0x32 and
            rom[offset + 1] == 0x00 and
            rom[offset + 2] in [0x60, 0x80, 0xa0]):
            rom[offset + 2] += 0x10


rom = loadrom('vkiller.rom')

# patch mapper access from Konami4 to Konami5 (scc) mapper
patch_mapper(rom)


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
