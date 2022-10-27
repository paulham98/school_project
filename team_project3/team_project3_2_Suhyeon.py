import random
import pandas as pd

POPULATION_SIZE = 15
MUTATION_RATE = 0.1
SIZE = 8

data = pd.read_excel("./국내 주요 도시간 거리.xlsx", header=1, index_col=0)
data = data.astype(int)

# 염색체를 클래스로 정의한다. 
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()		# 유전자는 리스트로 구현된다. 
        self.fitness = 0		# 적합도
        
        if self.genes.__len__()==0:	# 염색체가 초기 상태이면 초기화한다. 
            ###염색체 모양 수정
            self.genes = [x for x in range(1, SIZE+1)]
            random.shuffle(self.genes)
                
    ### 적합도 함수 수정 단일최대거리 334
    def cal_fitness(self):		# 적합도를 계산한다. 
        self.fitness = 334*9;
        hvalue = 0
        
        hvalue += data.iloc[0, self.genes[0]]
        for i in range(SIZE-1):
            hvalue += data.iloc[self.genes[i], self.genes[i+1]]    
        hvalue += data.iloc[self.genes[SIZE-1],0]
        
        self.fitness -= hvalue
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
    max_value  = sum([c.cal_fitness() for c in population])
    pick    = random.uniform(0, max_value)
    current = 0
    
    # 룰렛휠에서 어떤 조각에 속하는지를 알아내는 루프
    for c in pop:
        current += c.cal_fitness()
        if current > pick:
            return c

# 교차 연산 two point crossover
def crossover(pop):
    
    father = select(pop)
    mother = select(pop)

    lindex = random.randint(1, SIZE - 3)
    rindex = random.randint(lindex+1, SIZE -2)
    
    fsel = father.genes[lindex:rindex]
    msel = mother.genes[lindex:rindex]
    
    child1 = father.genes[:]
    child2 = mother.genes[:]
    
    for i in msel:
        child1.remove(i)
    for i in fsel:
        child2.remove(i)

    child1 = child1[:lindex] + msel + child1[lindex:]
    child2 = child2[:lindex] + fsel + child2[lindex:]
    
#     print("f: ", father.genes, " fsel: ", fsel)
#     print("m: ", mother.genes, " msel: ", msel)
#     print("c1: " ,child1)
#     print("c2: ", child2)
    
    return (child1, child2)

    
# 돌연변이 연산 수정 완료
def mutate(c):
    for i in range(SIZE):
        if random.random() < MUTATION_RATE:
            idx = random.randint(0,SIZE-1)
            tmp = c.genes[idx]
            #print(c.genes)
            c.genes.pop(idx)
            c.genes.append(tmp)
            #print("idx " , idx, " tmp ", tmp)
            #print(c.genes)
            
population = []
i=0
fit=[]

# 초기 염색체를 생성하여 객체 집단에 추가한다. 
while i<POPULATION_SIZE:
    population.append(Chromosome())
    i += 1

count=0
population.sort(key=lambda x: x.cal_fitness(), reverse=True)
print(count, "th population")
print_p(population)
count=1

while population[0].cal_fitness() < 334*9 - 1018:
    new_pop = []

    for _ in range(POPULATION_SIZE//2):
        c1, c2 = crossover(population);
        new_pop.append(Chromosome(c1));
        new_pop.append(Chromosome(c2));

    # 자식 세대가 부모 세대를 대체한다. 
    # 깊은 복사를 수행한다. 
    population = new_pop.copy();    
    
    for c in population: mutate(c)

    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    fit.append(population[0].cal_fitness())
    #print("세대 번호=", count)
    #print_p(population)
    count += 1
    if count > 500:
        break
        
print("last population ", count-1)
print_p(population)

print()
print("최선의 결과")
path=[data.index[0]]
for j in population[0].genes:
    path.append(data.index[j])
path.append(data.index[0])
print(path, "거리 ", 334*9 - population[0].cal_fitness())


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["figure.figsize"] = (20,9)
df = pd.DataFrame(fit)
plt.plot(df.index, df[0])
plt.savefig('tsp_linear.png')
plt.show()
