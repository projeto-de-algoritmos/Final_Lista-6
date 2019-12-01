from pqdict import PQDict


def recupera_distancia(searchData, aeroportoOrigem, aeroportoDestino):
    for dicionario in searchData:
        if aeroportoOrigem == dicionario['Origin'] and \
            aeroportoDestino == dicionario['Dest']:
            return dicionario['Distance']

def executa_prim(G, primeiro_no):
   
    no_de_parada = G.number_of_nodes() - 1
    atual = primeiro_no
    visitados = set() # Tira os repetidos e é uma Hash
    min_heap = PQDict() # É um min_heap
    mst = []
    peso_total = 0
    pesos = []

    while len(mst) < no_de_parada:
        # print("Esse é o visitados", visitados)
        # print("Esse é o min_heap: ", min_heap)
        for noVizinho in G.neighbors(atual):
            # print("Esse é o no: ", noVizinho)
            # print("Esse é o atual: ", atual)
            if noVizinho not in visitados and atual not in visitados:
                if(atual, noVizinho) not in min_heap and (noVizinho, atual) not in min_heap:
                    peso_aresta = G[atual][noVizinho]['weight']
                    min_heap.additem((atual, noVizinho), peso_aresta)
        
        visitados.add(atual)

        aresta, peso = min_heap.popitem() # Tira a raiz
        while(aresta[1] in visitados): # Aresta[1] é o vizinho
            aresta, peso = min_heap.popitem() # Vai tirando a raiz até encontrar um vizinho não visitado
            # print("Essa é a aresta: ", aresta)
            # print("Esse é o peso: ", peso)
        peso_total += peso
        pesos.append(peso)
        mst.append(aresta)
        atual = aresta[1]

    return mst, peso_total, pesos