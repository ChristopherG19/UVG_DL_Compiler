# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Clase Estado: Representa cada estado del autómata
class Estado():
    def __init__(self, stateNum):
        self.stateNum = stateNum
        
    def __str__(self):
        return f"q{self.stateNum}"
    
    def __repr__(self):
        return str(self)

# Clase Transición: Representa las transiciones del autómata
class Transition():
    def __init__(self, inState, symbol, fnState):
        self.inState = inState
        self.symbol = symbol
        self.fnState = fnState
        
    def __str__(self):
        return f"{self.inState}-{self.symbol}-{self.fnState}"
    
    def __repr__(self):
        return str(self)

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