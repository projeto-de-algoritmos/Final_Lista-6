from pqdict import PQDict
import time

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
                # print(G[origem])
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

def coleta_capacidade_da_mala():
    print("\033[0;32mO valor da capacidade deve ser um inteiro\033[0m")
    capacidade = int(input("Qual é a capacidade da sua Mala(l): "))
    capacidade = valida_capacidade(capacidade)

    return capacidade
    
def valida_capacidade(capacidade):
    while(capacidade <= 0):
        print("Capacidade inválida! Digite um valor maior que 0 e inteiro!")
        capacidade = int(input("Qual é a capacidade da sua Mala(l): "))
    return capacidade   

def executa_knapsack(itens, capacidade, searchData, origem, destino):
    qtdTotalProdutos = len(itens)

    tabelaKnapsack = [[0 for coluna in range(capacidade + 1)] for linha in range(qtdTotalProdutos + 1)]

    for linha in range(qtdTotalProdutos + 1):
        nomeItem = itens[linha-1][0]
        pesoItem = itens[linha-1][1]
        if (recupera_valor(searchData,origem,destino) == "InteriorFrio"):
            valorItem = itens[linha-1][2]
        elif (recupera_valor(searchData,origem,destino) == "InteriorCalor"):
            valorItem = itens[linha-1][3]
        elif (recupera_valor(searchData,origem,destino) == "LitoralCalor"):
            valorItem = itens[linha-1][4]
        elif (recupera_valor(searchData,origem,destino) == "LitoralFrio"):
            valorItem = itens[linha-1][5]
        
        print(recupera_valor(searchData,origem,destino))
        for coluna in range(capacidade + 1):
            if linha == 0 or coluna == 0:
                tabelaKnapsack[linha][coluna] = 0
            elif pesoItem > coluna:
                tabelaKnapsack[linha][coluna] = tabelaKnapsack[linha-1][coluna]
            else:
                # LEVAR / NAO LEVAR
                tabelaKnapsack[linha][coluna] = max(tabelaKnapsack[linha-1][coluna], tabelaKnapsack[linha-1][coluna - pesoItem] + valorItem)


    itensLevados = []
    limite = capacidade
    for linha in range(len(itens), 0, -1):
        estaNaMala = False
        # print(linha)
        # print(limite)
        if(tabelaKnapsack[linha][limite] != tabelaKnapsack[linha-1][limite]):
            estaNaMala = True
        
        if estaNaMala:
            pesoItem = itens[linha-1][1]
            itensLevados.append(itens[linha-1])
            limite -= pesoItem

    return tabelaKnapsack, itensLevados

def monta_tupla(data):
    itens = []
    for item in data:
        itens.append((item['Nome'], item['Peso'], item['ValorInteriorFrio'], item['ValorInteriorQuente'], item['ValorLitoralQuente'], item['ValorLitoralFrio']))
    return itens

def recupera_valor(searchData,aeroportoOrigem,aeroportoDestino):
    for dicionario in searchData:
        if aeroportoOrigem == dicionario['Origin'] and \
            aeroportoDestino == dicionario['Dest']:
            return dicionario['TypeDest']

def exibe_menu_perfil():
    print("==================== PERFIL ===================")
    print("1 - Turista")
    print("2 - Agência de viagens")
    print("0 - Sair")
    print("\nDigite o número correspondente a opção desejada")
    perfil = captura_opcao(0, 2, "\n\n\033[1;94mQual é o seu perfil? \033[0m ")

    return perfil

def captura_opcao(min, max, mensagem):
    opcao = int(input(mensagem))
    while(opcao < int(min) or opcao > int(max)):
        print("Opção inválida! Por favor, digite novamente!")
        opcao = int(input(mensagem))
    return opcao

def iniciar_programa():
    print("\033[1;35mSeu ajudante de viagem está carregando...\033[0m ")
    time.sleep(1.5)

def exibe_menu_agencia_de_viagens():
    print("===================== MENU PARA AGÊNCIA DE VIAGENS ==============================")
    print("1 - Visualizar menor custo para ligar todos os aeroportos")
    print("2 - Consultar rotas com menor caminho e custo")
    print("0 - Voltar a seleção de perfil")
    opcao = captura_opcao(0, 2, "\n\nQual opção deseja realizar? ")

    return opcao

