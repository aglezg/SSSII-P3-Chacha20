from ctypes import sizeof
from operator import mod
import os

CONSTANT_expa = '61707865'
CONSTANT_nd3 = '3320646e'
CONSTANT_2by = '79622d32'
CONSTANT_tek = '6b206574'

# Limpia la pantalla de la terminal
def cleanTerminal():
  os.system('cls' if os.name == 'nt' else 'clear')

# Invertir palabras de 32 bits (4 bytes)
def invert(wordOf4bytes): 
  result = ''
  aux = ''
  it = 0
  while (it < len(wordOf4bytes)):
    if (it == 0 or it % 2 != 0):
      aux += wordOf4bytes[it]
    else:
      result = aux + result
      aux = wordOf4bytes[it]
    it += 1
  return aux + result

# Imprimir estado
def printState(state):
  it = 0
  for element in state:
    if (it % 4 == 0 and it != 0):
      print()
    if (type(element) is int):
      print('{:08x}'.format(element) + ' ', end = '')
    else:
      print(str(element) + ' ', end = '')
    it += 1

# Crear estado inicial
def createInitialState(key, count, nonce):
  initialState = [int(CONSTANT_expa, 16), int(CONSTANT_nd3, 16), int(CONSTANT_2by, 16), int(CONSTANT_tek, 16)]
  
  for element in key:
    initialState.append(int(invert(element), 16))

  initialState.append(int(invert(count), 16))

  for element in nonce:
    initialState.append(int(invert(element), 16))

  return initialState


state = createInitialState(['00010203', '04050607', '08090a0b', '0c0d0e0f',
  '10111213', '14151617', '18191a1b', '1c1d1e1f'], '01000000', ['00000009',
  '0000004a', '00000000'])
printState(state)