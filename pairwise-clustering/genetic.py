#!usr/bin/env/python3
# -*- coding : utf-8 -*-
from random import randint, uniform
import numpy as np
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt

def init(filename):
    # Função que abre o arquivo com os dados das coordenadas
    dataset = []
    with open('dataset.txt') as f:
        data = f.readlines()
        for line in range(len(data)):
            data[line] = data[line].strip('\n')
            data[line] = data[line].split()
            dataset.append([float(data[line][0]), float(data[line][1])])
    return dataset

def euclidean_distance(x, y):
    return ((x[0] - y[0])**2 + (x[1] - y[1]) ** 2) ** 0.5

def gen_matrix(dataset):
    matrix = np.zeros((len(dataset), len(dataset)))
    # Para cada item do dataset
    for i in range(len(dataset)):
        for j in range(len(dataset)):
            matrix[i][j] = euclidean_distance(dataset[i], dataset[j])
    return matrix


def entropy(K, d_matrix, chromosome, dataset):
    # O fitness de cada indivíduo é a entropia de sua matriz de dissimilaridade
    # Calcula a entropia do cromossomo
    total_sum = 0
    for v in range(K): # Para cada cluster
        inner_sum = 0
        for k in range(len(dataset)):
            for l in range(len(dataset)):
                # Se Mkv = 1 e Mlv = 1
                if chromosome[k].index(1) == v and chromosome[l].index(1) == v:
                    inner_sum += d_matrix[k][l]
        total_sum += 1/(2 * pv(v, chromosome, len(dataset)) * len(dataset)) * inner_sum
    # Queremos o indivíduo com menor dissimilaridade, então inverte
    return total_sum


def select_parents(probabilities, chromosomes):
    selected = []
    for i in range(2):
        prob = uniform(0,1)
        for value in range(len(probabilities) - 1):
            if prob >= probabilities[i] and prob < probabilities[value + 1]:
                selected.append(chromosomes[i])
    return selected


def pv(v, chromosome, dset_size):
    sm = 0
    # Para cada item do dataset
    for k in range(dset_size):
        if chromosome[k].index(1) == v:
            # Mkv/N
            sm += 1/(dset_size)
    return sm

def crossover(parents, dset_size):
    if dset_size % 2 == 0:
        crossover_site = int(dset_size/2)
        child = parents[0][:crossover_site] + parents[1][crossover_site:]
    return child

def write_to_file(dataset, chromosome):
    with open('result.dat', 'w') as file:
        for line in range(len(dataset)):
            file.write('{} {} {} \n'.format(dataset[line][0], dataset[line][1], chromosome[line].index(1)))

def plot(filename, K):
    dataset = []
    with open(filename) as f:
        data = f.readlines()
        for line in range(len(data)):
            data[line] = data[line].strip('\n')
            data[line] = data[line].split()
            dataset.append([float(data[line][0]), float(data[line][1]), int(data[line][2])])

    colors = ['red', 'green', 'blue', 'black']
    red_patch = mpatches.Patch(color='red', label='Cluster 1')
    green_patch = mpatches.Patch(color='green', label='Cluster 2')
    blue_patch = mpatches.Patch(color='blue', label='Cluster 3')
    black_patch = mpatches.Patch(color='black', label='Cluster 4')
    plt.legend(handles=[red_patch, green_patch, blue_patch, black_patch])

    for centroid in range(4):
        plt.title('Clusters')
        plt.scatter([float(c[0]) for c in dataset if int(c[2]) == centroid], [float(c[1]) for c in dataset if int(c[2]) == centroid], c = colors[centroid])
    plt.show()


def main():
    ########## INICIALIZAÇÃO ##########
    # Carrega o conjunto de dados para a variável dataset
    dataset = init('dataset.txt')
    # Inicializa os centróides aleatóriamente
    chromosomes = [[[0 for x in range(4)] for y in range(len(dataset))] for individual in range(100)]
    for c in range(len(chromosomes)):
        for line in range(len(chromosomes[c])):
            chromosomes[c][line][randint(0,3)] = 1 # Atribui um cluster aleatório para o item
    # Gera a matriz de dissimilaridade entre os elementos do dataset.
    d_matrix = gen_matrix(dataset)

    # Inicializa o melhor indivíduo com um indivíduo qualquer, será substituído a medida
    # que a população for melhorando
    best_individual = chromosomes[0]


    for epoch in range(40):
        print ("Epoch: {}".format(epoch + 1))
        fitness = []
        for i in range(len(chromosomes)):
            fitness.append(entropy(4, d_matrix, chromosomes[i], dataset))

        total_fitness = sum(fitness)
        probabilities = []
        previous_prob = 0

        for c in chromosomes:
            # Normaliza as probabilidades
            c_prob = previous_prob + (entropy(4, d_matrix, c, dataset)/total_fitness)
            probabilities.append(c_prob)
            previous_prob = c_prob

        new_individuals = []
        # Até criar uma nova população
        while len(new_individuals) < 100:
            parents = select_parents(probabilities, chromosomes)
            # Se não foram selecionados dois pais, volta pro início do loop
            if len(parents) < 2:
                continue
            new_individuals.append(crossover(parents, len(dataset)))

        # Realiza mutações nos indivíduos
        for i in range(len(new_individuals)):
            for line in range(len(new_individuals[i])):
                if uniform(0,1) <= 0.05: # 5% de chance de mutação
                    new_individuals[i][line] = [0,0,0,0]
                    new_individuals[i][line][randint(0,3)] = 1

        for i in new_individuals:
            if entropy(4, d_matrix, i, dataset) > entropy(4, d_matrix, best_individual, dataset):
                best_individual = i

        chromosomes = new_individuals

    write_to_file(dataset, best_individual)
    plot('result.dat', 4)
main()
