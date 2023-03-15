# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from automatas.AFD import AFD, Transition
from tools.tree import *

class directConstruction():
    def __init__(self, infix, postfix, alphabet):
        self.infix = infix
        self.postfix = postfix
        self.alphabet = alphabet
        self.postfix += '#.'
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
        ABC = self.listAlphabet()
        
        for i in FinalTree:
            for j in i:
                if (type(j) != str and j != None and type(j) != int):
                    j = j.sort()
            
            if (i[0] == '#'):
                numberFState = i[4]

        # Se sigue el pseudocódigo proporcionado por el libro del dragón
        Dstates = []
        Dstates.append(inState)

        Dstates_marked = []
        while(not all(t in Dstates_marked for t in Dstates)):
            for t in Dstates:
                Dstates_marked.append(t)
                
                for symbol in self.alphabet:
                    U = []

                    # Buscamos en todo el árbol por las posiciones que tengan el símbolo
                    for x in t:
                        for el in FinalTree:
                            if x == el[4] and el[0] == symbol:
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

    # Se crea un alfabeto para nombrar estados posteriormente           
    def listAlphabet(self):
        a = list(map(chr, range(97, 123)))
        new = []
        for i in a:
            new.append(i.upper())
        new.reverse()
        return new
        

        
