#!/usr/bin/env python3
import math

DEFAULT_BLOCK_SIZE = 256        # - OBSOLETE


# Prend une chaîne de charactères m et la retourne en forme de nombre. Ce nombre est formé en contatenant les codes
# ASCII de chaque lettre du message, puis en convertissant le string de codes ASCII hexadécimaux en un int
def messageToNumber(m):
    m = str(m)      # Juste pour être sûr
    hexstring = ""

    for c in m:
        ccode = ord(c)
        hexstring += "%02x" % ccode     # %x prend un int et le colle sous forme hexadécimale

    # String en base 16 --> int
    return int(hexstring, 16)


# Prend un nombre et le transforme en sa chaîne de charactères originale
def numberToMessage(n):
    n = hex(n)
    m = ""

    for i in range(2, len(n), 2):
        c = int("0x" + n[i:i+2], 16)
        m += chr(c)

    return m

# --------------------------------------------------------------------------------
# -- Tests de différentes méthodes de séparation de texte ; ne fonctionnent pas --
# -- Pas eu le temps de bien implémenter un chiffrement par blocs.              --
# --------------------------------------------------------------------------------


# - FONCTION TEST, NE PAS UTILISER
# Prend un string et le convertit en blocs d'entiers de taille donnée
def stringToBlockList(message, blockSize=DEFAULT_BLOCK_SIZE):
    blockList = []

    for i in range(0, len(message), blockSize):
        blockList.append(messageToNumber(message[i:i+blockSize]))

    print(blockList)

    return blockList


# - FONCTION TEST, NE PAS UTILISER
# Prend une liste de blocs, convertit chaque bloc en texte puis retourne le string complet
def blockListToString(blockList):
    string = ""

    for block in blockList:
        string += numberToMessage(block)

    print(string)

    return string


# - FONCTION TEST, NE PAS UTILISER
# Prend un string et le crypte en le séparant en blocs
def encryptString(message, key):
    e, n = key

    if messageToNumber(message) >= n:
        blockSize = n/2
        numberOfBlocks = math.ceil(messageToNumber(message)/blockSize)
    else:
        blockSize = 1
        numberOfBlocks = 1

    for i in range(0, numberOfBlocks):
        for j in range(0, blockSize):
            return message[i]


if __name__ == "__main__":      # Si ce module est le main
    ctest = encryptString("Hello World!", (5, 35))
    print(ctest)
