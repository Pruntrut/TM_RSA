#!/usr/bin/env python3
from TM_RSAPrimeGen import generateTwoLargePrimes
from TM_RSAMaths import *
from TM_RSAText import *

entre = input("Entrez votre message : ")
message = messageToNumber(entre)

p, q = generateTwoLargePrimes(1024)

publicKey = generatePublicKey(p, q)
privateKey = generatePrivateKey(p, q, publicKey[0])

c = encrypt(message, publicKey)
print("c:", c)
m = decrypt(c, privateKey)
print("m décrypté:", m)

m_decrypté = numberToMessage(m)
print("Votre message était : %s" % m_decrypté)
