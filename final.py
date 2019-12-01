import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from networkx import nx
from funcoesFinal import *

df = pd.read_csv('2008.csv')
df = df.drop_duplicates(subset=['Origin', 'Dest'], keep='first')
df.to_json('Voos.json')

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