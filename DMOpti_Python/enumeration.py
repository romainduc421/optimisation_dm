#!/usr/bin/env python3
import sys
#Permet de creer tout les ensemble de recette disponible
from itertools import combinations

#Ecrie dans le fichier de sortie
def ecrire(resultat):
    nomFichier = str(sys.argv[1])

    #Nom du fichier solution
    nomFichier = "Solution_enumeration_"+nomFichier
    file = open(nomFichier, "w")

    #empeche le retour a la ligne
    file.write(str(len(resultat)).rstrip('\n'))
    for res in resultat:
        file.write(f" {str(res)}")
    file.close()
    print(f"Résultats inscrits dans le fichier '{nomFichier}'")

#Verifie que la recette corresponds au client
def clientSatisfait(recette, likes, dislikes):
    #Si un ingredient qu'il deteste est sur la pizza, alors il n'est pas satisfait
    for d in dislikes:
        if d in recette:
            return 0
    #Si un ingrédient qu'il aime n'est pas sur la pizza, alors il n'est pas satisfait
    for l in likes:
        if not l in recette:
            return 0
    return 1



try:
    instance_file = sys.argv[1]
except:
    raise Exception("Erreur à la lecture des arguments. Syntaxe de la commande :\n\
        python3 enumeration.py <chemin_vers_fichier_d_entree> >")

## Lecture du fichier de l'instance
data = []
try:
    with open(instance_file, "r") as f:
        data = f.readlines()
    data = [l.strip().split() for l in data]
except:
    raise Exception("Erreur lors de la lecture de l'instance. Vérifiez que le premier argument est bien un fichier d'instance (comme B_basic.txt)")

Nclients = int(data[0][0]) # Nombre total de clients
data.pop(0)

ingredients = dict() # nom d'un ingrédient (str) -> identifiant (entier allant de 0 à N-1)
noms_ingredients = [] # identifiant (entier allant de 0 à N-1, indice dans la liste) -> nom de l'ingrédient (str) qui a cet identifiant

Ningredients = 0

L = [set() for _ in range(Nclients)] # L[i] est la liste des ingrédients que le client i aime (Like)
D = [set() for _ in range(Nclients)] # D[i] est la liste des ingrédients que le client i n'aime pas (Dislike)


# Boucle sur tous les clients pour générer leurs préférences
for client in range(Nclients):
    Lc,Dc = data[2*client][1:], data[2*client+1][1:] # préférences du client
    for nom_ingr in Lc + Dc:
        if nom_ingr not in ingredients: # nom_ingr n'est pas dans les clés du dictionnaire -> c'est un ingrédient que l'on a pas encore rencontré
            ingredients[nom_ingr] = Ningredients # on lui attribue un numéro unique dans [0;N-1]
            Ningredients += 1 # incrémenter le compteur d'ingrédients
    L[client] = {ingredients[i] for i in Lc}
    D[client] = {ingredients[i] for i in Dc}

# -------------------------------------------------------------- #

#Creation structures
#Contient une recette et un "score" = nombre de client satisfait par la recette
enumeration = []*Nclients
#Contient l'ensemble des recettes possibles
recettes =[]*pow(2,Ningredients)

# Liste des ingrédients
listeIngredients = []
for i in range(0, Ningredients):
    listeIngredients.append(i)

# Génération de toutes les combinaisons possible de recette
for j in range (0, Ningredients):
    temp = combinations(listeIngredients, j)
    #Liste des recettes possibles
    recettes.extend(temp)

# On parcourt toutes les recettes
for r in recettes:
    nbClientSatisfait = 0
    #On parcourt chaque client
    for client in range(Nclients):
        # Vérifie si la recette correspond au client
        nbClientSatisfait = nbClientSatisfait + clientSatisfait(r, L[client], D[client])
    if nbClientSatisfait > 0:
        enumeration.append((nbClientSatisfait, r))


#Récupération de la meilleur recette
temp = enumeration[0][0]
for e in enumeration:
    #Si nbClientSatisfait > maxClient
    if e[0] > temp:
        temp = e[0]

# Récupération d'une recette correspondante
for e in enumeration:
    #On cherche la recette en question, une fois trouvé, on sort de la boucle
    if (e[0] == temp):
        optimale = e[1]
        break

# Traduction en recettes
resultat = []* len(optimale)
for key, value in ingredients.items():
    for ingr in optimale:
        if ingr == value:
            resultat.append(key)

#Creation du fichier solution
ecrire(resultat)

