

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

    ##Tenho que trocar os antigos estados finasis e os iniciais

    ##Verificando transições sobre múltiplos símbolos

    ##A ideia é verificar cada transição, as que possuirem comprimento maior do que 3 tem múltiplas transições, para estes casos chamo
    ##uma função que faz a conversão para o formato adequado (formato de diagrama ER).
    

    ##Caso que temos múltiplas transicoes incluindo o próprio elemento (Depois desse passo, todos tem tamanho 3)
    #new_transitions = []
    #for transition in transicoes:
    #    if len(transition) > 3:
    #        new_transitions.append([transition[0], transition[1], erFormat(transition)])
    #        transicoes.remove(transition)

    #for x in new_transitions:
    #    transicoes.append(x)

    ##Caso de multiplas transicoes
    '''teste = []
    for transicao in transicoes:
        simbolos = ""
        for i in transicoes:
            if transicao != i and transicao[0] == i[0] and transicao[2] == i[2]:
                #print(transicao)
                #print(i)
                teste.append(transicao)
                
    
    teste10 = []
    for x in range(0, len(teste), 2):
        #teste10.append(x)
        print(f"[{teste[x][0], teste[x][1], teste[x+1][1], teste[x+1][2]}]")
    return estados, transicoes, teste, teste10'''
    multiplas = []
    resultados = []
    ##Ainda tenho que testar se estar cobrindo corretamente os casos em que há mais de duas transicões.
    for i in range(len(transicoes)):
        for j in range(i+1, len(transicoes)):
            if transicoes[i][0] == transicoes[j][0]:
                chegada = transicoes[j][1:]
                if transicoes[i][2] in list(chegada): 

                     
                    removeSecond(transicoes[j], transicoes[i][0])
                    nova_transicao = [transicoes[i][0], f"({transicoes[i][1]}+{transicoes[j][1]})", transicoes[i][2]]
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
    return transicoes

    ##Eu tive uma ideia para identificar as multiplas transicoes, mas ainda estou na dúvida quanto a um caso específico.
    ## x,0,x
    ## x,1,x,x1
    ##https://pt.wikipedia.org/wiki/Aut%C3%B4mato_finito_determin%C3%ADstico

def stateHasLoop(estado :str, transitions: list):
    for x in transitions:
        if x[0] == x[2] and x[0] == estado: return x[1]
    return ""
def elimina_estado(estado :str, transitions :list):
    esquerda = []
    dirteita = []
    meio = [estado]

    for x in transitions:
        if x[0] == estado and x[0] != x[2]: direita = x
        if x[2] == estado and x[2] != x[0]: esquerda = x
        
    flag = stateHasLoop(estado, transitions)
    if flag != "": nova_transicao = [esquerda[0], f"{esquerda[1]}{flag}*{direita[1]}", direita[2]]
    else: nova_transicao = [esquerda[0], f"{esquerda[1]}{direita[1]}", direita[2]]
    
    aux = []
    ##removendo estado e transicoes
    for i in range(len(transitions)):
        if transitions[i][0] == estado or transitions[i][2] == estado and transitions[i][0] != transitions[i][2]: 
            #del transitions[i]
            aux.append(transitions[i])

    
    for x in aux:
        transitions.remove(x)
    transitions.append(nova_transicao)

    return transitions



def elimination(transitions :list):
    estados_pr_eliminar = []
    for element in transitions:
        if element[1] != 'λ':
            estados_pr_eliminar.append(element[0])
            estados_pr_eliminar.append(element[2])
    estados_pr_eliminar = list(set(estados_pr_eliminar))


    '''removidos = []    
    for i in range(len(estados_pr_eliminar)):
        for j in range(i+1, len(estados_pr_eliminar)):
            if estados_pr_eliminar[i][2] == estados_pr_eliminar[j][0] and estados_pr_eliminar[i][0] not in removidos:
                transitions.append([f'{estados_pr_eliminar[i][0]},{estados_pr_eliminar[i][1]}*{estados_pr_eliminar[j][1]}, {estados_pr_eliminar[j][2]}'])
                removidos.append(estados_pr_eliminar[j][0])
                #transitions.remove(estados_pr_eliminar[j])
'''
    #for estado in estados_pr_eliminar:
     #   elimina_estado(estado, transitions)
    #elimina_estado(estados_pr_eliminar[0], transitions)

    

                
    
    
    return sorted(estados_pr_eliminar)

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
teste = translate(estados, simbolos, estados_iniciais, estados_finais, transicoes)
teste2 = elimination(teste)


##Parece que esta removendo os estados, pelo menos um a um.

##O próximo passo é ver se eu consigo chegar até o caso base.
##Quando tem loop tem que colocar estrela.
##Trocar símbolo da concatenação(para sem símbolo), colocar ab ao invés de a*b 
teste10 = elimina_estado('x', teste)
#print(teste)
#print(teste10)

print(teste10)
teste10 = elimina_estado('x1', teste10)
print(teste10)
teste10 = elimina_estado('x1a', teste10)
print(teste10)
teste10 = elimina_estado('x1ab', teste10)
print(teste10) 
