#!usr/bin/env/python 3
# -*- coding: utf-8 -*
'''(1) Inicializar membership aleatoriamente
   (2) A partir dos valores dos centróides, atualizar o membership de cada elemento
       para o centróide mais próximo
   (3) Atualizar centróides calculando a média dos pontos membros de cada cluster
   (4) Se nenhum elemento mudou de cluster, parar, senão repetir passo 1 '''

import warnings
import matplotlib.patches as mpatches
from random import randint
from math import sqrt
from matplotlib import pyplot as plt
import copy, time

# Suprime a mensagem de erro de deprecated do matplotlib
warnings.filterwarnings("ignore")

plt.ion()

def init(filename):
    # Função que abre o arquivo com os dados das coordenadas e inicializa os centroides aleatoriamente
    dataset = []
    with open('dataset.txt') as f:
        data = f.readlines()
        for line in range(len(data)):
            data[line] = data[line].strip('\n')
            data[line] = data[line].split()
            dataset.append([float(data[line][0]), float(data[line][1]), int(randint(0,3))])
    return dataset

def update_membership(dataset):
    centroids = []
    for centroid in range(4):
        pos_x, pos_y, members = (0,0,0)
        for item in dataset:
            if item[2] == centroid:
                pos_x += float(item[0])
                pos_y += float(item[1])
                members += 1
        if members > 0:
            centroid_position = (pos_x / members, pos_y / members)
            centroids.append(centroid_position)
        else:
            # Se um dos clusters ficar sem membros, atribui clusters aleatórios
            print("Bad initialization values, reinitializing membership.")
            for line in range(len(dataset)):
                dataset[line][2] = random.randint(0, 3)
            centroid_position = (pos_x / members, pos_y / members)
            centroids.append(centroid_position)

    for i in range(len(dataset)):
        distances = []
        for centroid in range(4):
            distances.append(sqrt((dataset[i][0] - centroids[centroid][0])**2 + (dataset[i][1] - centroids[centroid][1])**2 ))
        dataset[i][2] = distances.index(min(distances)) # Atualiza o membership para o centróide + próximo


def write_to_file(dataset):
    with open('result.dat', 'w') as file:
        for line in dataset:
            file.write('{} {} {}\n'.format(line[0], line[1], line[2]))

def plot(dataset, iteration):
    colors = ['red', 'green', 'blue', 'black']
    red_patch = mpatches.Patch(color='red', label='Cluster 1')
    green_patch = mpatches.Patch(color='green', label='Cluster 2')
    blue_patch = mpatches.Patch(color='blue', label='Cluster 3')
    black_patch = mpatches.Patch(color='black', label='Cluster 4')
    plt.legend(handles=[red_patch, green_patch, blue_patch, black_patch])
    for centroid in range(4):
        plt.title('Iterations: {}'.format(iterations))
        plt.scatter([c[0] for c in dataset if c[2] == centroid], [c[1] for c in dataset if c[2] == centroid], c = colors[centroid])
        plt.pause(0.1)
    # plt.close()


d = init('dataset.txt')
iterations = 'Initializing'
plot(d, iterations)
iterations = 0
while True:
    iterations += 1
    old = copy.deepcopy(d)
    update_membership(d)
    if d == old:
        print ("Iterations: {}".format(iterations))
        print ("Image saved in 'clusters.png' and clusters info saved in 'result.dat'.")
        break
    plot(d, iterations)
    plt.savefig('clusters.png')
write_to_file(d)
