

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
        transitions.append(input[i].split(','))

    return states, symbols, initial_states, final_states, transitions

def erFormat(transition: list):
    aux = ""
    for x in transition[2:]:
        aux += (f"{x}+")
    return aux[:-1]

def refazTransicoes(transitions: list, flag: list):
    for x in transitions:
        for estado in flag:
            if x[0] == estado: transitions.remove(x); print(x)

def removeSecond(lista :list, element :str):
    i = 0
    j = 0
    for x in lista:
        if x == element: i = i + 1
        if i == 2:
            del lista[j]
        j = j + 1

def translate(estados: list, simbolos: list, estados_iniciais: list, estados_finais: list, transicoes: list):
    '''
        Input: Automato finito (estados, simbolos, estados_iniciais, estados_finais, transicoes)
        Output: Expressão Regular equivalente

    '''
    #Adicionando os novos estados iniciais e finais
    estados += ["i","f"]

    #Adicionando transições entre os novos e antigos estados finais e iniciais
    
    for estado in estados_iniciais:
        transicoes += [f"i,λ,{estado}".split(',')]
        
    for estado in estados_finais:
        transicoes += [f"{estado},λ,f".split(',')]

    #Atualizando os estados iniciais e finais
    estados_iniciais = []; estados_iniciais.append("i")
    estados_finais = []; estados_finais.append("f")
    
    ##Lógica para remover transições múltiplas
    multiplas = []
    resultados = []
    ##Ainda tenho que testar se estar cobrindo corretamente os casos em que há mais de duas transicões.
    for i in range(len(transicoes)):
        for j in range(i+1, len(transicoes)):
            if transicoes[i][0] == transicoes[j][0]:
                chegada = transicoes[j][1:]
                if transicoes[i][2] in list(chegada): 

                     
                    removeSecond(transicoes[j], transicoes[i][0])
                    nova_transicao = [transicoes[i][0],f"({transicoes[i][1]}+{transicoes[j][1]})",transicoes[i][2]]
                    #multiplas.append(transicoes[i])
                    multiplas.append(transicoes[j])
                    resultados.append(nova_transicao)
    
    
    
    aux = []
    [aux.append(x[2]) for x in resultados + multiplas]
    aux = list(set(aux))

    for element in transicoes:
        if element[2] in aux and element[0] != 'i' and element[0] != 'f': transicoes.remove(element)

    aux2 = []
    for element in multiplas:
        if element[2] not in [x[2] for x in resultados]: aux2.append(element)
    
    for x in aux2:
        multiplas.remove(x)

    for x in multiplas:
        transicoes.remove(x)

    
    for element in resultados:
        transicoes.append(element)
    return transicoes, estados_iniciais, estados_finais



def stateHasLoop(estado :str, transitions: list):
    for x in transitions:
        if x[0] == x[2] and x[0] == estado: return x[1]
    return ""

def transitionBefore(estado1 :str, estado2: str, transitions :list):
    for element in transitions:
        if (element[0] == estado1 and element[2] == estado2) or (element[0] == estado2 and element[2] == estado1): 
            return element
    
    return ""

def elimina_estado(estado :str, transitions :list):
    esquerda = []
    direita = []
    meio = [estado]
    print(f"Eliminando estado: {estado}")

    for x in transitions:
        if x[0] == estado and x[0] != x[2]: direita.append(x)
        if x[2] == estado and x[2] != x[0]: esquerda.append(x)

