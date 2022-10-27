import numpy as np
from matplotlib import pyplot as plt

POPULATION_SIZE = 10
MUTATION_RATE = 0.05
SIZE = 8

class Chromosome:
    # chromosome class initial setting
    def __init__(self, g=np.zeros((8, 2), dtype=int)):
        self.genes = g.copy()
        self.fitness = 0

        # gene initial setting
        positions = [(i, j) for i in range(8) for j in range(8)]
        for p in self.genes:
            i = np.random.randint(0, high=len(positions))
            q_position = positions[i]
            positions.pop(i)
            p[0], p[1] = q_position
    
    # calculate fitness
    def cal_fitness(self):
        self.fitness = 28
        value = 0

        for i, p in enumerate(self.genes):
            diagonal_p = []

            for x in range(0, SIZE):
                for y in range(0, SIZE):
                    if x + y == p[0] + p[1] or x - y == p[0] - p[1]:
                        diagonal_p.append((x, y))

            for j in range(i + 1, SIZE):
                if self.genes[j][0] == p[0] or self.genes[j][1] == p[1] or tuple(self.genes[j]) in diagonal_p:
                    value += 1

        self.fitness -= value
        return self.fitness

    def __str__(self):
        return self.genes.__str__()

# print
def print_p(pop):
    i = 0
    for x in pop:
        print("염색체 #", i, "=", ' '.join(map(str, x.genes)), "적합도=", x.cal_fitness())
        i += 1
    print("")

def select(pop):
    pick = np.random.randint(2, SIZE)
    return pop[pick]

def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index = np.random.randint(1, SIZE - 2)
    child1 = np.concatenate((father.genes[:index], mother.genes[index:]))
    child2 = np.concatenate((mother.genes[:index], father.genes[index:]))

    return (child1, child2)
    
# mutation
def mutate(c):
    for i in range(SIZE):
        if np.random.random() < MUTATION_RATE:
            c.genes[i] = (np.random.randint(0, SIZE), np.random.randint(0, SIZE))

if __name__ == '__main__':
    population = []
    fitness = []
    i=0

    while i < POPULATION_SIZE:
        population.append(Chromosome())
        i += 1

    count=0
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    fitness.append(population[0].cal_fitness())
    print("세대 번호=", count)
    print_p(population)
    count=1

    while population[0].cal_fitness() < 28:
        new_pop = []

        # crossover
        for _ in range(POPULATION_SIZE//2):
            c1, c2 = crossover(population)
            new_pop.append(Chromosome(c1))
            new_pop.append(Chromosome(c2))

        population = new_pop.copy();    
        
        # mutation
        for c in population: mutate(c)

        population.sort(key=lambda x: x.cal_fitness(), reverse=True)
        fitness.append(population[0].cal_fitness())
        print("세대 번호=", count)
        print_p(population)
        count += 1

        plt.plot(range(len(fitness)), fitness)
        # plt.show()
        if count > 1000 : break

    plt.show()