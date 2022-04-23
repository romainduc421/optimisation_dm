#!/usr/bin/env python
from __future__ import annotations

from dataclasses import dataclass, field

import pygad

@dataclass
class Customer:
    likes: set[str]
    dislikes: set[str]

@dataclass
class Challenge:
    customers: list[Customer] = field(default_factory=list)
    all_ingredients: set = field(default_factory=set)
    solution: set = field(default_factory=set)
    score: int = 0

    def reset(self):
        self.customers = []
        self.all_ingredients = set()
        self.solution = set()
        self.score = 0

    def add_customer(self, customer):
        self.customers.append(customer)
        self.all_ingredients |= customer.likes

    def evaluate(self, pizza: set[str]) -> int:
        result = 0
        for c in self.customers:
            if (c.likes & pizza == c.likes and 
                c.dislikes & pizza == set()):
                result += 1
        return result

    def solve(self, generations=100):
        ingr_list = sorted(list(self.all_ingredients))

        def fitness_func(solution, solution_idx):
            pizza = set([ingr_list[k] for (k,v) in enumerate(solution) if v == 1])
            return self.evaluate(pizza)

        ga_instance = pygad.GA(
            num_generations=generations,
            num_parents_mating=2,
            sol_per_pop=3,
            num_genes=len(ingr_list),
            fitness_func=fitness_func,
            init_range_low=0,
            init_range_high=2,
            random_mutation_min_val=0,
            random_mutation_max_val=2,
            mutation_by_replacement=True,
            gene_type=int)

        ga_instance.run()

        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        self.solution = set([ingr_list[k] for (k,v) in enumerate(solution) if v == 1])
        self.score = solution_fitness

    def process(self, filename, generations=100):
        self.reset()
        with open(f"optimisation_dm/src/soluce/{filename}.txt") as f:
            n = int(f.readline())
            for i in range(n):
                customer = Customer(
                    set(f.readline().strip().split()[1:]),
                    set(f.readline().strip().split()[1:])
                )
                self.add_customer(customer)

            print(len(self.all_ingredients))
            self.solve(generations)

        with open(f"out/{filename}.out-{self.score}.txt", "w") as f:
            f.write(f"{len(self.solution)} ")
            f.write(" ".join(self.solution))

c = Challenge()
c.process("a_exemple", 1000)
c.process("b_basique", 1000)
c.process("c_grossier", 1000)
c.process("d_difficile", 1000)
c.process("e_elabore", 1000)


