
# coding: utf-8

# In[245]:

import math
import random 
import numpy as np
from bitarray import bitarray

class Solver_8_queens:
    
    def __init__(self, pop_size=300, cross_prob=1, mut_prob=0.8):
        self.pop_size, self.cross_prob, self.mut_prob = pop_size, cross_prob, mut_prob
    
    #оператор создания начальных популяций
    def first_populat(self):
        count = 0
        while count != self.pop_size:
            qp = np.random.randint(0,8, (8,))
            count += 1
            return list(qp)

    # окей, нач популяц сгенерили

    # далее на очереди фитнесс-функция
    def fitness(self, osob):
        k = 0
        lst = osob
        for i in range(8):
            for j in range(i + 1, 8):
                if abs(i - j) == abs(lst[i] - lst[j]) or lst[i] == lst[j]:
                    k += 1
        return (1 - k / 28)
    #окей, фитнесс врде есть

    
    # займемся оператором репродукции
    def reproduce(self, fitness_list, population):
        #выбираем особей для селекции колесом рулетки
        #parent = []
        fitness_sum = sum(fitness_list)
        rand_value = random.random() * fitness_sum
        for count, value in enumerate(fitness_list):
            rand_value -= value
            if rand_value <= 0:
                #parent.append(self.population[count])
                return population[count]
    #будем сичтать что особей для скрещивания выбрали, займемся кроссоверингом

    #делается типа в три этапа 1-выбор родителей для скрещ, 2-случайной выб. точка скрещивания, 3-обмен хромосомами
    def crossover(self, parent1, parent2):
        childrens = []
        if random.random() <= self.cross_prob:
            cross_point = random.randint(1, len(parent1) - 1)
            child1, child2 = parent1[:cross_point] + parent2[cross_point:], parent2[:cross_point] + parent1[cross_point:]
            childrens.append(child1)
            childrens.append(child2)
        return childrens #ну вот типа возвращает список, в нем 2 ребенка

    #теперь чe, теперь мутация
    def mutate(self, population, mut_rate):
        for osob in population:
            if random.random() <= mut_rate:
                point = random.randint(0, 7)
                value = random.randint(0, 7)
                osob[point] = value
                
    #походу остается, сделать визуализатор лучш особи, и  все это дело заупстить, чтоб работало
    def visual(self, osob):
        deck = []
        for i in range(64):
            deck.append('+')
        deck = np.array(deck)
        deck.resize(8,8)

        for (j,i) in zip(range(len(osob)),osob):
            deck[j, i] = 'Q'
        return deck
        

    #Solve на очереди
    def solve(self, min_fitness=0.95, max_epochs=10000):
        epoch_num, best_fitn_value = 0, 0
        best_osob = []
        max_fitness_value = 0
        population = []
        population.append(self.first_populat())

        while (min_fitness == None or max_fitness_value < min_fitness) and (max_epochs==None or epoch_num <= max_epochs):

            # запишем значения фитнесс ф-ции
            all_fitness_values = []
            #print(population)
            for osob in population:
                all_fitness_values.append(self.fitness(list(osob)))
            max_fitness_value = max(all_fitness_values)
                
            #отберем особей для скрещивания, если че над будет переделать
            parents1 = [self.reproduce(all_fitness_values, population) for i in range(len(population)//2)]
            
            parents2 = [self.reproduce(all_fitness_values, population) for i in range(len(population)//2)]
            
            #покрестим особей
            for i,j in zip(parents1, parents2):
                children = self.crossover(i, j)
                population.append(i for i in children)
            #добавили детей в попуцляцию, можно запустить мутацию
            self.mutate(population, self.mut_prob)
            #ок, кого-то замутировали, можно заканчивать всю эту тему
            epoch_num += 1
            best_fitn_value = max(all_fitness_values)
            best_osob = population[all_fitness_values.index(best_fitn_value)]
            best_osob_index = all_fitness_values.index(max(all_fitness_values))
            
        return best_fitn_value, epoch_num, self.visual(population[best_osob_index])

