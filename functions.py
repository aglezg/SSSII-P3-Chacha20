# ----------------------------------------------------------------------------------------
# Práctica 3: Generador Chacha20.
# Asignatura: Seguridad en Sistemas Informáticos
# Fecha de entrega: 17/03/2022
# Autor:
# - Adrián González Galván
# - alu0101321219@ull.edu.es
# ----------------------------------------------------------------------------------------
# En este fichero se encuentran las funciones utilizadas para el desarrollo de la práctica.
# ----------------------------------------------------------------------------------------

from ctypes import sizeof
from operator import mod
import os

CONSTANT_expa = '61707865'
CONSTANT_nd3 = '3320646e'
CONSTANT_2by = '79622d32'
CONSTANT_tek = '6b206574'

ROUNDS = 20

HEXADECIMAL_DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
  'a', 'b', 'c', 'd', 'e', 'f']

# Limpia la pantalla de la terminal
def cleanTerminal():
  os.system('cls' if os.name == 'nt' else 'clear')

# Comprueba si un digito es un digito hexadecimal
def isHexadecimalDigit(digit):
  if (digit in HEXADECIMAL_DIGITS):
    return True
  return False

# Comprueba que un elemento del estado sea válido
def isValidKeyElement(element):
  if (len(element) != 8):
    return False
  else:
    for i in element:
      if (isHexadecimalDigit(i) == False):
        return False
  return True

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

# ROTL
def ROTL(a, b):
  return ((a << b) & 0xffffffff) | a >> (32 - b)

# QR
def QR(x, a, b, c, d):
  x[a] = (x[a] + x[b]) & 0xffffffff
  x[d] ^= x[a]
  x[d] = ROTL(x[d], 16)
  
  x[c] = (x[c] + x[d]) & 0xffffffff
  x[b] ^= x[c]
  x[b] = ROTL(x[b], 12)
  
  x[a] = (x[a] + x[b]) & 0xffffffff
  x[d] ^= x[a]
  x[d] = ROTL(x[d], 8)
  
  x[c] = (x[c] + x[d]) & 0xffffffff
  x[b] ^= x[c]
  x[b] = ROTL(x[b], 7)

# chacha_block
def chachaBlock(state, print_state: bool = False):
  original_state = []

  for i in range(len(state)):
    original_state.append(state[i]) 

  round = 0
  while round < ROUNDS:
    # Odd round
    QR(state, 0, 4, 8, 12)
    QR(state, 1, 5, 9, 13)
    QR(state, 2, 6, 10, 14)
    QR(state, 3, 7, 11, 15)
    # Even round
    QR(state, 0, 5, 10, 15)
    QR(state, 1, 6, 11, 12)
    QR(state, 2, 7, 8, 13)
    QR(state, 3, 4, 9, 14)
  
    round += 2

  if (print_state):
    print("\n\n ESTADO FINAL tras 20 iteraciones:\n")
    printState(state)

  result = []
  for i in range(len(state)):
   result.append((original_state[i] + state[i]) & 0xffffffff)
   
  return result