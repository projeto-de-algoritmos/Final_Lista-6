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

def coleta_origem_e_destino():
    origem = str(input("Origem: "))
    destino = str(input("Destino: "))
    
    return origem, destino

def dijkstra(G, origem, destino, visitados = [], distancias = {}, predecessores = {}):
    # Verifica se os valores passados para origem e destino existem no Grafo
    if origem not in G:
        raise TypeError('Local de origem indicado não existe na carta do aerporto')
    if destino not in G:
        raise TypeError('Local de destino indicado não existe na carta do aerporto')    
    
    # Condição de parada da recursão, quando chega no nó destino
    if origem == destino:
        
        caminho = []
        pred = destino

        # Aqui realiza o backtracking para mostrar o caminho a partir da origem
        while pred != None:
            caminho.append(pred) # Append coloca no começo
            pred = predecessores.get(pred, None)
        
        # Inicializando a variável de caminho legível
        caminhoLegivel = caminho[0] # Coloca a origem no caminho legível que é uma maneira mais agradável visualmente de mostrar o caminho
        
        # Completa o caminho de forma legível
        for i in range(1, len(caminho)): 
            caminhoLegivel = caminho[i] + ' ---> ' + caminhoLegivel

        return caminho, caminhoLegivel, distancias[destino]
 
    else :     
        # Se a lista de visitados estiver vazia, significa que ele está no nó de origem e a distância é zero
        if not visitados: 
            distancias[origem] = 0

        # Percorre os vizinhos do nó de origem
        for vizinho in G[origem] :
            # Confere se o vizinho não foi visitado
            if vizinho not in visitados:
                # print(distancias[origem])
                # print(G[origem][vizinho])
                nova_distancia = distancias[origem] + G[origem][vizinho]['weight'] # Guarda a soma da distância armazenada no nó de origem mais a do novo nó
                # float('inf') -> funciona como se fosse um valor infinito
                if nova_distancia < distancias.get(vizinho, float('inf')):  # Atualiza as distâncias e os predecessores caso a nova distância
                                                                            # seja menor que as armazenadas... Expande a mancha
                    distancias[vizinho] = nova_distancia
                    predecessores[vizinho] = origem
                    
        visitados.append(origem) # Coloca o nó atual nos visitados

        naoVisitados = {} # Cria um dict para guardar os nós não visitados para chamar na recursão

        for no in G: # Percorre todos os nós do grafo
            if no not in visitados: # Se o nó não tiver nos visitados
                naoVisitados[no] = distancias.get(no, float('inf')) # 'no' é a key e o distancias.get é o value do dict        
        
        # Pega o nó não visitado que possui a menor distância
        novoNo = min(naoVisitados, key = naoVisitados.get)

        # chama recursivo pro novo nó
    return dijkstra(G, novoNo, destino, visitados, distancias, predecessores)