import random
import pandas as pd
import numpy as np

distance = pd.read_excel('./국내 주요 도시간 거리.xlsx', header=1, index_col=0)
distance = distance.astype(int)
print(distance)
print(distance.iloc[8][0])

POPULATION_SIZE = 10  # 개체 집단의 크기
MUTATION_RATE = 0.1  # 돌연 변이 확률
SIZE = 10  # 하나의 염색체에서 유전자 개수


# 염색체를 클래스로 정의한다.
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()  # 유전자는 리스트로 구현된다.
        self.fitness = 0  # 적합도
        if self.genes.__len__() == 0:  # 염색체가 초기 상태이면 초기화한다.
            self.genes.append(0)
            tmp_arr = np.random.choice(range(1, SIZE-1), size=SIZE - 2, replace=False)
            for a in tmp_arr:
                self.genes.append(a)
            self.genes.append(0)

    def cal_fitness(self):  # 적합도를 계산한다.
        self.fitness = 0
        value = 0
        for i in range(SIZE-1):
            # print(len(self.genes))
            value += distance.iloc[self.genes[i], self.genes[i+1]]
            # print(distance.iloc[i, self.genes[i]])
        self.fitness = value
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
    max_value = sum([c.cal_fitness() for c in pop])
    pick = random.uniform(0, max_value)
    current = 0

    # 룰렛휠에서 어떤 조각에 속하는지를 알아내는 루프
    for c in pop:
        current += c.cal_fitness()
        if current > pick:
            return c


# 교차 연산
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    # print(father.genes, mother.genes)
    index = np.sort(np.random.choice(range(1, SIZE - 1), size=2, replace=False))

    latter_length = len(father.genes) - index[1] - 2
    father_mid = father.genes[index[0]:index[1]]
    mother_mid = mother.genes[index[0]:index[1]]

    father_reordered = father.genes[1:index[1]:] + father.genes[index[1]:9]
    mother_reordered = mother.genes[1:index[1]:] + mother.genes[index[1]:9]
    father_reord_filtered = list(filter(lambda x: x not in mother_mid, father_reordered))
    mother_reord_filtered = list(filter(lambda x: x not in father_mid, mother_reordered))
    child1 = [0] + mother_reord_filtered[-index[0]:] + father_mid + mother_reord_filtered[:latter_length] + [0]
    child2 = [0] + father_reord_filtered[-index[0]:] + mother_mid + father_reord_filtered[:latter_length] + [0]
    # print(father.genes, mother.genes)
    # print(child1, child2)
    return child1, child2


# 돌연변이 연산
def mutate(c):
    if random.random() < MUTATION_RATE:
        # print(1)
        swap_id = np.random.choice(range(1, SIZE-1), size=SIZE - 2, replace=False)
        tmp_value1 = c.genes[swap_id[0]]
        tmp_value2 = c.genes[swap_id[1]]
        c.genes[swap_id[0]] = tmp_value2
        c.genes[swap_id[1]] = tmp_value1


if __name__ == '__main__':
    # 메인 프로그램
    population = []
    i = 0

    # 초기 염색체를 생성하여 객체 집단에 추가한다.
    while i < POPULATION_SIZE:
        population.append(Chromosome())
        i += 1

    count = 0
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    print("세대 번호=", count)
    print_p(population)
    count = 1

    while population[0].cal_fitness() > 1018:
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
        population.sort(key=lambda x: x.cal_fitness())
        print("세대 번호=", count)
        print_p(population)
        count += 1
        if count > 1000: break