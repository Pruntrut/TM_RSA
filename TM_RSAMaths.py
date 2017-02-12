#!/usr/bin/env python3
import logging
import random

# Configuration du débugage
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Trouve le plus grand diviseur commun de a et b 
def gcd(a, b):
    logging.debug("Starting search for gdc")
    
    while a != 0:
        a, b = b % a, a
    
    logging.debug("Found gdc: %d", b)
    return b


# Retourne l'inverse modulaire de e (d) en utilisant l'algorithme étendu d'euclide 
def extendedEuclid(a, b):
    u, u1 = 0, 1            # Affectation parallèle des variables (évite les variables intermédiaires)
    v, v1 = 1, 0 
    r, r1 = b, a
    
    logging.debug("Start of Ext Euclidean Alg")
    
    while r1 != 0:
        q = r//r1           # On calcule le quotient
        r, r1 = r1, r-r1*q
        u, u1 = u1, u-u1*q
        v, v1 = v1, v-v1*q
    
    logging.debug("Ext Euclid Alg done!")
    logging.debug("Found r=%d u=%d v=%d" % (r, v, u))
    
    return r, u, v


# Génère la clé publique, utiliser e=65537 par défaut (standard)
def generatePublicKey(p, q, e=65537):
    logging.debug("Generating public key...")

    n = p * q

    # Si e n'est pas premier avec phi(n), on ne pourrait pas trouver l'inverse modualire
    i = 0
    listOfEValues = [65537, 257, 17, 5, 3]

    while gcd(e, (p-1)*(q-1)) != 1:
        if i < 4:
            e = listOfEValues[i]        # On parcourt une liste de valeurs de e fréq. utilisées
            i += 1
        else:
            e = random.randint(3, round(n/2))  # Sinon, on génère des nombres (pas trop grand) jusqu'à en trouver un bon

    logging.debug("Public key done!")
    logging.debug("Found e=%d n=%d" % (e, n))
    
    return e, n


# Génère la clé privée
def generatePrivateKey(p, q, e):
    logging.debug("Generating private key...")

    if gcd(e, (p-1)*(q-1)) != 1:   # Vérification que pgdc(e, phi(n)) = 1 au cas où
        raise Exception("Improper public exponenent used! %d is not coprime with phi(n)!" % e)

    n = p*q
    totient = (p-1)*(q-1)
    d = extendedEuclid(totient, e)[2]

    if d < 0:           # Si d est négatif, ajoute phi(n) une fois pour le rendre positif (pas d'effet à part rendre les
        d += totient    # calculs plus rapides pour un ordinateur), car on veut 0 <= d < phi(n)

    logging.debug("Private key done!")
    logging.debug("Found d=%d n=%d" % (d, n))
    
    return d, n


# Prend un tuple de clé publique et un message et le crypte
def encrypt(m, publicKey):
    logging.debug("Encrypting...")
    c = pow(m, publicKey[0], publicKey[1])
    
    logging.debug("Encrypting done !")
    logging.debug("Cyphertext: %d" % c)
    
    return c


# Prend un tuple de clé privée et un message et le décrypte
def decrypt(c, privateKey):
    logging.debug("Decrypting...")
    
    m = pow(c, privateKey[0], privateKey[1])
    
    logging.debug("Decrypting done !")
    logging.debug("Plaintext: %d" % m)

    return m


# Fait une exponentiation modulaire rapide (a^b mod c)
def powerMod(a, b, c=0):
    x = 1
    b = bin(b)[2:]

    if c > 0:
        for i in b:
            x = x**2 % c
            if i == "1":
                x = x * a % c
        
        return x
    else: 
        for i in b:
            x **= 2
            if i == "1":
                x = x * a
        
        return x
