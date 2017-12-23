import re
import codecs
import os

from konami_scc.common import Commands, generate_reverse_command_map


NOTE_REGEX = re.compile('^([abcdefgr]\#?)(\d+)')
NOTES = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b', 'r']
COMMON = re.compile('^([oti])(\d+)')
COMMAND = re.compile('^@(\w+)\(([^\)]*)\)')
WHITESPACE = re.compile('^\s+')
COMMENT = re.compile('^;.*')

class ParseException(Exception):
  pass

class Data:
  def __init__(self, game, memory_offset, music_offset):
    self.data = bytearray()
    self.song_data = bytearray()
    self.tracks_data = bytearray()
    self.memory_offset = memory_offset
    self.tracks_offset = 0
    self.music_offset = music_offset
    self.symbols = {'0': None}
    self.second_pass = False
    self.commands = generate_reverse_command_map(game.COMMANDS)
    self.songs = {}

  def reset(self, second_pass):
    self.second_pass = second_pass
    self.data = bytearray()
    # calculate song table size and music data offset
    num_songs = max(self.songs.keys()) + 1
    song_table_size = num_songs * 2
    self.tracks_offset = self.memory_offset + song_table_size
    tracks_size = 0
    for song_index in range(num_songs):
      tracks = self.songs.get(song_index, ['0'] * 8)
      num_tracks = sum(0 if addr == '0' else 1 for addr in tracks)
      print(num_tracks)
      tracks_size += 2 + num_tracks * 2

  def song(self, index, channels):
    if not self.second_pass:
      self.songs[index] = channels

  def append(self, *data):
    for item in data:
      if isinstance(item, bytearray):
        self.data += item
      elif item in self.commands:
        self.data.append(self.commands[item])
      elif item >= 256:
        self.data.append(item & 0xff)
        self.data.append(item >> 8)
      else:
        self.data.append(item)

  def symbol(self, name):
    name = name.strip()
    offset = len(self.data)
    if name in self.symbols:
      if self.symbols[name] != offset:
        raise ParseException('Multiply defined symbol "%s"' % name)
    self.symbols[name] = offset
  
  def lookup(self, name):
    name = name.strip()
    if self.second_pass:
      if name not in self.symbols:
        raise ParseException('ERROR: Unresolved symbol "%s"' % name)
      addr = self.symbols[name]
      if addr is None:
        return 0
      else:
        return self.symbols[name] + self.music_offset
    else:
      return 0xfeee

  def song_output(self):
    num_songs = max(self.songs.keys()) + 1
    print('%d %04x %04x %04x %04x' % (num_songs, self.memory_offset, self.tracks_offset, self.music_offset, self.music_offset + len(self.data)))
    for song_index in range(num_songs):
      song_addr = len(self.tracks_data) + self.tracks_offset
      self.song_data.append(song_addr & 0xff)
      self.song_data.append(song_addr >> 8)
      tracks_bitmask = 0
      tracks_addresses = bytearray()
      tracks = self.songs.get(song_index, ['0'] * 8)
      for track in tracks:
        addr = self.lookup(track)
        print('%s - %04x' % (track, addr))
        tracks_bitmask <<= 1
        if addr:
          tracks_bitmask |= 1
          tracks_addresses.append(addr & 0xff)
          tracks_addresses.append(addr >> 8)
      self.tracks_data.append(tracks_bitmask)
      self.tracks_data.append(0xe0)
      self.tracks_data += tracks_addresses
    assert len(self.song_data) == num_songs * 2
    return self.song_data + self.tracks_data

  def music_output(self):
    return self.data
      

def decode_hex(text):
  return bytearray(codecs.decode(text.strip(), "hex"))


def parse(mml, output):
  try:
    for line_index, line in enumerate(mml.splitlines()):
      if ':' in line:
        index = line.index(':')
        label = line[0:index]
        line = line[index+1:]
        output.symbol(label)

      while line:
        m = NOTE_REGEX.match(line)
        if m:
          note = NOTES.index(m.group(1))
          length = int(m.group(2))
          output.append(note * 16 + length - 1)
          line = line[m.end():]
          continue
        m = COMMON.match(line)
        if m:
          cmd = m.group(1)
          value = int(m.group(2))
          if cmd == 't':
            output.append(Commands.TEMPO, value)
          elif cmd == 'o':
            if value >= 6:
              raise ParseException("Illegal octave")
            output.append(0xd0 + value)
          elif cmd == 'i':
            assert value < 128
            output.append(Commands.INSTRUMENT, value & 0xff)
          line = line[m.end():]
          continue
        m = COMMAND.match(line)
        if m:
          cmd = m.group(1)
          if cmd == 'song':
            args = m.group(2).split(',')
            song_index = int(args[0])
            channels = []
            for channel_index in range(8):
              symbol = args[channel_index + 1].strip()
              channels.append(symbol)
            output.song(song_index, channels)
          elif cmd == 'call':
            output.append(Commands.CALL, output.lookup(m.group(2)))
          elif cmd == 'rtn':
            output.append(Commands.RTN)
          elif cmd == 'loop':
            num_loops, symbol = m.group(2).split(',')
            output.append(Commands.LOOPGOTO, int(num_loops), output.lookup(symbol))
          elif cmd == 'loop2':
            num_loops, symbol = m.group(2).split(',')
            output.append(Commands.LOOP2, int(num_loops), output.lookup(symbol))
          elif cmd == 'goto':
            output.append(Commands.GOTO, output.lookup(m.group(2)))
          elif cmd == 'inst':
            output.append(Commands.INSTRUMENT, decode_hex(m.group(2)))
          elif cmd == 'cmd':
            output.append(decode_hex(m.group(2)))
          elif cmd == 'end':
            output.append(Commands.END)
          elif cmd == 'dummy':
            pass
          else:
            raise ParseException('Unrecognized command')
          line = line[m.end():]  
          continue
        m = WHITESPACE.match(line)
        if m:
          line = line[m.end():]
          continue
        m = COMMENT.match(line)
        if m:
          line = line[m.end():]
          continue

        raise ParseException("Syntax error")
  except ParseException as exc:
    print('PARSE ERROR at line %d: %s "%s"' % (line_index + 1, str(exc), line))
    exit(-1)


def compile(filename, data, game, rom_offset, song_ram_offset, music_ram_offset, hack=False):
  with open(filename) as stream:
    mml = stream.read()

  output = Data(game, song_ram_offset, music_ram_offset)
  print('pass1')
  parse(mml, output)
  output.reset(second_pass=True)
  print('pass2')
  parse(mml, output)

  # patch songs
  for index, byte in enumerate(output.song_output()):
    data[index + song_ram_offset + rom_offset] = byte

  # patch music
  for index, byte in enumerate(output.music_output()):
    offset = index + music_ram_offset + rom_offset
    if hack and offset >= 0x2050:  # this hack is needed because the .kss file has split banks
      offset += 0x4000
    data[offset] = byte

  return data
