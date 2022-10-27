import random
from matplotlib import pyplot as plt
import numpy as np


POPULATION_SIZE = 10  # 개체 집단의 크기
MUTATION_RATE = 0.1  # 돌연 변이 확률
SIZE = 8  # 하나의 염색체에서 유전자 개수


# 염색체를 클래스로 정의한다.
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()  # 유전자는 리스트로 구현된다.
        self.fitness = 0  # 적합도
        if self.genes.__len__() == 0:  # 염색체가 초기 상태이면 초기화한다.
            i = 0
            while i < SIZE:
                if random.random() >= 0.5:
                    self.genes.append(np.random.randint(0, SIZE))
                else:
                    self.genes.append(np.random.randint(0, SIZE))
                i += 1

    def cal_fitness(self):  # 적합도를 계산한다.
        self.fitness = 28
        value = 0
        # 행열 충돌 계산
        for i in range(len(self.genes) -1 ):
            for j in range(i +1, len(self.genes)):
                if self.genes[i] == self.genes[j]:
                    value += 1
        for i in range(len(self.genes) - 1):
            for j in range(i + 1, len(self.genes)):
                if abs(self.genes[j] - self.genes[i]) == abs(j - i):
                    value += 1
        # for i in range(SIZE):
        #     value += self.genes[i] * pow(2, SIZE - 1 - i)
        self.fitness -= value
        return self.fitness

    def __str__(self):
        return self.genes.__str__()


# 염색체와 적합도를 출력한다.
def print_p(pop):
    i = 0
    for x in pop:
        print("염색체 #", i, "=", x, "적합도=", x.cal_fitness())
        i += 1
    print("")


# 선택 연산
def select(pop):
    # max_value = sum([c.cal_fitness() for c in pop])
    # pick = random.uniform(0, max_value)
    pick = np.random.randint(0, SIZE)
    return pop[pick]
    # current = 0
    #
    # # 룰렛휠에서 어떤 조각에 속하는지를 알아내는 루프
    # for c in pop:
    #     current += c.cal_fitness()
    #     if current > pick:
    #         return c


# 교차 연산
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index = np.sort(np.random.choice(range(1, SIZE - 1), size=2, replace=False))
    child1 = father.genes[:index] + mother.genes[index:]
    child2 = mother.genes[:index] + father.genes[index:]
    return child1, child2


# 돌연변이 연산
def mutate(c):
    for i in range(SIZE):
        if random.random() < MUTATION_RATE:
            if random.random() < 0.5:
                c.genes[i] = np.random.randint(0, SIZE)
            else:
                c.genes[i] = np.random.randint(0, SIZE)


if __name__ == '__main__':
    # 메인 프로그램
    population = []
    i = 0
    fitness = []
    # 초기 염색체를 생성하여 객체 집단에 추가한다.
    while i < POPULATION_SIZE:
        population.append(Chromosome())
        i += 1

    count = 0
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    print("세대 번호=", count)
    print_p(population)
    count = 1

    while population[0].cal_fitness() < 28:
        new_pop = []

        # 선택과 교차 연산
        for _ in range(POPULATION_SIZE // 2):
            c1, c2 = crossover(population)
            new_pop.append(Chromosome(c1))
            new_pop.append(Chromosome(c2))

        # 자식 세대가 부모 세대를 대체한다.
        # 깊은 복사를 수행한다.
        population = new_pop.copy()

        # 돌연변이 연산
        for c in population: mutate(c)

        # 출력을 위한 정렬
        population.sort(key=lambda x: x.cal_fitness(), reverse=True)
        fitness.append(population[0].cal_fitness())
        print("세대 번호=", count)
        print_p(population)
        count += 1

        # plt.plot(range(len(fitness)), fitness)
        # plt.show()
        if count > 1000: break