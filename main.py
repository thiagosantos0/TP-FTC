


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

##Cria as estruturas para estados, simbolos, estados iniciais, estados finais, transicoes
def start(input: list):
    estados = list(input[0].split(','))
    simbolos = list(input[1].split(','))
    estados_iniciais = list(input[2].split(','))
    estados_finais = list(input[3].split(','))
    transicoes = []
    for i in range(4, len(input)):
        transicoes.append(input[i].split(','))

    return estados, simbolos, estados_iniciais, estados_finais, transicoes

#Transforma uma transição para o formato do diagram ER
def erFormat(transition: list):
    new_transitions = []
    for x in transition[2:]:
        new_transitions.append([transition[0], transition[1], x])
    return new_transitions

##Realiza o passo dois do algoritmo, trocar as transições múltiplas por uniões.

def translate(estados: list, simbolos: list, estados_iniciais: list, estados_finais: list, transicoes: list):
    '''
        Input: Automato finito (estados, simbolos, estados_iniciais, estados_finais, transicoes)
        Output: Lista de transições no formato final
    '''
    #Adicionando os novos estados iniciais e finais à estrutura de estados
    estados += ["i","f"]


    ##Passando transicoes para tamanho 3
    for x in transicoes:
        if len(x[2:]) >= 2:
            transicoes.remove(x)
            for y in erFormat(x):
                transicoes.append(y)
           
    #Adicionando transições entre os novos e antigos estados finais e iniciais
    for estado in estados_iniciais:
        transicoes += [f"i,λ,{estado}".split(',')]
        
    for estado in estados_finais:
        transicoes += [f"{estado},λ,f".split(',')]

    #Atualizando os estados iniciais e finais
    estados_iniciais = []; estados_iniciais.append("i")
    estados_finais = []; estados_finais.append("f")
    
    ##Lógica para remover transições múltiplas

    transicoes_copy = transicoes.copy()

    for i in range(0, len(transicoes)-2):
        for j in range(i+1, len(transicoes)-1):
            if transicoes[i][0] == transicoes[j][0]:
                chegada = transicoes[j][2]
                if transicoes[i][2] == chegada:
                    nova_transicao = [transicoes[i][0],f"({transicoes[i][1]}+{transicoes[j][1]})",transicoes[i][2]]

                    transicoes_copy.append(nova_transicao)
                    transicoes_copy.remove(transicoes[j])
                    transicoes_copy.remove(transicoes[i])

    
    transicoes = transicoes_copy
    return estados, simbolos, estados_iniciais, estados_finais, transicoes

##Verifica se o estado em questão tem loop
def stateHasLoop(estado :str, transitions: list):
    for x in transitions:
        if x[0] == x[2] and x[0] == estado: return x[1]
    return ""

##Verifica se havia transição anteriormente entre "estado1" e "estado2" 
def transitionBefore(estado1 :str, estado2: str, transitions :list):
    for element in transitions:
        if (element[0] == estado1 and element[2] == estado2): 
            return element
    
    return ""

#Elimina o estado "estado"
def elimina_estado(estado :str, transitions :list):
    esquerda = []
    direita = []
    #print(f"Eliminando estado: {estado}")

    for x in transitions:
        if x[0] == estado and x[0] != x[2]: direita.append(x)
        if x[2] == estado and x[2] != x[0]: esquerda.append(x)

    ##A flag sinaliza o loop e também guarda ele
    flag = stateHasLoop(estado, transitions)
    nova_transicao = []
    for element1 in esquerda:
        for element2 in direita:
            if flag != "":
                if transitionBefore(element1[0], element2[2], transitions) != "":
                    transicao_antiga = transitionBefore(element1[0], element2[2], transitions)
                    nova_transicao.append([element1[0], f"({transicao_antiga[1]}+{element1[1]}{flag}*{element2[1]})", element2[2]])
                    transitions.remove(transicao_antiga)
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

    return transicoes

##Minha ordem de eliminação
##Tenho que explicar na documentação porque escolhi essa ordem específica.

def myOrder(estados_pr_eliminar :list, transitions: list):
    direita = []
    esquerda = []
    new_list = []
    #print("Estados para eliminar: ", estados_pr_eliminar)
    for estado in estados_pr_eliminar:
        i = 0
        for x in transitions:
            if x[0] == estado and x[0] != x[2]: direita.append(x); i = i + 1
            if x[2] == estado and x[2] != x[0]: esquerda.append(x); i = i + 1
            
        new_list.append([estado, i])
    ##Criei uma lista de tuplas com os estados e quantidade de transições possíveis e ordenei de forma
    ##crescente pelo número de "transições eliminativas"(onde o estado em questão é o central) que passam por ele.
    new_list.sort(key=lambda x:x[1])
    return new_list

##Realiza a eliminação de todos os estados até que sobre apenas 'i' e 'f'
#Exibe a expressão regular equivalente
#Retorna uma lista de tuplas mostrando a ordem dos estados que foram eliminados. (Eliminaação feita da esquerda para a direita)
def elimination(transitions :list):
    estados_pr_eliminar = []
    retorno = []
    for element in transitions:
        if element[1] != 'λ':
            estados_pr_eliminar.append(element[0])
            estados_pr_eliminar.append(element[2])
    estados_pr_eliminar = list(set(estados_pr_eliminar))
        
    for element in myOrder(estados_pr_eliminar, transicoes):
        elimina_estado(element[0], transitions)
        retorno.append(element)
    print(transitions[0][1])
    return retorno

def getOrder(transition :list):
    return elimination(transition)

##Main
entrada = readFiles()
estados, simbolos, estados_iniciais, estados_finais, transicoes = start(entrada)
estados, simbolos, estados_iniciais, estados_finais, transicoes = translate(estados, simbolos, estados_iniciais, estados_finais, transicoes)



############### Testes
#teste2 = elimination(teste)
#print(teste)
#print(estados)
#print(simbolos)
#print(estados_iniciais)
#print(estados_finais)
##Parece que esta removendo os estados, pelo menos um a um.

##O próximo passo é ver se eu consigo chegar até o caso base.
##Trocar símbolo da concatenação(para sem símbolo), colocar ab ao invés de a*b 
teste10 = elimination(transicoes)
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