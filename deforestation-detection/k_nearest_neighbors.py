#! /usr/bin/env python2
# -*- encoding: utf-8 -*-
import sys, os
from math import sqrt
import numpy as np
import argparse


def convertList(l):
    # Função para converter os itens da lista para inteiros
    for item in range(len(l)):
        l[item] = int(l[item])
    return l

def createDataset(path, c, dataset):
    # Extrai as informações de cor das imagens e gera um dataset.
    # Salva em um arquivo os nomes das imagens no diretório passado
    os.system('ls {}/*ppm > filenames.txt'.format(path))
    with open('filenames.txt') as f:
        names = f.readlines()

    # Remove caracteres de formatação
    for line in range(len(names)):
        names[line] = names[line].strip('\n')


    # Para cada arquivo de treinamento
    for name in names:
        item = []
        with open(name, 'r+') as img:
            img_data = img.read()
            img_data = img_data.replace('\n', ' ')
            img_data = img_data.split()
            red = convertList(img_data[4::3])
            green = convertList(img_data[5::3])
            blue = convertList(img_data[6::3])

            # Calcula a média dos valores RGB de toda a imagem (8x8 pixels)
            avg = (sum(red)/len(red), sum(green)/len(green), sum(blue)/len(blue))

            # Salva os valores RGB em uma lista, juntamente com sua classificação
            item.append(avg[0])
            item.append(avg[1])
            item.append(avg[2])
            item.append(c)
            dataset.append(item)

    # Remove o arquivo auxiliar
    os.system('rm filenames.txt')
    return

def readImage(image):
    # Lê a imagem ppm e organiza em um formato adequado
    # para salvar em uma matriz
    with open(image) as img:
        img_data = img.read()
        img_data = img_data.replace('\n', ' ')
        img_data = img_data.split()

        # Cada 'chunk' ou linha pertencente ao bloco 8x8, é composto
        # de 24 itens(8 triplas RGB), formando no final um bloco correspondente
        # a 64 pixels
        chunk_size = int(img_data[1]) * 3

        # Cria um auxiliar com os dados da imagem sem o cabeçalho
        aux = img_data[4:]

        # Armazena os dados do cabeçalho para reconstruir a imagem posteriormente
        header = img_data[:4]

        # Divide a imagem em n partes, onde n é o número de linhas
        img_matrix = [aux[i:i + chunk_size] for i in xrange(0, len(aux), chunk_size)]

    return img_matrix, img_data, header


def everyPatch(image, block_size):
    # Divide a imagem em vários patches de 8x8 pixels
    width = len(image[1]) # nº de colunas
    height = len(image) # nº de linhas
    position = (0,0) # Linha x Coluna
    patches = []

    while True:
        patch = []

        for index in range(position[0], position[0] + block_size):
            # Cria um patch 8x8 composto por 8 listas(uma para cada linha)
            # e 24 valores por lista (8 red, 8 green, 8 blue)
            patch.append(image[index][position[1]: position[1] + block_size * 3])

        patches.append(patch)
        if (position[1] + block_size * 3) < width: # Se ao incrementar a coluna em 24, a largura da imagem não for ultrapassada
            position = (position[0], position[1] + block_size * 3) # Move a posição para 24 colunas à direita
        else: # Se a largura da imagem for ultrapassada
            if (position[0] + block_size >= height): # Se estiver na base da imagem
                break
            else: # Se ainda não estiver na base da imagem
                position = (position[0] + block_size, 0) # Muda a posição para 8 linhas abaixo (linha de blocos abaixo)

    return patches

def euclideanDistance(x, y):
    # Calcula a distância euclidiana entre os elementos
    s = (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2
    return sqrt(s)

def classify(patches, k, block_size):
    global dataset
    for p in range(len(patches)):
        # Para cada bloco 8x8 que compõe a imagem
        distance = []
        l = []
        for _ in patches[p]:
            # Lista auxiliar que une as 8 linhas de um bloco em uma lista só
            l += _

        red = convertList(l[0::3])
        green = convertList(l[1::3])
        blue = convertList(l[2::3])

        # Calcula a média RGB do bloco 8x8
        avg = (sum(red)/len(red), sum(green)/len(green), sum(blue)/len(blue))
        for item in dataset:
            # Adiciona na lista de distância tuplas contendo na primeira posição a distância do item atual para os valores
            # do dataset, e na segunda posição a classificação
            distance.append((euclideanDistance(avg, item), item[3]))
        distance = sorted(distance, key=lambda d: d[0]) # Ordena a lista pelas distâncias
        d = 0
        f = 0
        if (k % 2)  == 0: # Se o k for par transforma em ímpar
            k -= 1
        if k <= 0:
            k = 1

        for _ in range(k):
            if distance[_][1] == 'd':
                d += 1
                # print 'd'
            else:
                f += 1
                # print 'f'
        if d > f:
            # Cria um bloco 8x8 totalmente vermelho, para substituir blocos classificados
            # como desmatados
            patches[p] = [[255 if x % 3 == 0 else 0 for x in range(block_size * 3)] for y in range(block_size)]

    return patches

def rebuildImage(image, header, block_size):
    # Função que reconstrói a imagem com os blocos classificados
    width = int(header[1])
    height = int(header[2])
    start = 0
    end = width/block_size
    lines = []

    for _ in range(height/block_size):
        # Cria uma lista com as linhas de blocos que compõe a imagem
        lines.append(np.hstack(image[start:end]))
        start += width/block_size
        end += width/block_size

    # Junta as linhas de blocos verticalmente, formando a matriz da imagem
    rebuilt = np.vstack(lines)

    with open('output.ppm', 'w') as img:
        # Abre o arquivo de saída e escreve o header ppm
        img.write('{}\n'.format(header[0]))
        img.write('{} {}\n'.format(header[1], header[2]))
        img.write('{}\n'.format(header[3]))
        for j in rebuilt:
            for i in j:
                img.write('{} '.format(str(i)))

    return

def main(args):
    global dataset
    dataset = []

    # Cria os conjuntos de dados para uso do k-nn
    createDataset('desmatado1', 'd', dataset)
    createDataset('floresta', 'f', dataset)

    if args.k > len(dataset):
        print "O valor escolhido para k é muito alto! Aumente o número de amostras ou diminiua o valor de k."
        raise SystemExit

    # Imagem para classificar é passada por argumento
    img_matrix, img_data, header = readImage(args.filename)
    # Pega todos os patches 8x8 da imagem
    p = everyPatch(img_matrix, args.block_size)
    # Classifica os patches e retorna a imagem destacada
    new_img = classify(p, args.k, args.block_size)

    # Chama a função que reconstrói a imagem
    rebuildImage(new_img, header, args.block_size)


parser = argparse.ArgumentParser(description='Classificação de imagens')
parser.add_argument('filename', type=str, help='Nome do arquivo de imagem')
parser.add_argument('k', type=int, help='Valor de K')
parser.add_argument('block_size', type = int, help='Dimensões do bloco* (tamanho x tamanho) \n * Tanto a altura quanto \
a largura da imagem escolhida devem ser múltiplos do tamanho de bloco passado como argumento, caso contrário ocorrerão erros.')

args = parser.parse_args()

main(args)
