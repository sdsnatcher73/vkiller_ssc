"""
Common conversion code shared by all games
"""
from collections import defaultdict


class Commands:
    """Commands that the player can execute"""
    NO_PARAM = 'NO_PARAM'
    SINGLE_PARAM = 'SINGLE_PARAM'
    DOUBLE_PARAM = 'DOUBLE_PARAM'
    TRIPLE_PARAM = 'TRIPLE_PARAM'
    QUAD_PARAM = 'QUAD_PARAM'
    TEMPO = 'TEMPO'
    SET_LOOP = 'SET_LOOP'
    LOOP1 = 'LOOP1'
    LOOP2 = 'LOOP2'
    LOOPGOTO = 'LOOPGOTO'
    CALL = 'CALL'
    RTN = 'RTN'
    GOTO = 'GOTO'
    END = 'END'
    INSTRUMENT = 'INSTRUMENT'
    NOTE_ON = 'NOTE_ON'
    NOTE_OFF = 'NOTE_OFF'
    OCTAVE = 'OCTAVE'
    COMMAND_F0 = 'COMMAND_F0'


COMMANDS_COMMON = [
    (Commands.TEMPO, [0xe9]),
    (Commands.SET_LOOP, [0xf5]),
    (Commands.CALL, [0Xf9]),
    (Commands.RTN, [0xfa]),
    (Commands.LOOP1, [0xfb]),
    (Commands.LOOP2, [0xfc]),
    (Commands.GOTO, [0xfd]),
    (Commands.END, [0xff]),
]


def generate_command_map(commands_table):
    """Generate a command map which turns command IDs into command enum commands"""
    commands = defaultdict(None)
    for cmd in range(0, 0xc0):
        commands[cmd] = Commands.NOTE_ON
    for cmd in range(0xc0, 0xd0):
        commands[cmd] = Commands.NOTE_OFF
    for cmd in range(0xd0, 0xd6):
        commands[cmd] = Commands.OCTAVE
    for func, cmds in commands_table:
        for cmd in cmds:
            # assert cmd not in commands, 'Multiply defined command %02x' % cmd
            commands[cmd] = func
    return commands


def generate_reverse_command_map(commands_table):
    """Generate a command map which turns enum commands into command IDs"""
    cmd_map = generate_command_map(commands_table)
    commands = {}
    for byte, command in cmd_map.items():
        if command not in commands:
            commands[command] = byte
    return commands
