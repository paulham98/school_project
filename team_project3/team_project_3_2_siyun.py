import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

distance = pd.read_excel('./국내 주요 도시간 거리.xlsx', header=1, index_col=0)

distance = distance.astype(int)

POPULATION_SIZE = 10
MUTATION_RATE = 0.1
SIZE = 10

class Chromosome:
    def __init__(self, g=np.zeros((SIZE,), dtype=int)):
        self.genes = g.copy()
        self.fitness = 0

        if np.array_equal(self.genes, np.zeros((SIZE,), dtype=int)):
            self.genes = np.concatenate((np.zeros((1,), dtype=int), np.random.choice(range(1, SIZE - 1), size=SIZE - 2, replace=False), np.zeros((1,), dtype=int)))

    
    def cal_fitness(self):
        self.fitness = 0

        value = 0
        for i in range(SIZE - 1):
            if i == 8:
                value += distance.iloc[self.genes[i], 0]
            else:
                value += distance.iloc[self.genes[i], self.genes[i + 1]]
        self.fitness = value
        return self.fitness

    def __str__(self):
        return self.genes.__str__()

def print_p(pop):
    i = 0
    for x in pop:
        print("염색체 #", i, "=", x, "적합도=", x.cal_fitness())
        i += 1
    print("")

def select(pop):
    max_value  = sum([c.cal_fitness() for c in pop])
    pick = np.random.uniform(0, max_value)
    current = 0
    
    for c in pop:
        current += c.cal_fitness()
        if current > pick:
            return c

def crossover(pop):
    father = select(pop)
    mother = select(pop)

    while np.array_equal(father.genes, mother.genes):
        father = select(pop)
        mother = select(pop)

    index = np.sort(np.random.choice(range(1, SIZE - 1), size=2, replace=False))

    child1 = np.concatenate((np.zeros((1,), dtype=int), np.full((SIZE - 2,), -1, dtype=int), np.zeros((1,), dtype=int)))
    child2 = np.concatenate((np.zeros((1,), dtype=int), np.full((SIZE - 2,), -1, dtype=int), np.zeros((1,), dtype=int)))

    child1[index[0]:index[1]] = father.genes[index[0]:index[1]]
    child2[index[0]:index[1]] = mother.genes[index[0]:index[1]]

    for i, g in enumerate(mother.genes):
        if g not in child1 and np.where(child1 == -1)[0].size != 0:
            child1[np.where(child1 == -1)[0][0]] = g

    for i, g in enumerate(father.genes):
        if g not in child2 and np.where(child2 == -1)[0].size != 0:
            child2[np.where(child2 == -1)[0][0]] = g

    return (child1, child2)
    
def mutate(c):
    for i in range(SIZE):
        if np.random.random() < MUTATION_RATE:
            c.genes = np.concatenate((np.zeros((1,), dtype=int), np.random.choice(range(1, SIZE - 1), size=SIZE - 2, replace=False), np.zeros((1,), dtype=int)))

if __name__ == '__main__':
    population = []
    fitness = []
    i=0

    while i < POPULATION_SIZE:
        population.append(Chromosome())
        i += 1

    count=0
    population.sort(key=lambda x: x.cal_fitness())
    fitness.append(population[0].cal_fitness())
    print("세대 번호=", count)
    print_p(population)
    count=1

    while population[0].cal_fitness() > 988:
        new_pop = []

        for _ in range(POPULATION_SIZE//2):
            population.sort(key=lambda x: x.cal_fitness())
            c1, c2 = crossover(population)
            new_pop.append(Chromosome(c1))
            new_pop.append(Chromosome(c2))

        population = new_pop.copy();    
        
        for c in population: mutate(c)

        population.sort(key=lambda x: x.cal_fitness())
        fitness.append(population[0].cal_fitness())
        print("세대 번호=", count)
        print_p(population)
        count += 1

        plt.plot(range(len(fitness)), fitness)
        plt.show()

        if count > 1000: break