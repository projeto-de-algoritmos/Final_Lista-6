import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from networkx import nx
from funcoesFinal import *

def main():
    iniciar_programa()
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

    posicoesNo = {}
    x = 0
    y = 0
    for no in G.nodes():
        y += 1
        if y > 20:
            y = 1
            x += 4
        posicoesNo.update({no: (x, y)})

    while True:
        os.system("clear")
        perfil = exibe_menu_perfil()
        if perfil == 1:
            print("\033[0;32mOlá! Meu caro turista!\033[0m")
            time.sleep(1)
            print("\033[0;32mPrimeiro...\033[0m")
            time.sleep(1)
            origem = str(input("\033[0;32mDe que lugar você está saindo? \033[0m"))
            print("\033[0;32mOk!\033[0m")
            time.sleep(0.5)
            destino = str(input("\033[0;32mPara onde você gostaria de ir? \033[0m"))
            print("\033[0;32mEstamos consultando o Dijkstra para obter a melhor rota com menor custo para você... aguarde\033[0m")
            time.sleep(1.5)
            caminho, caminhoLegivel, distancia = dijkstra(G, origem, destino)
            print('\n\n\033[0;32mEssa é a menor rota: \033[0m')
            print(caminhoLegivel)
            print('\n\n\033[0;32mDistância para chegar ao destino (Custo) \033[0m')
            print(distancia)
            print("\n\n")
            fig2 = plt.figure('Menor Caminho com Menor Custo (MCMC) - Dijkstra')
            nx.draw(G, pos = posicoesNo, nodelist=caminho, labels = labels, font_size = 13)
            plt.show()
            print("\033[0;32mVamos arrumar as malas! \033[0m")
            time.sleep(0.5)
            capacidadeMala = coleta_capacidade_da_mala()
            # executa_knapsack(itens, capacidadeMala)

        elif perfil == 2:
            while True:
                os.system("clear")
                opcao = exibe_menu_agencia_de_viagens()
                if opcao == 1:
                    prim, custo, pesos = executa_prim(G, 'ATL')
                    print("Árvore Geradora Mínima pelo algoritmo de Prim")
                    print(prim)
                    print("\n\n")
                    print("Custo Total da MST: ")
                    print(custo)
                    print("\n\n")
                    print("Custo individual das arestas da MST: ")
                    print(pesos)
                    fig1 = plt.figure('Árvore Geradora Miníma')
                    nx.draw(G, labels = labels, pos = posicoesNo, edgelist = prim)
                    plt.show()
                    input("Aperte ENTER para voltar ao menu ")
                elif opcao == 2:
                    origem, destino = coleta_origem_e_destino()
                    caminho, caminhoLegivel, distancia = dijkstra(G, origem, destino)
                    print('\n\nEssa é a menor rota:')
                    print(caminhoLegivel)
                    print('\n\nDistância para chegar ao destino (Custo)')
                    print(distancia)
                    print("\n\n")
                    fig2 = plt.figure('Menor Caminho com Menor Custo (MCMC) - Dijkstra')
                    nx.draw(G, pos = posicoesNo, nodelist=caminho, labels = labels, font_size = 13)
                    plt.show()
                    input("Aperte ENTER para voltar ao menu ")
                else:
                    break
        else:
            os.system("clear")
            print("Ajudante encerrado com sucesso!")
            break

main()