from pydoc import cli
import sys
from random import randint, random

#Ecrie dans le fichier de sortie
def ecrire(resultat):
    nomFichier = str(sys.argv[1])

    #Nom du fichier solution
    nomFichier = "Solution_Genetique_"+nomFichier
    file = open(nomFichier, "w")

    #empeche le retour a la ligne
    file.write(str(len(resultat)).rstrip('\n'))
    for res in resultat:
        file.write(f" {str(res)}")
    file.close()
    print(f"Résultats inscrits dans le fichier '{nomFichier}'")

try:
    instance_file = sys.argv[1]
except:
    raise Exception("Erreur à la lecture des arguments. Syntaxe de la commande :\n\
        python3 evaluation.py <chemin_vers_fichier_d_entree> <chemin_vers_fichier_de_solution>")

# ----------------------------------------------------------------------------------------- #
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

# ----------------------------------------------------------------------------------------- #
#Algo Genetique
Res_Attendu = Nclients
Nb_Ingredient = Ningredients

#Nombre de recette de base
NbRecette = 20
#Nombre maximum d'itération (génération)
Nb_Generation_Max = 100
#Critère d'arret: Si aucune evolution sur un pourcentage de la generation, on arrete.
Arret_Evolution = int (Nb_Generation_Max * 0.1)
# Operateur de mutation (Plusieurs essai pour trouver une "bonne valeur"
Mutation = 0.7
# Operateur de selection (% des meilleures recettes)
Recette_Selectionnee = 0.3
#Survie des recettes les moins bonnes
Chance_Survie = 0.5

Nb_recette_selectionnee = int(NbRecette * Recette_Selectionnee)
# Génère un ingrédient aléatoire
def ingredientAleatoire():
    res = randint(0,Nb_Ingredient-1)
    return res

#Génère une recette
def generer_Recette():
    recette = list()
    for _ in range(0, randint(1,Nb_Ingredient-1)):
        temp = ingredientAleatoire()
        if temp not in recette:
            recette.append(temp)
    return recette

# Créer une population aléatoire de la taille de NbRecette
def genererNouvellesRecettes():
    return [generer_Recette() for _ in range(NbRecette)]


#Croisement dedeux recettes
def croisement (recetteA, recetteB):
    #Nouvelle recette vide au départ
    new_recette = []
    #On parcourt la premiere recette
    for rec in range(0, int(len(recetteA))):
        #Une chance sur deux de garder cet ingrédient
        if random() < 0.5:
            new_recette.append(rec)
    for rec in range(0, int(len(recetteB))):
        #Une chance sur deux de garder cet ingrédient
        if random() < 0.5:
            if rec not in new_recette:
                new_recette.append(rec)
    return new_recette

#Opere une mutation: ajoute ET/OU supprime un ingrédient de la recette
def mutation (recette):
    if random() < 0.5:
        new_ingredient = ingredientAleatoire()
        if (len(recette) < Nb_Ingredient):
            while new_ingredient in recette:
                new_ingredient = ingredientAleatoire()
            recette.append(new_ingredient)
    if random() < 0.5:
        new_ingredient = ingredientAleatoire()
        if (len(recette) < Nb_Ingredient):
            while new_ingredient not in recette:
                new_ingredient = ingredientAleatoire()
            recette.remove(new_ingredient)
    return recette


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

# Détermine le score d'un recette = nombre de client satisfait
def nbClientSatisfait (recette, likes, dislikes, nbClientsTotal):
    nbClient = 0
    for client in range(nbClientsTotal):
        nbClient += clientSatisfait(recette, likes[client], dislikes[client])
    return nbClient

# Ordonne toutes les recettes de la population selon l'attrait qu'elles génèrent
def classement_meilleure_recette(population, nbClientsTotal, Likes, Dislikes):
    nbClientSatisfaitPopulation = 0
    tabScore = list()
    for recette in population:
        nbClient = nbClientSatisfait(recette, Likes, Dislikes, nbClientsTotal)
        nbClientSatisfaitPopulation += nbClient
        tabScore.append((recette, nbClient))
    return sorted(tabScore, key=lambda x: x[1], reverse=True)

# Réalise toutes les étapes nécessaires à la création de la nouvelle génération
def nouvelle_generation(population, nbClientsTotal, Likes, Dislikes):
    #Ordonne la population
    population_triee = classement_meilleure_recette(population, Nclients, L, D)

    #Condition d'arret: si tout les clients sont satisfaits avec la recette, stop
    solution = []
    for recette in population_triee:
        if recette[1] == Res_Attendu:
            solution.append(recette[0])
            return population_triee, solution

    # Sinon, on crée une nouvelle génération de recette

    #On récupère les (Nb_recette_selectionnee) meilleures recettes
    recettes_parents = []
    for recette in population_triee[:Nb_recette_selectionnee]:
        recettes_parents.append(recette[0])

    #On récupère les moins bonnes recettes ayant survécues:
    for recette in population_triee[Nb_recette_selectionnee:]:
        if random() < Chance_Survie:
            recettes_parents.append(recette[0])

    #On remplie le reste des recettes par croisement
    while len(recettes_parents) < NbRecette:
        recA = randint(0, len(recettes_parents)-1)
        recB = randint(0, len(recettes_parents)-1)
        if recA != recB:
            recettes_parents.append(croisement(recettes_parents[recA], recettes_parents[recB]))

    #On fait muter les recettes
    for recette in recettes_parents:
        if random() < Mutation:
            recette = mutation(recette)


    #On renvoie la nouvelle gen'
    return recettes_parents, solution

print("Lancement du programme...")
solution = None
nbGen = 0
nbSansEvolution = 0
dernierScoreMax = 0
population = genererNouvellesRecettes()
print("Génération de initiale terminée. Début des évolutions:")

while not solution and nbGen < Nb_Generation_Max and nbSansEvolution <= Arret_Evolution:
    if nbGen > 0:
        dernierScoreMax = scoreMax
    population, solution = nouvelle_generation(population, Nclients, L, D)
    scoreMax = nbClientSatisfait(population[0], L, D, Nclients)
    print(f"Génération n°{nbGen}: score max: {scoreMax} - Nb génération sans évolution: {nbSansEvolution}")
    nbGen += 1
    # Contrôle l'arrêt si l'évolution du score max est bloqué
    if scoreMax == dernierScoreMax:
        nbSansEvolution += 1
    else:
        nbSansEvolution = 0

res = nbClientSatisfait(population[0], L, D, Nclients)

# Traduction des indices en ingrédients
resultat = []
for key, value in ingredients.items():
    for ingredient in range(res):
        if ingredient == value:
            resultat.append(key)

print("ARRÊT !")
print(f"Génération finale (n°:{nbGen}) - score max de cet gen: {res}")


ecrire(resultat)