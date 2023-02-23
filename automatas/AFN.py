# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Clase Stack
from tools.stack import Stack
from tools.infixToPostfix import Conversion

class Estado():
    def __init__(self, stateNum):
        self.stateNum = stateNum
        
    def __str__(self):
        return f"q{self.stateNum}"
    
    def __repr__(self):
        return str(self)
        
class Transition():
    def __init__(self, inState, symbol, fnState):
        self.inState = inState
        self.symbol = symbol
        self.fnState = fnState
        
    def __str__(self):
        return f"{self.inState}-{self.symbol}-{self.fnState}"
    
    def __repr__(self):
        return str(self)
class AFN:
    def __init__(self, InState, FnState, numStates, transitions, states):
        self.epsilon = "ε"
        self.numStates = numStates
        
        self.states = states
        self.initialState = InState
        self.finalState = FnState
        self.transitions = transitions
    
    def __str__(self):
        return f"No. Estados: {self.numStates}\nEstados: {self.states}\nEstado inicial: {self.initialState}\nEstado final: {self.finalState}\nTransiciones: {self.transitions}"
        
class Construction(object):
    def __init__(self, expression):
        self.expression = expression
        self.epsilon = "ε"
        self.numStates = 0
        self.states = set()

        self.alphabet = []
        
        self.AFNS = []
        
        #Se obtiene la expresión en postfix
        self.Obj = Conversion(self.expression)
        self.postfixExp = self.Obj.infixToPostfix()
        self.alphabet = self.Obj.get_alphabet(expression)
       
    def fusionTransitions(self, transitions):
        result = []
        for element in transitions:
            if (isinstance(element, list)):
                result.extend(self.fusionTransitions(element))
            else:
                result.append(element)

        return result 
    
    def Thompson_Construction(self):
        
        print("Infix: ", self.expression)
        print("Postfix: ",self.postfixExp)
        
        for i in self.postfixExp:
            self.Thompson_Components(i)
            
        self.states = self.AFNS[0].states
        return self.AFNS[0]
        
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
    
    def concat(self, afnA, afnB):
        
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
          
        
        
        