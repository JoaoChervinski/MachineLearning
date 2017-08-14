import math
import random

def gera_estado(x,y):
    if random.uniform(0,1) > 0.5:
        acrescimo = round(random.uniform(0,0.15), 3)
        if (x + acrescimo) > 5:
            x = x - acrescimo
        else:
            x = x + acrescimo
    else:
        decrescimo = round(random.uniform(0,0.15), 3)
        if (x - decrescimo) < -5:
            x = x + decrescimo
        else:
            x = x - decrescimo
    if random.uniform(0,1) > 0.5:
        acrescimo = round(random.uniform(0,0.15), 3)
        if (y + acrescimo) > 5:
            y = y - acrescimo
        else:
            y = y + acrescimo
    else:
        decrescimo = round(random.uniform(0,0.15), 3)
        if (y - decrescimo) < -5:
            y = y + decrescimo
        else:
            y = y - decrescimo
    estado = [x,y]
    return estado

def calcula_custo(x,y):
        custo = - 20 - x**2 + 10 * math.cos(2*math.pi*x) -y**2 +10*math.cos(2*math.pi*y)
        return custo

def prob_aceitacao(custo_atual,custo_novo,temperatura):
    prob = math.exp((custo_novo - custo_atual)/ temperatura)
    return prob

T = 100
T_min = 1

posx = round(random.uniform(-5,5), 3)
posy = round(random.uniform(-5,5), 3)
estado_atual = [posx,posy]
custo_atual = calcula_custo(estado_atual[0],estado_atual[1])
melhor_solucao = estado_atual[::]


while T > T_min:
    i = 1
    while i <= 10000:

        novo_estado = gera_estado(estado_atual[0],estado_atual[1])
        custo_novo = calcula_custo(novo_estado[0],novo_estado[1])
        pa = prob_aceitacao(custo_atual, custo_novo, T)

        if custo_novo > custo_atual:
            estado_atual[::] = novo_estado[::]
            melhor_solucao = novo_estado[::]
        elif custo_atual > custo_novo:
            if pa < random.uniform(0,1):
                estado_atual[::] = novo_estado[::]
        i = i + 1

    T = T - 0.5

print("Melhor Solucao:%s" % (melhor_solucao))
print "Custo: ", calcula_custo(melhor_solucao[0],melhor_solucao[1])
