# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Se importa la clase AFD
from automatas.AFD import *
from tools.components import *

# Clase principal donde se realiza el algoritmo de subconjuntos
class subconjuntos():
    def __init__(self, AFN, alphabet, expression, postfix):
        self.AFN = AFN
        self.AFNstates = AFN.states
        self.AFNtransitions = AFN.transitions
        self.alphabet = alphabet
        self.eps = 'ε'
        self.tempTransitions = []
        self.final_AFD_transitions = []
        self.InState = None
        self.FnStates = []
        self.expression = expression
        self.postfixExp = postfix
         
    # Se crea un alfabeto para nombrar estados posteriormente           
    def listAlphabet(self):
        a = list(map(chr, range(97, 123)))
        new = []
        for i in a:
            new.append(i.upper())
        new.reverse()
        return new
        
    # Algoritmo principal de subconjuntos
    def subconjuntos_construction(self): 
        
        # Se crean nombres para estados   
        ABC = self.listAlphabet()   
        self.names = {}
         
        # Se sigue el pseudocódigo proporcionado por el libro del dragón
        Dstates = []
        # Se inicia con el e-closure del estado inicial del AFN
        DstatesTemp = self.e_closure([self.AFN.initialState])
        Dstates.append(DstatesTemp)

        Dstates_marked = []
  
        # Se verifican los estados y se marcan hasta que acaben
        while(not all(t in Dstates_marked for t in Dstates)):
            for t in Dstates:
                Dstates_marked.append(t)

                for symbol in self.alphabet:
                    if(symbol == 'ε'):
                        continue
                    U = self.e_closure(self.move(t, symbol))
                    
                    if(U not in Dstates):
                        Dstates.append(U)

                    if(t != []):
                        if(U != []):
                            self.tempTransitions.append(Transition(t, symbol, U))                     
    
        # Se renombran los estados
        for newState in Dstates_marked:
            if(newState != []):
                name = ABC.pop()
                self.names[name] = newState

        # Se renombran las transiciones
        for trans in self.tempTransitions:
            newInState = None
            newFnState = None
            for key, value in self.names.items():
                if(value == trans.inState):
                    newInState = key
                if(value == trans.fnState):
                    newFnState = key
            self.final_AFD_transitions.append(Transition(newInState, trans.symbol, newFnState))
           
        # Se obtiene el estado inicial y el o los estados finales         
        for key, values in self.names.items():
            if self.AFN.initialState in values:
                self.InState = key
                
            if self.AFN.finalState in values:
                self.FnStates.append(key)
                
        return AFD(self.InState, self.FnStates, len(self.names), self.final_AFD_transitions, list(self.names.keys()))
     
    # Función move proporcionada por el libro del dragón                       
    def move(self, states, symbol):
        NewStates = []
        pila = []
        
        if (not isinstance(states, list)):
            pila.append(states)
        else:
            for i in states:
                pila.append(i)

        while(len(pila)>0):
            t = pila.pop()
            for trans in self.AFNtransitions:
                if(trans.inState == t and trans.symbol == symbol):
                    if(trans.fnState not in NewStates):
                        NewStates.append(trans.fnState)

        return NewStates

    # Función e-closure proporcionada por el libro del dragón 
    def e_closure(self, states):
        Result = []
        pila = []
        
        for i in states:
            pila.append(i)
            Result.append(i)

        while(len(pila) != 0):
            t = pila.pop()
            for trans in self.AFNtransitions:
                if(trans.inState == t and trans.symbol == self.eps):
                    if(trans.fnState not in Result):
                        Result.append(trans.fnState)
                        pila.append(trans.fnState)
                            
        return Result
    