import os.path
from os import path
import json
import random as rn
import numpy


class Problem:
    def __init__(self):
        self.file_name = '1.json'
        self.city_number = 300
        self.matrix = [[]]
        self.init_matrix()

    def get_cost(self, paths):
        solution = 0
        for i in range(self.city_number - 1):
            solution += self.get_distance(paths[i], paths[i + 1])
        solution += self.get_distance(paths[self.city_number - 1], paths[0])
        return solution

    def get_distance(self, source, destination):
        return self.matrix[source][destination]

    def find_optimal_sol(self):
        solutions = []
        for i in range(self.city_number):
            nodes = [k for k in range(self.city_number)]
            current_node = i
            paths = []
            paths.append(current_node)
            for j in range(self.city_number - 1):
                node = current_node
                current_node = min([n for n in nodes if n not in paths], key=lambda n: self.get_distance(node, n))
                paths.append(current_node)
            solutions.append(self.get_cost(paths))
        return min(solutions)

    def init_matrix(self):
        if path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.matrix = json.loads('\n'.join(file.readlines()))
                return
        self.gen_matrix()
        with open(self.file_name, 'w') as file:
            file.write(json.dumps(self.matrix))

    def gen_matrix(self):
        self.matrix = [[] for _ in range(self.city_number)]
        for i in range(self.city_number):
            self.matrix[i] = [0 for _ in range(self.city_number)]
            for j in range(self.city_number):
                if j > i:
                    self.matrix[i][j] = rn.randint(5, 150)
                elif j == i:
                    self.matrix[i][j] = numpy.inf
                else:
                    self.matrix[i][j] = self.matrix[j][i]


class Solution:
    def __init__(self, problem: Problem, paths):
        self.paths = paths
        self.problem = problem
        self.cost = problem.get_cost(paths)


class GeneticAlgorithm:
    def __init__(self, batch_number, probability, problem: Problem):
        self.population_size = 1000
        self.breeding_pool_size = 100
        self.mutation_probability = probability
        self.batch_size = problem.city_number / batch_number
        self.problem = problem
        self.current_generation = self.__get_initial_population()

    def __get_initial_population(self):
        population = []
        for i in range(self.population_size):
            population.append(Solution(self.problem, sorted(list(range(self.problem.city_number)), key=lambda x: rn.randint(0, self.problem.city_number))))
        return population

    def __choose_solution(self, probabilities):
        random = rn.random()
        sum = 0.0
        for i in range(len(probabilities)):
            sum += probabilities[i]
            if sum > random:
                return i
        return len(probabilities) - 1

    def __get_probabilities(self, solutions):
        values = [0.0 for _ in range(len(solutions))]
        sum = 0.0
        for i in range(len(solutions)):
            values[i] = 1.0 / solutions[i].cost
            sum += values[i]
        for i in range(len(values)):
            values[i] /= sum
        return values

    def __mutate(self, solution):
        first = rn.randint(0, len(solution.paths) - 1)
        second = rn.randint(0, len(solution.paths) - 1)
        solution.paths[first], solution.paths[second] = solution.paths[second], solution.paths[first]

    def __cross(self, first: Solution, second: Solution):
        first_genes = [0 for _ in range(self.problem.city_number // 2)]
        for i in range(self.problem.city_number // 2):
            first_genes[i] = first.paths[int(self.batch_size * 2 * (i // self.batch_size) + i % self.batch_size)]
        paths = [0 for _ in range(self.problem.city_number)]
        current_second = 0
        for i in range(self.problem.city_number):
            if (i // self.batch_size) % 2 == 0:
                paths[i] = first.paths[i]
            else:
                while second.paths[current_second] in first_genes:
                    current_second += 1
                paths[i] = second.paths[current_second]
                current_second += 1
        return Solution(self.problem, paths)

    def get_best_solution(self):
        return min(self.current_generation, key=lambda c: c.cost)

    def iterate(self):
        breeding_pool = sorted(self.current_generation, key=lambda s: s.cost)[:self.breeding_pool_size]
        best = breeding_pool[:self.breeding_pool_size // 5]
        probabilities = self.__get_probabilities(breeding_pool)
        new_population = [0 for _ in range(self.problem.city_number)]
        for i in range(self.problem.city_number):
            if i < self.breeding_pool_size // 5:
                new_population[i] = best[i]
            else:
                new_population[i] = self.__cross(breeding_pool[self.__choose_solution(probabilities)],
                                                 breeding_pool[self.__choose_solution(probabilities)])
                if rn.random() < self.mutation_probability:
                    self.__mutate(new_population[i])
        self.current_generation = new_population