##Consegui separar as transições de interesse nas listas "direita" e "esquerda", eu só tenho que verificar se elas tem loop e fazer de forma parecida que eu fiz anteriormente, agora levando
#em conta que tenho uma lista de transições e não apenas uma

    ##Tenho que verificar se já havia transições entre o par de estados
    flag = stateHasLoop(estado, transitions)
    nova_transicao = []
    for element1 in esquerda:
        for element2 in direita:
            if flag != "":
                if transitionBefore(element1[0], element2[2], transitions) != "":
                    transicao_antiga = transitionBefore(element1[0], element2[2], transitions)
                    nova_transicao.append([element1[0], f"({transicao_antiga[1]}+{element1[1]}{flag}*{element2[1]})", element2[2]])
                    transitions.remove(transicao_antiga)
                ##Como a flag retorna "" quando não tem loop, eu não preciso do if-else
                else:
                    nova_transicao.append([element1[0], f"{element1[1]}({flag})*{element2[1]}", element2[2]])

            else: 
                if transitionBefore(element1[0], element2[2], transitions) != "":
                    transicao_antiga = transitionBefore(element1[0], element2[2], transitions)
                    nova_transicao.append([element1[0],f"({transicao_antiga[1]}+{element1[1]}{element2[1]})",element2[2]])
                    transitions.remove(transicao_antiga)
                else:
                    nova_transicao.append([element1[0],f"{element1[1]}{element2[1]}",element2[2]])

    aux = []
    ##removendo estado e transicoes
    for i in range(len(transitions)):
        if transitions[i][0] == estado or transitions[i][2] == estado and transitions[i][0] != transitions[i][2]: 
            aux.append(transitions[i])
    
    
    for x in aux:
        transitions.remove(x)
    ##Adicionando as novas transições
    for element in nova_transicao:
        transitions.append(element)

    print(f"Transições após a remoção do estado {estado}:")
    #print(esquerda)
    #print(direita)
    print(transicoes); print("\n")
    #print(nova_transicao)
    return transicoes

##Minha ordem de eliminação

##Tenho que explicar na documentação porque escolhi essa ordem específica.
def myOrder(estados_pr_eliminar :list, transitions: list):
    direita = []
    esquerda = []
    new_list = []
    
    for estado in estados_pr_eliminar:
        i = 0
        for x in transitions:
            if x[0] == estado and x[0] != x[2]: direita.append(x); i = i + 1
            if x[2] == estado and x[2] != x[0]: esquerda.append(x); i = i + 1
            
        new_list.append([estado, i])

    ##Criei uma lista de tuplas com os estados e quantidade de transições possíveis
    new_list.sort(key=lambda x:x[1])
    return new_list

def elimination(transitions :list):
    estados_pr_eliminar = []
    for element in transitions:
        if element[1] != 'λ':
            estados_pr_eliminar.append(element[0])
            estados_pr_eliminar.append(element[2])
    estados_pr_eliminar = list(set(estados_pr_eliminar))
        
    for element in myOrder(estados_pr_eliminar, transicoes):
        elimina_estado(element[0], transitions)
    print("A expressão regular obtida através do autômato finito é:")
    print(transitions[0][1])
    return estados_pr_eliminar

entrada = readFiles()
estados, simbolos, estados_iniciais, estados_finais, transicoes = start(entrada)
#print(estados)
#print(simbolos)
#print(estados_iniciais)
#print(estados_finais)
print(transicoes)
#print(transicoes[0][1])
printAlgorithm()


############### Teste
teste, estados_iniciais, estados_finais = translate(estados, simbolos, estados_iniciais, estados_finais, transicoes)
#teste2 = elimination(teste)
#print(teste)
#print(estados)
#print(simbolos)
#print(estados_iniciais)
#print(estados_finais)
##Parece que esta removendo os estados, pelo menos um a um.

##O próximo passo é ver se eu consigo chegar até o caso base.
##Trocar símbolo da concatenação(para sem símbolo), colocar ab ao invés de a*b 
teste10= elimination(teste)
print(teste10)
#print(esquerda)
#print(direita)


'''teste10 = elimina_estado('i0', teste)
print(teste10)

teste10 = elimina_estado('p1', teste)
print(teste10)

teste10 = elimina_estado('p0', teste)
print(teste10)

teste10 = elimina_estado('i1', teste)
print(teste10
'''
'''print(teste10)
teste10 = elimina_estado('x1', teste10)
print(teste10)
teste10 = elimina_estado('x1a', teste10)
print(teste10)
teste10 = elimina_estado('x1ab', teste10)
print(teste10)

'''