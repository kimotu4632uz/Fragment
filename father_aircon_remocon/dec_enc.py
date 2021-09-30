#!/usr/bin/env python
from pathlib import Path
import json

t = 870

def in_range(min, target, max):
  return min < target and target < max

def decode(code):
  code_body = code[2:66] + code[68:132] + code[138:202] + code[204:268]

  bytes = []
  for i in range(0, 16):
    byte = 0
    for j in range(0, 8):
      first_idx = (i*8 + j)*2
      if in_range(700, code_body[first_idx], 1000) and in_range(700, code_body[first_idx + 1], 1000):
        byte |= (0 << j)
      elif in_range(700, code_body[first_idx], 1000) and in_range(2000, code_body[first_idx + 1], 3000):
        byte |= (1 << j)
      else:
        print(f'{i}: {code_body[i]}, {code_body[i+1]}')
    bytes.append(byte)

  return bytes


def encode(bytes):
  frames = []
  result = []

  for i in range(0,2):
    code = []
    i *= 8
    code.append(4*t)
    code.append(4*t)

    for byte in bytes[i:i+4]:
      for j in range(8):
        if byte & 1 == 0:
          code.append(t)
          code.append(t)
        else:
          code.append(t)
          code.append(3*t)
        byte >>= 1
 
    code.append(4*t)
    code.append(4*t)

    for byte in bytes[i+4:i+8]:
      for j in range(8):
        if byte & 1 == 0:
          code.append(t)
          code.append(t)
        else:
          code.append(t)
          code.append(3*t)
        byte >>= 1
 
    code.append(4*t)
    code.append(4*t)
    code.append(t)

    frames.append(code)
  
  for frame in frames[:-1]:
    result.extend(frame)
    result.append(14000)
  result.extend(frames[-1])

  return result


def check(code):
  result = []
  for c in code:
    if in_range(700, c, 1000):
      result.append(t)
    elif in_range(2000, c, 3000):
      result.append(3*t)
    elif in_range(3000, c, 4000):
      result.append(4*t)
    else:
      print(c)
      result.append(c)
  
  return result



if __name__ == '__main__':
  codes = json.loads(Path('codes.json').read_text())
  bytes = decode(codes['father_27'])
  
  for i in range(0, 4):
    line_1 = []
    line_2 = []
    for byte in bytes[i*4:(i+1)*4]:
      line_1.append('     0x{:02x}'.format(byte))
      line_2.append('{:04b} {:04b}'.format(byte >> 4, byte & 0xf))
    print(' '.join(line_1))
    print(' '.join(line_2))