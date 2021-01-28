

def printAlgorithm():
    print("********************************************************************************************************")
    print("           ********  -----  Translate Finite Automata to Regular Expression  -----  ********\n")
    print("1 - Crie um AFNλ a partir do AF em questão. Para isso, adicione um novo estado inicial 'i'(com transição")
    print("     λ para o antigo estado inicial) a ele e um novo estado final 'f' (com uma transição λ vindo do ")
    print("     antigo estado final para o novo). \n")

    print("2 - Transforme o AFNλ em um Diagrama ER, isto é, troque a transições sobre múltiplos símbolos por uma ")
    print("     uma única transição da forma a1 + a2 + ... + an. \n")

    print("3 - Elimine todos os estados até que sobre apenas os estados 'i' e 'f'. ")
    print("     Para fazer isso, para cada par de estados <e1, e2> onde existe transição de 'e1' para 'e' e de ")
    print("     'e' para 'e2', crie uma transição de 'e1' para 'e2' da seguinte maneira. ")
    print("   A - Se 'e1' != 'e2' então a nova transição de 'e1' para 'e2' será da forma: r1 r2* r3.")
    print("   B - Se 'e1' == 'e2' então a noova transição de 'e1' para 'e2' será da forma: r1 r2* r3. ")
    print("       (Note que aqui teremos um loop, dado que 'e1' = 'e2')")
    print("   C - Se existia uma transição anteriormente de 'e1' para 'e2', a nova transição será da forma: ")
    print("      r0 + r1 r2* r3, onde r0 representa a transição que já existia.\n")
    print("********************************************************************************************************")
    return None

def readFiles():
    with open("t1.txt") as f:
        content = f.read().splitlines()
    
    return content

def start(input: list):
    states = list(input[0].split(','))
    symbols = list(input[1].split(','))
    initial_states = list(input[2].split(','))
    final_states = list(input[3].split(','))
    transitions = []
    for i in range(4, len(input)):
        transitions.append(input[i])

    return states, symbols, initial_states, final_states, transitions

def translate(estados: list, simbolos: list, estados_iniciais: list, estados_finais: list, transicoes: list):
    '''
        Input: Automato finito (estados, simbolos, estados_iniciais, estados_finais, transicoes)
        Output: Expressão Regular equivalente

    '''
    #Adicionando os novos estados iniciais e finais
    estados += ["<i>","<f>"]
    #Adicionando transições entre os novos e antigos estados finais e iniciais
    for estado in estados_iniciais:
        transicoes.append(f"(<i>,<λ>,{estado})")

    for estado in estados_finais:
        transicoes.append(f"({estado},<λ>,<f>)")

    ##Verificando transições sobre múltiplos símbolos

    ##A ideia é ir verificando os pares "estado, símbolo" e sempre que este par se repetir
    ##eu guardo o estado. Depois disso, eu removo todas as transições que possuem esse par
    ##E adiciono um transição no formato especificado

    #O(N^2)
    transicoes.append("(<i1>,<λ>,<g>)")
    transicoes.append("(<i2>,<λ>,<r>)")
    transicoes.append("(<i2>,<λ>,<s>)")
    transicoes.append("(<i2>,<λ>,<t>)")

    estados.append('<i1>')
    estados.append('<i2>')

    dicionario = dict.fromkeys(estados, "")
    aux = []
    transicoes_copy = list(map(lambda x: x.replace("(", "").replace(")", ""),transicoes))
    for i in range(len(transicoes)):
        aux1 = [transicoes_copy[i].split(",")[0], transicoes_copy[i].split(",")[1]]
        
        for j in range(i+1, len(transicoes)):
            aux2 = [transicoes_copy[j].split(",")[0], transicoes_copy[j].split(",")[1]]
            #print(transicoes[i], transicoes[j])
            if aux1 == aux2: aux.append([transicoes_copy[i].split(",")[2], transicoes_copy[i].split(",")[0] , transicoes_copy[j].split(",")[2]]); print(transicoes[i], transicoes[j]) #Salvando o estado

    ##Agrupando os pares comuns
    labels = ""
    for x in aux:
        dicionario[x[1]] += x[0] + " "
        dicionario[x[1]] += x[2] + " "
        labels += dicionario[x[1]]

    labels =  list(set(labels.split()))

    ##Pegando os valors únicos 
    for key, value in dicionario.items():
        dicionario[key] = list(set(value.split()))
        print(dicionario[key])

    ##Deletando os estados que transitam sobre múltiplos símbolos
    print(transicoes)
    print("\n\n\n\n")
    for i in range(len(transicoes)):
        #print(transicoes_copy[i].split(",")[0])
        if transicoes_copy[i].split(",")[0] in labels or transicoes_copy[i].split(",")[1] in labels:
            del transicoes[i]
    return transicoes_copy, labels

entrada = readFiles()
estados, simbolos, estados_iniciais, estados_finais, transicoes = start(entrada)
print(estados)
print(simbolos)
print(estados_iniciais)
print(estados_finais)
print(transicoes)

printAlgorithm()
print(estados)

############### Teste
transicoes, labels = translate(estados, simbolos, estados_iniciais, estados_finais, transicoes)
print(transicoes[-1].split(",")[0])
print(transicoes[-1][0].split(",")[0] in labels)
print(labels)

