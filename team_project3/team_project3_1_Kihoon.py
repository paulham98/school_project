import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
from matplotlib import animation

POPULATION_SIZE = 4# 개체 집단의 크기
MUTATION_RATE = 0.1	# 돌연 변이 확률
SIZE = 8			# 하나의 염색체에서 유전자 개수		
QUEEN = 8
# 염색체를 클래스로 정의한다. 
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()		# 유전자는 리스트로 구현된다. 
        self.fitness = 0		# 적합도
        if self.genes.__len__()==0:	# 염색체가 초기 상태이면 초기화한다. 
            i = 0
            temp_set = set()
            while i<SIZE:
                input = random.randint(1,QUEEN)
                if input not in temp_set:
                    self.genes.append(input) 
                    temp_set.add(input)               
                    i += 1
        self.cal_fitness()
        
    def cal_fitness(self):		# 적합도를 계산한다. 
        self.fitness = int((QUEEN)*(QUEEN-1)/2);
        collison=set()
        for i in range(SIZE):
            left = i-1;right = i+1;
            count = 1
            while left>-1 or right<SIZE:
                if left>=0:
                    if self.genes[i]-self.genes[left]==0 or abs(self.genes[i]-self.genes[left])==count:
                        collison.add((i,left))
                    left -=1
                if right<SIZE:
                    if self.genes[i]-self.genes[right]==0 or abs(self.genes[i]-self.genes[right])==count:
                        collison.add((right,i))
                    right +=1
                count +=1
        self.fitness -= len(collison)
        # print(collison)
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
    max_value  = sum([c.fitness for c in pop])
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
    for i in range(SIZE):
        if random.random() < MUTATION_RATE:
            check=True
            temp =set(c.genes)
            new_input= random.randint(0,QUEEN-1)
            while new_input==i+1:
                new_input = random.randint(0,QUEEN-1)
            c.genes[i],c.genes[new_input]= c.genes[new_input],c.genes[i]
    if check:
        c.cal_fitness()
def print_board(board:list):
    board_array = []
    for queen in board:
        temp = [0 if queen-1!=x else 1 for x in range(QUEEN)]
        board_array.append(temp)
    for i in range(QUEEN):
        print(board_array[i])
# 초기 염색체를 생성하여 객체 집단에 추가한다. 
def start(num,check=False):
    population = []
    i=0
    while i<POPULATION_SIZE+num:
        population.append(Chromosome())
        i += 1
    count=0
    # population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    print("세대 번호=", count)
    print_p(population)
    count=1
    population_fitness = []
    while population[0].cal_fitness() < int((QUEEN)*(QUEEN-1)/2):
        # new_pop = []
        # 선택과 교차 연산
        for _ in range((POPULATION_SIZE+num)//2):
            c1, c2 = crossover(population);
            population.append(Chromosome(c1));
            population.append(Chromosome(c2));
        
        # 자식 세대가 부모 세대를 대체한다. 
        # 깊은 복사를 수행한다. 
        population.sort(key=lambda x: x.fitness, reverse=True)
        population = population[:POPULATION_SIZE+num]
        
        # 돌연변이 연산
        for c in population: mutate(c)

        # 출력을 위한 정렬
        population.sort(key=lambda x: x.fitness, reverse=True)
        print("세대 번호=", count , "=======================")
        print_p(population)
        count += 1
        population_fitness.append(float(sum([x.fitness for x in population])/(POPULATION_SIZE+num)))
        if count > 1000 : break;
    print(count)
    print(len(population_fitness))
    print(population_fitness)
    if check:
        plt.scatter(x=[c for c in range(1,count)],y=population_fitness,color='b')
        # print_board(population[0].genes)
        plt.savefig('{}-queen_{}-size.png'.format(QUEEN,POPULATION_SIZE+i))
        plt.show()
        plt.close()
    return population_fitness

# 메인 프로그램
new_result= []
population_size_with_create_child = []
for i in range(0,50):
    if i==0:
        new_result.append(start(i,True))
    else:
        new_result.append(start(i,False))
for i in range(0,50):
    print(i+POPULATION_SIZE," >>>>" ,new_result[i])
    population_size_with_create_child.append([i+POPULATION_SIZE,len(new_result[i])])
plt.plot(population_size_with_create_child,color='b')
plt.xlabel('POPULATION_SIZE');plt.ylabel("CREATE CHILD");
plt.savefig('population-make-child.png')
plt.legend()
plt.show()
plt.close()
print(population_size_with_create_child)
# fig ,axs = plt.figure(ncols =3, figsize=(10,3) , subplot_kw={"projection":"3d"})
# fontlabel = {"fontsize":"large", "color":"gray", "fontweight":"bold"}

# plt.scatter(x=[c for c in range(1,count)],y=population_fitness,color='b')
# print_board(population[0].genes)
# plt.savefig('8-queen.png')
# plt.show()
# a = Chromosome([1,6,8,3,7,4,2,5])
# print(a.cal_fitness())