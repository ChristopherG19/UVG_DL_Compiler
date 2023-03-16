# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Se importan calses
from tools.stack import Stack
from tools.infixToPostfix import Conversion
from tools.components import *

# Clase AFN: Representa los AFN's creados
class AFN():
    def __init__(self, InState, FnState, numStates, transitions, states):
        self.epsilon = "ε"
        self.numStates = numStates
        
        self.states = states
        self.initialState = InState
        self.finalState = FnState
        self.transitions = transitions
    
    def __str__(self):
        return f"No. Estados: {self.numStates}\nEstados: {self.states}\nEstado inicial: {self.initialState}\nEstado final: {self.finalState}\nTransiciones: {self.transitions}"

# Clase Construction: Representa la construcción de Thompson    
class Construction(object):
    def __init__(self, expression, postfix, alphabet):
        self.expression = expression
        self.epsilon = "ε"
        self.numStates = 0
        self.states = set()

        self.alphabet = []
        
        self.AFNS = []
        
        self.postfixExp = postfix
        self.alphabet = alphabet
       
    # Método para tener un mismo formato en las transiciones
    def fusionTransitions(self, transitions):
        result = []
        for element in transitions:
            if (isinstance(element, list)):
                result.extend(self.fusionTransitions(element))
            else:
                result.append(element)

        return result 
    
    # Algoritmo principal que lee la expresión y construye el AFN que se retorna
    def Thompson_Construction(self):
        for i in self.postfixExp:
            self.Thompson_Components(i)
            
        self.AFNS[0].numStates = len(self.AFNS[0].states)
        return self.AFNS[0]
    
    # Algoritmo secundario que construye AFN's que componen al AFN final   
    def Thompson_Components(self, char):
        if (char in self.alphabet):
            self.AFNS.append(self.symbol(char))
            
        elif (char == '|'):
            afnA = self.AFNS.pop()
            afnB = self.AFNS.pop()
            self.AFNS.append(self.union(afnB, afnA))
        
        elif (char == '*'):
            afn = self.AFNS.pop()
            self.AFNS.append(self.kleene(afn))
    
        elif (char == '.'):
            afnA = self.AFNS.pop()
            afnB = self.AFNS.pop()
            self.AFNS.append(self.concat(afnB, afnA))

        elif (char == '+'):
            afn = self.AFNS.pop()
            self.AFNS.append(self.kleenePos(afn))
            
        elif (char == '?'):
            afn = self.AFNS.pop()
            self.AFNS.append(self.questionMark(afn))

    # Construcción de un AFN para los símbolos
    def symbol(self, symbol):
        
        self.numStates += 1
        InState = Estado(self.numStates)
        self.numStates += 1
        FnState = Estado(self.numStates)
        trans = []
        trans.append(Transition(InState, symbol, FnState))
        
        trans = self.fusionTransitions(trans)
        
        self.states.add(InState)
        self.states.add(FnState)
        
        return AFN(InState, FnState, self.numStates, trans, [InState, FnState])
      
    # Construcción de un AFN para las uniones  
    def union(self, afnA, afnB):
        self.numStates += 1
        InState = Estado(self.numStates)
        self.numStates += 1
        FnState = Estado(self.numStates)   
        trans = []
        trans.append(afnA.transitions)
        trans.append(afnB.transitions)
        trans.append(Transition(afnA.finalState, self.epsilon, FnState))
        trans.append(Transition(afnB.finalState, self.epsilon, FnState))
        trans.append(Transition(InState, self.epsilon, afnA.initialState))
        trans.append(Transition(InState, self.epsilon, afnB.initialState))
        
        trans = self.fusionTransitions(trans)
        
        states = afnA.states + afnB.states
        states.append(InState)
        states.append(FnState)
        
        for state in states:
            self.states.add(state)
         
        return AFN(InState, FnState, self.numStates, trans, states)
    
    # Construcción de un AFN para las cerraduras kleene
    def kleene(self, afn):
        self.numStates += 1
        InState = Estado(self.numStates)
        self.numStates += 1
        FnState = Estado(self.numStates)   
        trans = []
        trans.append(afn.transitions)
        
        trans.append(Transition(afn.finalState, self.epsilon, afn.initialState))   
        trans.append(Transition(InState, self.epsilon, afn.initialState))   
        trans.append(Transition(afn.finalState, self.epsilon, FnState))   
        trans.append(Transition(InState, self.epsilon, FnState))   
        
        trans = self.fusionTransitions(trans)
        
        states = afn.states
        states.append(InState)
        states.append(FnState)
        
        for state in states:
            self.states.add(state)

        return AFN(InState, FnState, self.numStates, trans, states)
    
    # Construcción de un AFN para las cerraduras positivas
    def kleenePos(self, afn):
        self.numStates += 1
        InState = Estado(self.numStates)
        self.numStates += 1
        FnState = Estado(self.numStates) 
        
        trans = []
        trans.append(afn.transitions)
        trans.append(Transition(afn.finalState, self.epsilon, afn.initialState))
        trans.append(Transition(InState, self.epsilon, afn.initialState))   
        trans.append(Transition(afn.finalState, self.epsilon, FnState))
           
        trans = self.fusionTransitions(trans)
        
        states = afn.states
        states.append(InState)
        states.append(FnState)
        
        for state in states:
            self.states.add(state)

        return AFN(InState, FnState, self.numStates, trans, states)
    
    # Construcción de un AFN para las cerraduras interrogación    
    def questionMark(self, afn):
        self.numStates += 1
        InState = Estado(self.numStates)
        self.numStates += 1
        FnState = Estado(self.numStates)   
        trans = []
        trans.append(afn.transitions)
        
        
        trans.append(Transition(InState, self.epsilon, afn.initialState))   
        trans.append(Transition(afn.finalState, self.epsilon, FnState))   
        trans.append(Transition(InState, self.epsilon, FnState))   
        
        trans = self.fusionTransitions(trans)
        
        states = afn.states
        states.append(InState)
        states.append(FnState)
        
        for state in states:
            self.states.add(state)
    
        states = afn.states
        
        return AFN(InState, FnState, self.numStates, trans, states)
    
    # Construcción de un AFN para las concatenaciones
    def concat(self, afnA, afnB):
        
        '''
            Se ajustan los estados para no tener que utilizar
            concatenaciones con epsilon
        '''
        for trans in afnB.transitions:
            if (trans.inState == afnB.initialState):
                trans.inState = afnA.finalState
            elif (trans.fnState == afnB.initialState):
                trans.fnState == afnA.finalState

        afnB.states.remove(afnB.initialState)
        states = afnA.states + afnB.states
        InState = afnA.initialState
        FnState = afnB.finalState            
        
        trans = []
        trans.append(afnA.transitions)
        trans.append(afnB.transitions)
        trans = self.fusionTransitions(trans)
        
        return AFN(InState, FnState, self.numStates, trans, states)
          
        
        
        