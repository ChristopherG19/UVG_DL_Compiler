# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from components import *
from tree import *

# Clase AFD: Representa los AFD's creados
class AFD():
    def __init__(self, InState, FnState, numStates, transitions, states):
        self.numStates = numStates
        
        self.states = states
        self.initialState = InState
        self.finalStates = FnState
        self.transitions = transitions
    
    def __str__(self):
        return f"No. Estados: {self.numStates}\nEstados: {self.states}\nEstado inicial: {self.initialState}\nEstado o estados finales: {self.finalStates}\nTransiciones: {self.transitions}"

# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

class directConstruction():
    def __init__(self, infix, postfix, alphabet):
        self.infix = infix
        self.postfix = postfix
        self.alphabet = alphabet
        self.letterSymbols = {}
        
        newSim = Simbolo('#') 
        newSim2 = Simbolo('.') 
        newSim2.setType(True)
        self.postfix.append(newSim)
        self.postfix.append(newSim2)
        
        ls = [l.label if not l.isSpecialChar else repr(l.label) for l in self.postfix]
        print("\nPostfix: ", "".join(ls))
        print()

    def buildDFA(self):
        T = Tree(self.postfix)
        self.Tree = T.generateTree()       
        self.Tree.calculate_positions()
        
        FinalTree = self.Tree.traverse_tree(self.Tree)
        
        # print(self.alphabet)
        # print(self.Tree)

        inState = sorted(FinalTree[0][1])
        InState = None
        FnStates = []
        trans = []
        numberFState = 1
        names = {}
        ABC = listAlphabet()
        
        for i in FinalTree:
            for j in i:
                if (type(j) != str and j != None and type(j) != int and type(j) == list):
                    j = j.sort()
            
            if (i[0] == '#'):
                numberFState = i[4]
                
            #Imprimir árbol
            # print(i)

        #print()
        # Se sigue el pseudocódigo proporcionado por el libro del dragón
        Dstates = []
        Dstates.append(inState)

        Dstates_marked = []
        while(not all(t in Dstates_marked for t in Dstates)):
            for t in Dstates:
                Dstates_marked.append(t)
                
                for symbol in self.alphabet:
                    if(symbol == 'ε'):
                        continue
                    U = []

                    # Buscamos en todo el árbol por las posiciones que tengan el símbolo
                    for x in t:
                        for el in FinalTree:
                            #print(el[0].label, symbol)
                            if x == el[4] and el[0].label == symbol:
                                for a in el[3]:
                                    if (a not in U):
                                        U.append(a)      
                                                             
                    if (len(U) > 0):
                        if (U not in Dstates):
                            Dstates.append(U)

                    if(t != []):
                        if(U != []):
                            trans.append(Transition(t, symbol, U))  
                
        # Se renombran los estados
        for newState in Dstates_marked:
            if(newState != []):
                name = ABC.pop()
                names[name] = newState

        final_Trans = []

        # Se renombran las transiciones
        for t in trans:     
            newInState = None
            newFnState = None
            for key, value in names.items():
                if(value == t.inState):
                    newInState = key
                if(value == t.fnState):
                    newFnState = key     
            final_Trans.append(Transition(newInState, t.symbol, newFnState))
        
        # Se obtiene el estado inicial y el o los estados finales         
        for key, values in names.items():
            if inState in values or inState == values:
                InState = key
            
            if numberFState in values:
                FnStates.append(key)
                
        print(names)
        return AFD(InState, FnStates, len(names), final_Trans, list(names.keys()))


# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

import graphviz

# Función para mostrar AFN's
def showGraphNFA(nfa, metodo):
    g = graphviz.Digraph(comment="AFN")

    g.attr(rankdir='LR')

    for estado in nfa.states:
        if estado == nfa.initialState and estado == nfa.finalState:
            g.edge('start', str(estado))
            
        if estado == nfa.initialState:
            g.edge('start', str(estado))
            g.node('start', shape='point')
        elif estado == nfa.finalState:
            g.node(str(estado), shape='doublecircle')
        else:
            g.node(str(estado), shape='circle')

    for transicion in nfa.transitions:
        origen, simbolo, destino = transicion.inState, transicion.symbol, transicion.fnState
        g.edge(str(origen), str(destino), label=str(simbolo))
        
    g.render(f'results/AFN_{metodo}',format='png')

# Función para mostrar AFD's
def showGraphDFA(dfa, metodo):
    g = graphviz.Digraph(comment="AFD")

    g.attr(rankdir='LR')

    for estado in dfa.states:
        if estado == dfa.initialState and estado in dfa.finalStates:
            g.node(str(estado), shape='doublecircle')
            
        if estado == dfa.initialState:
            g.edge('start', str(estado))
            g.node('start', shape='point')
        elif estado in dfa.finalStates:
            g.node(str(estado), shape='doublecircle')
        else:
            g.node(str(estado), shape='circle')

    for transicion in dfa.transitions:
        origen, simbolo, destino = transicion.inState, transicion.symbol, transicion.fnState
        g.edge(str(origen), str(destino), label=str(simbolo))
        
    g.render(f'results/AFD_{metodo}', format='png')    

        
