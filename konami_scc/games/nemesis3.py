"""
Info for parsing Nemesis 3 music
"""
from konami_scc.common import Commands, COMMANDS_COMMON

NAME = 'nemesis3'

MEMORY_DUMPS = ['nemesis3.bin']

TRACKS_START_ADDRESS = 0x35aa
NUM_SONGS = 72

COMMANDS = COMMANDS_COMMON + [
    (Commands.INSTRUMENT, [0xf8]),
    (Commands.NO_PARAM, [0xf5]),  # this player version has no separate 'SET_LOOP' command
    (Commands.LOOPGOTO, [0xfb]),
    (Commands.SINGLE_PARAM, [0xdb, 0xe7, 0xea, 0xed, 0xee, 0xf1, 0xf2, 0xf7, 0xfe]),
    (Commands.DOUBLE_PARAM, [0xd6, 0xd7, 0xdd, 0xe1, 0xe6, 0xeb]),
]

VST_MODE = 0


def apply_command(state, cmd, *params):
    """Let a command modify the current state"""
    if cmd == 0xfe:
        for x in range(0xeb, 0xf8):
            state.commands.pop(x, None)
    # reset commands for V1 player
    if cmd == 0xf0:
        state.commands.pop(0xf1, None)
        state.commands.pop(0xf2, None)
        state.commands.pop(0xf3, None)
        return
    if cmd == 0xf6:
        state.commands.pop(0xf4, None)
        state.commands.pop(0xf5, None)
        return
    if cmd == 0xec:
        state.commands.pop(0xeb, None)
        return
    if cmd == 0xef:
        state.commands.pop(0xee, None)
        return
    if cmd == 0xe8:
        state.commands.pop(0xe6, None)
        state.commands.pop(0xe7, None)
        return
    # dc resets the state for db/dd
    # note: originally I made db/dd mutually exclusive
    # but that ended up with a dd command being sent with 0's
    # which then hangs the player
    if cmd == 0xdc:
        state.commands.pop(0xdb, None)
        state.commands.pop(0xdd, None)
        return
    # d6/d7/d8 are mutually exclusive
    # d8 is the default (off) state
    if cmd == 0xd8:
        state.commands.pop(0xd6, None)
        state.commands.pop(0xd7, None)
        return
    if cmd == 0xd6:
        state.commands.pop(0xd7, None)
    if cmd == 0xd7:
        state.commands.pop(0xd6, None)
    state.set(cmd, *params)


def state_to_controllers(state, channel):
    """Convert state to a series of MIDI CC controller settings"""
    result = []
    value = state.get(0xfe, 1)
    value = value & 0x7f  # FIXME: in some rare cases, the top bit is set
    if channel >= 3:
        value |= 8  # SCC?
    result.append((85, value,))  # SCC/PSG channel mode
    value = state.get(0xea, 0)
    result.append((22, (value >> 4) * 8,))
    result.append((7, (value & 0xf) * 8,))
    value = state.get(0xeb, 0)
    result.append((71, ((value >> 12) & 0xf) * 8,))
    result.append((72, ((value >> 8) & 0xf) * 8,))
    result.append((73, ((value >> 4) & 0xf) * 8,))
    result.append((74, (value & 0xf) * 8,))
    value = state.get(0xf1, 0)
    result.append((78, (value >> 4) * 8,))
    result.append((79, (value & 0xf) * 8,))
    value = state.get(0xf2)
    if value is None:
        result.append((14, 0,))
    else:
        result.append((14, 1 + value * 4,))
    value = state.get(0xed, 0)
    result.append((15, (value >> 4) * 8,))
    result.append((16, (value & 0xf) * 8,))
    value = state.get(0xdb, 0)
    result.append((17, (value & 0xf) * 8,))  # TODO: fix overflow
    value = state.get(0xdd, 0)
    result.append((18, ((value >> 12) & 0xf) * 8,))
    result.append((19, ((value >> 8) & 0xf) * 8,))
    result.append((20, ((value >> 4) & 0xf) * 8,))
    result.append((21, (value & 0xf) * 8,))
    value = state.get(0xee, 0)
    result.append((23, value * 4,))
    value = state.get(0xf8, 0)
    if value < 128:
        result.append((9, (value & 0x7f),))
        result.append((12, 0,))
        result.append((13, 0,))
    else:
        result.append((9, ((value >> 8) & 0x7f),))
        result.append((12, (value & 0x3f) * 2,))
        result.append((13, ((value >> 6) & 0x3) * 32,))
    return result

TRACKS = [
    (73, "The Universe of Blackness"),
    (61, "Memories"),
    (71, "Equipment"),
    (5, "We Followed The Sun"),
    (6, "Feel Pleasure to The Death"),
    (4, "Fighter Blood"),
    (3, "The Position Light"),
    (7, "Space Traveler"),
    (62, "Strangers in Time Space"),
    (9, "Gradius Boss"),
    (10, "Salamander Boss"),
    (8, "Gradius2 Boss"),
    (11, "Dance of Middle Easterners"),
    (67, "Hellraiser"),
    (68, "Galactic Desert"),
    (69, "From Ancient Times"),
    (12, "Cosmic Heroes"),
    (70, "Close Quarters"),
    (13, "Prophecy"),
    (65, "Trust Me I Will Save You"),
    (63, "The King of Diamonds"),
    (72, "Give My Heart to You"),
    (64, "The Suggestion"),
    (60, "Mirage"),
]
