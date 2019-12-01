import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from networkx import nx
from funcoesFinal import *

with open('Voos.json') as json_file:
    data = json.load(json_file)

with open('VoosLinhaUnica.json') as json_file:
    searchData = json.load(json_file)

listaDeAdjacencia = {}
listaAeroportos = []

for (key, aeroportoOrigem) in data['Origin'].items():
    if not listaDeAdjacencia.get(aeroportoOrigem):
        listaDeAdjacencia[aeroportoOrigem] = []
        listaAeroportos.append(aeroportoOrigem)

    listaDeAdjacencia[aeroportoOrigem].append(data['Dest'][key])

with open('listaAdjacencia.json', 'w') as json_file:
    json.dump(listaDeAdjacencia, json_file)

G = nx.Graph()
labels = {}

for aeroporto, rotas in listaDeAdjacencia.items():
    labels[aeroporto] = aeroporto
    G.add_node(aeroporto)

    for rota in rotas:        
        G.add_edge(aeroporto, rota, weight = recupera_distancia(searchData, aeroporto, rota))

labels['OGD'] = 'OGD'
labels['CYS'] = 'CYS'


prim, custo, pesos = executa_prim(G, 'ATL')
print("Árvore Geradora Mínima pelo algoritmo de Prim")
print(prim)
print("\n\n")
print("Custo Total da MST: ")
print(custo)
print("\n\n")
print("Custo individual das arestas da MST: ")
print(pesos)

posicoesNo = {}
x = 0
y = 0
for no in G.nodes():
    y += 1
    if y > 20:
        y = 1
        x += 4
    posicoesNo.update({no: (x, y)})

fig1 = plt.figure('Árvore Geradora Miníma')
nx.draw(G, labels = labels, pos = posicoesNo, edgelist = prim)
plt.show()

#-------------------------------------
origem, destino = coleta_origem_e_destino()
caminho, caminhoLegivel, distancia = dijkstra(G, origem, destino)
print('\n\n\nMenor Caminho com Menor Custo (MCMC) - Dijkstra')
print(caminhoLegivel)
print('\n\n\nCusto total considerando as distâncias entre pontos')
print(distancia)
print("\n\n")
fig2 = plt.figure('Menor Caminho com Menor Custo (MCMC) - Dijkstra')
nx.draw(G, pos = posicoesNo, nodelist=caminho, labels = labels, font_size = 13)
plt.show()