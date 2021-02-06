

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
    teste = []
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
    return estados, transicoes, teste, teste10

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
estados, transicoes, teste1, teste2 = translate(estados, simbolos, estados_iniciais, estados_finais, transicoes)
#print(estados)
#print(transicoes)
#print(new_transitions)

print(teste1)
print(teste2)