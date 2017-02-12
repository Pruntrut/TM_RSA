import random


# -- OBSOLETE
# Génère un nombre premier d'une certaine longueur de bits!--non utilisé, remplacé par generateTwoLargePrimes
def generateLargePrime(keySize=1024):
    if keySize < 3:
        raise Exception("Key size too small")

    # Génération d'un et vérification de sa primalité
    while True:
        n = random.randrange(2 ** (keySize - 1), 2 ** keySize)
        if isPrime(n):
            return n


# Génère un tuple de 2 grands nombres premiers dans 2 intervalles contenues à l'intérieur d'une grande intervalle
def generateTwoLargePrimes(keySize=1024):
    if keySize < 3:
        raise Exception("Key size too small")

    # Génération du nbre premier p dans une intervalle entre 2^(keySize) et 2^(keySize) + 2^(keySize - 1)
    # par ex: entre 1024 (2^10) et 1536 (2^10 + 2^9)
    # On cherche le nombre premier après le nombre tiré au harsard
    p = random.randrange(2 ** keySize, 2 ** keySize + 2 ** (keySize - 1))

    if p % 2 == 0:  # Si p est pair, +1 pour permettre une incrémentation plus rapide
        p += 1

    while not isPrime(p):       # Tant que p n'est pas premier, augmenter de 2
        p += 2

    # Génération du nbre premier q dans une intervalle entre 2^(keySize) + 2^(keySize - 1) et 2^(keySize + 1)
    # par ex: entre 1536 (2^10 + 2^9) et 2048 (2^11)
    q = random.randrange(2 ** keySize + 2 ** (keySize - 1), 2 ** (keySize + 1))

    if q % 2 == 0:  # Si q est pair, +1 pour permettre une incrémentation plus rapide
        q += 1

    while not isPrime(q):
        q += 2

    return p, q


# Vérifie si un nombre n est premier
def isPrime(n):
    if n < 2:
        raise Exception("Number smaller than 2 in isPrime()")

    # liste des nbres premiers inférieurs à 1000
    smallPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                   103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                   211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                   331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                   449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                   587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                   709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                   853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                   991, 997]

    if n < 2:
        return False

    if n in smallPrimes:  # Si n est dans les nbres premiers de 1 à 1000
        return True

    # Méthode plus rapide pour déterminer si un nombre est premier, on divise n par les nbres premiers inférieurs à 1000
    for primeNum in smallPrimes:
        if n % primeNum == 0:
            return False

    # Si les méthodes ci-dessus ne fonctionnent pas, utilise Rabin-Miller pour determiner si un nombre est premier
    return rabinMiller(n)


# Retoune vrai si un nombre est premier (méthode probabilistque)
def rabinMiller(n):
    if n < 3 or n % 2 != 1:  # Le test ne marche que si les nombres sont impairs et > 3
        raise Exception("Odd number or number smaller than 3 entered into RM")

    s = n - 1
    t = 0

    while s % 2 == 0:  # Divise s par 2 tant qu'il reste entier et
        s //= 2         # on compte le nbre de pas avec t. On obient
        t += 1  # donc n-1 = (2^t)*s

    k = 0  # k traque la probabilité d'un faux résultat (prob. calculée avec 2^(-k))

    while k < 64:
        a = random.randrange(2, n - 1)  # Sécurité incertaine de la librairie random (remplacer plus tard ?)
        v = pow(a, s, n)  # a^s mod n

        if v != 1:  # quand v vaut 1, le test est validé pour la base a car a^(s*2^i) ne changera jamais
            i = 0
            while v != (n - 1):  # on cherche un a^(s*(2^i)) mod n égal à n-1 avec i augmentant dans chaque passage
                if i == t - 1:
                    return False  # si on ne trouve pas de v égal à n-1 dans a^s <= a^(s*2î) < n-1, on retourne False
                else:
                    i += 1
                    v = pow(v, 2, n)  # v^2 mod n
        k += 1  # on a diminué la proba que n ne soit pas premier d'un facteur de 4 ---> k += 1 (proba totale 4^(-k)

    # Si n a passé le test, il y a une proba de 2^(-128) que n ne soit pas premier
    return True
