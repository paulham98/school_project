import random
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
from itertools import permutations
POPULATION_SIZE = 3# 개체 집단의 크기
MUTATION_RATE = 0.1	# 돌연 변이 확률

# 염색체를 클래스로 정의한다. 
data_df = pd.read_excel('./국내 주요 도시간 거리.xlsx',engine='openpyxl',header=1)
data_df.set_index('도시명',drop=True,inplace=True)
data_df = data_df.astype('int') 

CITY_LIST = data_df.columns[2:].tolist()
SIZE = len(CITY_LIST)			# 하나의 염색체에서 유전자 개수		
#### 서울 - 도시 - 서울 을 위한 완전탐색 
def min_distance():
    result = float('inf')
    result_city_list= None
    for i in permutations(CITY_LIST):
        new_result = 0
        current_city = '서울'
        for al in i:
            new_result+=data_df[current_city][al]
            current_city = al
        new_result += data_df[current_city]['서울']
        if new_result < result :
            result = new_result
            result_city_list = ['서울'] + list(i) + ['서울']

    return result ,result_city_list

MIN_DISTANCE,MIN_CITY_DISTANCE = min_distance()

print("MIN DISTANCE : " ,MIN_DISTANCE)
print("MIN DISTANCE CITY: " ,MIN_CITY_DISTANCE)

class Chromosome:
    def __init__(self, g=[]):
        self.genes:list = g.copy()		# 유전자는 리스트로 구현된다. 
        self.fitness = 0		# 적합도
        if self.genes.__len__()==0:
            self.genes = CITY_LIST.copy()# 염색체가 초기 상태이면 초기화한다. 
            random.shuffle(self.genes)
        self.cal_fitness()
    def cal_fitness(self):		# 적합도를 계산한다. 
        self.fitness = 0;
        current_city = '서울'
        for i in range(SIZE):
            self.fitness += data_df[current_city][self.genes[i]]
            current_city = self.genes[i]
        self.fitness += data_df[current_city]['서울']
        
        return self.fitness

    def __str__(self):
        return self.genes.__str__()


# 염색체와 적합도를 출력한다. 
def print_p(pop):
    i = 0
    for x in pop:
        print("염색체 #", i, "=", x, "적합도=", x.fitness)
        i += 1
    print("")

# 선택 연산
def select(pop):
    max_value  = sum([c.fitness for c in population])
    pick    = random.uniform(0, max_value)
    current = 0
    # 룰렛휠에서 어떤 조각에 속하는지를 알아내는 루프
    for c in pop:
        current += c.fitness
        if current > pick:
            return c

# 교차 연산
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index1 = random.randint(0, SIZE-1)
    index2 = index1
    while index2!=index1 and abs(index1-index2)!=1:
        index2 = random.randint(0,SIZE-1)
    if index2<index1:
        index1,index2=  index2,index1
    #every index1 < index2 
    father_swap = father.genes[index1:index2]
    mother_swap = mother.genes[index1:index2]
    father_temp = [x for x in father.genes if x not in mother_swap]
    mother_temp = [y for y in mother.genes if y not in father_swap]

    child1 = father_temp[:index1] + mother_swap + father_temp[index1:]
    child2 = mother_temp[:index1] + father_swap + mother_temp[index1:]
    return (child1, child2)


# 돌연변이 연산
def mutate(c):
    check=False
    for i in range(1,SIZE):
        if random.random() < MUTATION_RATE:
            check=True
            swap_number = random.randint(0,SIZE-1)
            c.genes[i],c.genes[swap_number]=c.genes[swap_number],c.genes[i]

    if check:
        c.cal_fitness()

# 메인 프로그램
population = []
i=0
# 초기 염색체를 생성하여 객체 집단에 추가한다. 
while i<POPULATION_SIZE:
    population.append(Chromosome())
    i += 1

count=0
# population.sort(key=lambda x: x.cal_fitness(), reverse=True)
print("세대 번호=", count)
print_p(population)
count=1
population_fitness = []
while population[0].cal_fitness() > MIN_DISTANCE:
    # new_pop = []
    # 선택과 교차 연산
    for _ in range(POPULATION_SIZE//2):
        c1, c2 = crossover(population);
        population.append(Chromosome(c1));
        population.append(Chromosome(c2));
    
    # 자식 세대가 부모 세대를 대체한다. 
    # 깊은 복사를 수행한다. 
    population.sort(key=lambda x: x.fitness)
    population = population[:POPULATION_SIZE]
    
    # 돌연변이 연산
    for c in population: mutate(c)
    # 출력을 위한 정렬
    population.sort(key=lambda x: x.fitness)
    print("세대 번호=", count , "=======================")
    print_p(population)
    count += 1
    population_fitness.append(sum([x.fitness for x in population])/POPULATION_SIZE)
    if population[0].fitness == MIN_DISTANCE:
        print('FOUND :',population[0].genes ,  "  적합도=", population[0].fitness)
        break;
    if count > 1000 : break;


plt.scatter(x=[c for c in range(1,count)],y=population_fitness,color='b')
plt.savefig('TSP.png')
plt.show()
plt.close()
# print(data_df)
# a = Chromosome([1,6,8,3,7,4,2,5])
# print(a.cal_fitness())
