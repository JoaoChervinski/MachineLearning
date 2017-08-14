#Algoritmo Genetico
import random
import math
# Avaliando o fitness
def fitness(individuo):
	x = ''.join(map(str, individuo[0:10]))
	y = ''.join(map(str, individuo[10:20]))
	x = int(x, 2)
	y = int(y, 2)
	x = float(x - 512)/100
	y = float(y - 512)/100
	if x == 0 and y == 0: # Caso x e y forem 0, ocorrera erro na divisao, entao atribui um valor alto
		res = 10000000
	else:
		res = 1 / abs(- 20 - x**2 + 10 * math.cos(2*math.pi*x) -y**2 +10*math.cos(2*math.pi*y))
	return res

def seleciona_pais(probabilidades, individuos):
	selecionados = []
	for item in range(0,2):
		prob_gerada = random.uniform(0,1)
		for value in range(len(probabilidades)):
			if prob_gerada >= probabilidades[value] and prob_gerada < probabilidades[value + 1]:
				selecionados.append(individuos[value])
	return selecionados
soma_fitness = 0
prob_anterior = 0

def cruzamento(pais):
	descendente = []
	descendente = [0 for item in range(20)]
	descendente[0:10] = pais[0][0:10]
	descendente[10:20] = pais[1][10:20]
	return descendente

#Criar 100 individuos
individuos = []
gene = []

# Criando os individuos
for iteration in range(0,100):
	for run in range(0,20):
		x = random.randint(0,1)
		gene.append(x)
	individuos.append(gene)
	gene = []

# Adquirindo a soma total do fitness dos individuos
for item in individuos:
	soma_fitness += fitness(item)

probabilidades = []  # Armazena as probabilidades de cada individuo

for item in individuos:
	prob_individuo = prob_anterior + (fitness(item)/soma_fitness)
	probabilidades.append(prob_individuo)
	prob_anterior = prob_individuo

melhor_solucao = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] # Inicializa a lista

for run in range(200):
	novos_individuos = []
	while len(novos_individuos) < 100:
		pais = seleciona_pais(probabilidades, individuos)
		if len(pais) < 2:
			continue
		novo_individuo = cruzamento(pais)
		novos_individuos.append(novo_individuo)
	for item in novos_individuos:    # Mutacao dos genes com 20% de chance
		if random.uniform(0,1) <= 0.2:
			for gene in item:
				if random.uniform(0,1) <= 0.2:
					if gene == 0:
						gene = 1
					elif gene == 1:
						gene = 0
	for item in novos_individuos:
		if fitness(item) > fitness(melhor_solucao):
			melhor_solucao = item

melhor_x = ''.join(map(str, melhor_solucao[0:10]))
melhor_y = ''.join(map(str, melhor_solucao[10:20]))
melhor_x = int(melhor_x, 2)
melhor_y = int(melhor_y, 2)
melhor_x = float(melhor_x - 512)/100
melhor_y = float(melhor_y - 512)/100
resultado = (- 20 - melhor_x**2 + 10 * math.cos(2*math.pi*melhor_x) -melhor_y**2 +10*math.cos(2*math.pi*melhor_y))

print ("\n  Melhor Solucao  x: %.4f  y: %.4f -- Resultado: %f \n" % (melhor_x,melhor_y,resultado))
