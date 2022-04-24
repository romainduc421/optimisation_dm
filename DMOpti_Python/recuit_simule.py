#!/usr/bin/env python3

import math
import random
from typing import List, Callable
from dataclasses import dataclass, field
import copy
import sys

@dataclass
class Client:
    id: int
    likes: List[str] = field(default_factory=list)
    dislikes: List[str] = field(default_factory=list)



def input_data_parsing(dataset_path: str) -> List[Client]:
    '''parse un jeu de données en liste d'objects client facilement utilisable.
    Args:
        dataset_path: relative path to the dataset file.
    Returns:
        List of Client objects.
    '''
    with open(dataset_path, "r") as f:
        Clients: List[Client] = list()
        # skips the first line since we don't really need to know how many Clients there are
        lines = f.readlines()[1::]
        # the even indexed lines are ingredients that a Client likes and the odd ones contain those he dislikes
        for cid, (likes_line, dislikes_line) in enumerate(zip(lines[::2], lines[1::2])):
            # skips the number of products number and removes unnecessary whitespace
            likes = [like.strip() for like in likes_line.split(sep=" ")[1:]]
            dislikes = [dislike.strip() for dislike in dislikes_line.split(sep=" ")[1:]]
            Clients.append(Client(cid, likes, dislikes))
        return Clients


def score_solution(pizza_ingredients: List[str], clients: List[Client]) -> int:
        '''
        Args:
            pizza_ingredients: liste des ing sur la pizza
            clients: liste de clients qui ont subi l'enquête
        Returns:
            le nb de clients qui voudront bien commander la pizza
        '''
        score = 0
        for client in clients:
            if all([liked_ingredient in pizza_ingredients for liked_ingredient in client.likes]) and \
                    not any([disliked_ingredient in pizza_ingredients for disliked_ingredient in client.dislikes]):
                score += 1
        return score

class Solution:
    def __init__(self, Clients: List[Client], pizza_ingredients: List[str] = None):
        self.Clients = Clients
        if pizza_ingredients is None:
            self._initial_solution()
        else:
            self.pizza_ingredients = pizza_ingredients

    def _initial_solution(self):
        '''Makes a pizza with all the ingredients Clients like.'''
        self.pizza_ingredients = []
        for Client in self.Clients:
            self.pizza_ingredients += Client.likes
        # enleve les ingredients en doublons
        self.pizza_ingredients = list(set(self.pizza_ingredients))

    @property
    def score(self) -> int:
        return score_solution(self.pizza_ingredients, self.Clients)

    def submission_format(self) -> str:
        '''Returns the solution as the number of ingredients followed by the names of the ingredients.'''
        ingredients = " ".join([str(ingredient) for ingredient in self.pizza_ingredients])
        return f'{len(self.pizza_ingredients)} ' + ingredients

    def create_new_solution(self) -> 'Solution':
        '''Creates a new solution by changing the current one with a neighbourhood operator.'''
        operators = [add_liked_ingredient, remove_disliked_ingredient]
        operator: operateur_voisinage = random.choice(operators)
        new_pizza_ingredients = operator(self.pizza_ingredients, self.Clients)
        return Solution(self.Clients, new_pizza_ingredients)


# neighbourhood operators

operateur_voisinage = Callable[[List[str], List[Client]], List[str]]
#list object is not callable in py

def remove_disliked_ingredient(pizza_ingredients: List[str], Clients: List[Client]) -> List[str]:
    '''enlève un ingrédient de la pizza qu'un client aléatoire n'apprecie pas du tout'''
    pizza_ingredients = copy.copy(pizza_ingredients)
    Clients_that_dislike_stuff = [Client for Client in Clients if Client.dislikes]
    if not Clients_that_dislike_stuff:
        return pizza_ingredients
    random_Client = random.choice(Clients_that_dislike_stuff)
    for disliked_ingredient in random_Client.dislikes:
        if disliked_ingredient in pizza_ingredients:
            pizza_ingredients.remove(disliked_ingredient)
            break
    return pizza_ingredients


def add_liked_ingredient(pizza_ingredients: List[str], Clients: List[Client]) -> List[str]:
    '''ajoute un ingrédient qu'un client aléatoire aime sur la pizza'''
    pizza_ingredients = copy.copy(pizza_ingredients)
    Clients_that_like_stuff = [Client for Client in Clients if Client.likes]
    if not Clients_that_like_stuff:
        return pizza_ingredients
    random_Client = random.choice(Clients_that_like_stuff)
    for liked_ingredient in random_Client.likes:
        if liked_ingredient not in pizza_ingredients:
            pizza_ingredients.append(liked_ingredient)
            break
    return pizza_ingredients



prgm_refroidissement = Callable[[float, float, int], float]


def exponentiel_prgm_refroidissement(t_start: float, alpha: float, iteration: int) -> float:
    ''' retourne la nouvelle temperature du systeme coinjointement au programme de refroidissement exponentiel'''
    return t_start*math.pow(alpha, iteration)


def recuit_simule(Clients: List[Client], t_start: float, t_stop: float, t_iter: int, alpha: float,
                        change_temperature: prgm_refroidissement) -> Solution:
    '''simulated annealing algorithm (stochastic)
    Args:
        Clients: liste des clients étudiés
        t_start: temperature de depart du système
        t_stop: temperature après laquelle l'algo d'optimisation va s'arrêter
        t_iter: nombre d'iterations a une temperature donnee
        alpha: coefficient (taux) de variation de température
        change_temperature: échéancier de refroidissement utilisé dans l'algo
    Returns:
        solution au problème (pas forcément optimale)
    '''
    #evaluate the initial point
    current_solution = Solution(Clients)
    #current working solution
    best_solution = current_solution
    t_current = t_start
    iterations = 0

    while t_current > t_stop:
        #t iterations (t steps)
        for k in range(t_iter):
            new_solution = current_solution.create_new_solution()
            if new_solution.score >= current_solution.score:
                current_solution = new_solution
                if current_solution.score >= best_solution.score:
                    best_solution = current_solution
            else:
                diff = new_solution.score - current_solution.score
                metropolis= math.exp(diff)*math.exp(1/t_current)

                #check if we would keep the new point
                if random.random() < metropolis:
                    #store the new current point
                    current_solution = new_solution
            iterations += 1

        t_current = change_temperature(t_start, alpha, iterations)
        print(t_current)

    return best_solution

def main():
    try:
        instance_file = sys.argv[1]
    except:
        raise Exception("Erreur à la lecture des arguments. Syntaxe de la commande :\n\
        python3 recuit_simule.py <chemin_vers_fichier_d_entree> ")

    Clients = input_data_parsing(instance_file)
    solution = recuit_simule(Clients, t_start=100, t_stop=1, t_iter=20, alpha=0.99,
                                   change_temperature=exponentiel_prgm_refroidissement)
    nameFile = "Solution_recuitSim_"+instance_file
    with open(nameFile, "w") as txtfile1:
    	print(solution.submission_format(), file=txtfile1)

if __name__ == '__main__':
    main()
    
    	
    	
