# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from automatas.AFD import *
from tools.tree import *
from tools.components import *


class directConstruction():
    def __init__(self, infix, postfix, alphabet):
        self.infix = infix
        self.postfix = postfix
        self.alphabet = alphabet
        newSim = Simbolo('#') 
        newSim2 = Simbolo('.') 
        newSim2.setType(True)
        self.postfix.append(newSim)
        self.postfix.append(newSim2)
        self.letterSymbols = {}

    def buildDFA(self):
        T = Tree(self.postfix)
        self.Tree = T.generateTree()        
        self.Tree.calculate_positions()
        
        FinalTree = self.Tree.traverse_tree(self.Tree)

        inState = sorted(FinalTree[0][1])
        InState = None
        FnStates = []
        trans = []
        numberFState = 1
        names = {}
        ABC = listAlphabet()
        
        for i in FinalTree:
            for j in i:
                if (type(j) == list):
                    j = j.sort()
            
            if (i[0].label == '#'):
                numberFState = i[4]
                
            #Imprimir árbol
            # print(i)

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

        

        
