#!/usr/bin/env python3

import math
import random
from typing import List, Callable
from dataclasses import dataclass, field
import copy
import sys

@dataclass
class Customer:
    id: int
    likes: List[str] = field(default_factory=list)
    dislikes: List[str] = field(default_factory=list)


def parse_dataset(dataset_path: str) -> List[Customer]:
    """Parses a dataset into a list of handy Customer objects.
    Args:
        dataset_path: relative path to the dataset file.
    Returns:
        List of Customer objects.
    """
    with open(dataset_path, "r") as f:
        customers: List[Customer] = list()
        # skips the first line since we don't really need to know how many customers there are
        lines = f.readlines()[1::]
        # the even indexed lines are ingredients that a customer likes and the odd ones contain those he dislikes
        for cid, (likes_line, dislikes_line) in enumerate(zip(lines[::2], lines[1::2])):
            # skips the number of products number and removes unnecessary whitespace
            likes = [like.strip() for like in likes_line.split(sep=" ")[1:]]
            dislikes = [dislike.strip() for dislike in dislikes_line.split(sep=" ")[1:]]
            customers.append(Customer(cid, likes, dislikes))
        return customers

def naive_cost_function(pizza_ingredients: List[str], customers: List[Customer]) -> int:
    """
    Args:
        pizza_ingredients: list of ingredients on a the pizza.
        customers: list of Customers that were surveyed.
    Returns:
        The number of customers that would order the pizza.
    """
    score = 0
    for customer in customers:
        if all([liked_ingredient in pizza_ingredients for liked_ingredient in customer.likes]) and \
                not any([disliked_ingredient in pizza_ingredients for disliked_ingredient in customer.dislikes]):
            score += 1
    return score


class Solution:
    def __init__(self, customers: List[Customer], pizza_ingredients: List[str] = None):
        self.customers = customers
        if pizza_ingredients is None:
            self._initial_solution()
        else:
            self.pizza_ingredients = pizza_ingredients

    def _initial_solution(self):
        """Makes a pizza with all the ingredients customers like."""
        self.pizza_ingredients = []
        for customer in self.customers:
            self.pizza_ingredients += customer.likes
        # remove duplicate ingredients
        self.pizza_ingredients = list(set(self.pizza_ingredients))

    @property
    def score(self) -> int:
        return naive_cost_function(self.pizza_ingredients, self.customers)

    def submission_format(self) -> str:
        """Returns the solution as the number of ingredients followed by the names of the ingredients."""
        ingredients = " ".join([str(ingredient) for ingredient in self.pizza_ingredients])
        return f'{len(self.pizza_ingredients)} ' + ingredients

    def create_new_solution(self) -> 'Solution':
        """Creates a new solution by changing the current one with a neighbourhood operator."""
        operators = [add_liked_ingredient, remove_disliked_ingredient]
        operator: neighbourhood_operator = random.choice(operators)
        new_pizza_ingredients = operator(self.pizza_ingredients, self.customers)
        return Solution(self.customers, new_pizza_ingredients)


# neighbourhood operators

neighbourhood_operator = Callable[[List[str], List[Customer]], List[str]]


def remove_disliked_ingredient(pizza_ingredients: List[str], customers: List[Customer]) -> List[str]:
    """Removes an ingredient a random customer dislikes from the pizza."""
    pizza_ingredients = copy.copy(pizza_ingredients)
    customers_that_dislike_stuff = [customer for customer in customers if customer.dislikes]
    if not customers_that_dislike_stuff:
        return pizza_ingredients
    random_customer = random.choice(customers_that_dislike_stuff)
    for disliked_ingredient in random_customer.dislikes:
        if disliked_ingredient in pizza_ingredients:
            pizza_ingredients.remove(disliked_ingredient)
            break
    return pizza_ingredients


def add_liked_ingredient(pizza_ingredients: List[str], customers: List[Customer]) -> List[str]:
    """Adds an ingredient a random customer likes to the pizza."""
    pizza_ingredients = copy.copy(pizza_ingredients)
    customers_that_like_stuff = [customer for customer in customers if customer.likes]
    if not customers_that_like_stuff:
        return pizza_ingredients
    random_customer = random.choice(customers_that_like_stuff)
    for liked_ingredient in random_customer.likes:
        if liked_ingredient not in pizza_ingredients:
            pizza_ingredients.append(liked_ingredient)
            break
    return pizza_ingredients



cooling_schedule = Callable[[float, float, int], float]


def exponential_cooling_schedule(t_start: float, alpha: float, iteration: int) -> float:
    """Returns the new temperature of the system changed according to the exponential cooling schedule."""
    return t_start * alpha ** iteration


def recuit_simule(customers: List[Customer], t_start: float, t_stop: float, t_iter: int, alpha: float,
                        change_temperature: cooling_schedule) -> Solution:
    """Recuit simule
    Args:
        customers: list of surveyed customers.
        t_start: starting temperature of the system.
        t_stop: temperature after which the algorithm will halt.
        t_iter: number of iterations in a given temperature.
        alpha: the rate of temperature change coefficient.
        change_temperature: the cooling schedule used in the algorithm.
    Returns:
        Best found solution for the problem.
    """
    current_solution = Solution(customers)
    best_solution = current_solution
    t_current = t_start
    iterations = 0

    while t_current > t_stop:
        for k in range(t_iter):
            new_solution = current_solution.create_new_solution()
            if new_solution.score >= current_solution.score:
                current_solution = new_solution
                if current_solution.score >= best_solution.score:
                    best_solution = current_solution
            else:
                delta = new_solution.score - current_solution.score
                sigma = random.random()
                if sigma < math.exp(delta / t_current):
                    current_solution = new_solution
            iterations += 1

        t_current = change_temperature(t_start, alpha, iterations)
        print(t_current)

    return best_solution


if __name__ == '__main__':
    try:
        instance_file = sys.argv[1]
    except:
        raise Exception("Erreur à la lecture des arguments. Syntaxe de la commande :\n\
        python3 recuit_simule.py <chemin_vers_fichier_d_entree> ")

    customers = parse_dataset(instance_file)
    solution = recuit_simule(customers, t_start=100, t_stop=1, t_iter=20, alpha=0.99,
                                   change_temperature=exponential_cooling_schedule)
    print(solution.score)
    nameFile = "Solution_recuitSim_"+instance_file
    with open(nameFile, "w") as txtfile1:
    	print(solution.submission_format(), file=txtfile1)
    	
    	
