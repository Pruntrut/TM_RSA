#!/usr/bin/env python3
import time
import timeit

from TM_RSAMaths import powerMod


# Décorateur qui est enrobé autour d'une fonction que l'on désire chonométrer. Il exécute la fonction originale mais
# permet de rajouter des instrucions sans réécrire la fonction.
# Entoure une fonction que l'on désire chonométrer
def myTimer(wrapped):
    def wrapper(*args, **kwargs):
        global timings

        tdebut = time.clock()
        result = wrapped(*args, **kwargs)       # Exécution de la fonction originale
        tfin = time.clock()

        timings.append(tfin - tdebut)
        print("Function %s took %f seconds" % (wrapped.__name__, tfin - tdebut))
        return result

    return wrapper


# -- OBSOLETE
# Ceci est la méthode timeit, qui n'a pas été utilisée en fin de compte, car il n'était pas possible d'incrémenter la
# puissance au fur et à mesure comme avec la méthode du décorateur. La méthode timeit fonctionne avec un string
# contenant les instructions à répéter, qui est passé à un objet Timer. Quand on appelle la méthode Timer.timeit(), on
# exécute le code un certain nombre de fois et retourne le temps nécessaire (cela permet de prendre un temps moyen).
"""

powerModSource = '''
def powerMod(b, e, m = 0):
    x = 1
    e = bin(e)[2:]


    if m > 0:
        for i in e:
            x = x**2 % m
            if i == "1":
                x = x*b % m

        return x
    else:
        for i in e:
            x = x**2
            if i == "1":
                x = x*b

        return x

powerMod(2876, 4578, 786)'''

"""
# -- FIN OBSOLETE


# On affecte les variables
timings = []
powerList = range(0, 10000, 250)
base = 1976620216402300889624482718775150
modulo = 1174834798455295478692610950681

# -----------
# On teste l'exp. modulaire rapide "faite-maison"
powerMod = myTimer(powerMod)        # Eveloppement de powerMod() par le décorateur (ce qui permet le chronométrage)

for i in powerList:
    powerMod(base, i, modulo)

print(timings)
timings = []

# -----------
# On teste la version par défaut de python.
pow = myTimer(pow)

for i in powerList:
    pow(base, i, modulo)

print(timings)
timings = []

# -----------
# On teste la méthode standard a**b % c avec powerlist.
for i in powerList:
    t0 = time.clock()
    base ** i % modulo
    t1 = time.clock()
    timings.append(t1-t0)

print(timings)


# -- OBSOLETE
# Suite de la méthode timeit
"""
t1 = timeit.Timer("2876 ** 4578 % 786")
print("Straightforward: %f" % t1.timeit(1))

t2 = timeit.Timer(powerModSource)
print("Homemade: %f" % t2.timeit(1))

t3 = timeit.Timer("pow(2876, 4578, 786)")
print("Python pow: %f" % t3.timeit(1))
"""
# -- FIN OBSOLETE
