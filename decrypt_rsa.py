import math
import time
import os
import json
from pylab import *
from random import randint

MESSAGE = 65 #message brut
ITERATIONS = 3 #nombre d'itérations pour la modélisation
LIMITE = 2000 #représente l'index de ligne à ne pas dépasser dans 'entiers_premiers.txt' . Cela permet de ne pas prendre n trop grand (dépassement mémoire) VALEUR MAX = 216815

fichier = open('entiers_premiers.txt','r')
liste = fichier.readlines()
fichier.close()



def chiffrer(m, n,e):
    en = m**e
    return en % n

def calculClePrivee(phi,e):
    d=2
    for i in range(100):
        x = 1 + i*phi
        if x%e==0:
            d = x//e
            break
    return d
def showPourcentage(p):
    clear = lambda: os.system('cls')
    clear()
    pgbar = "["
    for i in range (100):
        if i<p:
            pgbar+="|"
        else:
            pgbar+="."
    pgbar+="]"
    print(pgbar)

def genererTest():#permet de génerer deux nombres p et q constituant les clés
    p = int(liste[randint(5,LIMITE)].rstrip("\n"))
    q = int(liste[randint(5,LIMITE)].rstrip("\n"))
    if p==q:
        return genererTest()
    else:
        return (p,q)
def modelisation():
    abs = []
    temps= []
    for i in range(ITERATIONS):#chaque tour de boucle correspond à un déchiffrement
        p,q = genererTest()
        n = p*q #n est public (à l'inverse de p et q)
        phi_n= (p-1)*(q-1)
        k=2
        while math.gcd(phi_n,k)!=1:
            k=k+1
        e = k #exposant (fait partie de la clé publique)
        m_crypte = chiffrer(MESSAGE,n,e)

        #Début de la décomposition en éléments simples (=début du déchiffrement)
        debut = time.time()
        k = 0
        while k<len(liste) and n%int(liste[k].rstrip("\n"))!=0:
            k=k+1
        decomp_inf = int(liste[k].rstrip("\n"))
        decomp_sup = n//decomp_inf
        phi_n= (decomp_inf-1)*(decomp_sup-1)
        cle_priv = calculClePrivee(phi_n,e)
        m_decrypte = (m_crypte**cle_priv)%n
        fin =time.time()
        #Fin du calcul (=message déchiffré)
        temp_calcul = fin - debut
        if MESSAGE!=m_decrypte:#en cas d'erreur
            print("[ERREUR] n : " + str(n)+",  p: "+str(p)+", q: "+str(q), ", e: "+str(e)+", d: "+str(cle_priv), ", message décrypté: "+ str(m_decrypte) + ", message crypté: "+str(m_crypte))
        else:
            abs.append(n)#ajoute en abscisse le nombre de chiffre de n
            temps.append(float("{:.5f}".format(temp_calcul)))#ATTENTION=>les temps sont en s
            showPourcentage((i/ITERATIONS)*100)
    return abs,temps

#x,y = modelisation()
#fichier_sauv = open('calculs.json')
#sauvegarde = json.load(fichier_sauv)
#fichier_sauv.close()

#for i in range(len(x)):
    sauvegarde[0].append(x[i])
    sauvegarde[1].append(y[i])
#fichier_sauv = open('calculs.json','w')
#json.dump(sauvegarde,fichier_sauv)
#fichier_sauv.close()

fichier_sauv = open('calculs.json')
sauvegarde = json.load(fichier_sauv)
fichier_sauv.close()
plt.plot(sauvegarde[0],sauvegarde[1],'o',marker='.')
plt.xscale('log')
plt.ylabel('Temps de déchiffrement (en s)')
plt.xlabel('Valeur de la clé')
plt.title('Temps de déchiffrement en fonction de la valeur de la clé.')
plt.show()