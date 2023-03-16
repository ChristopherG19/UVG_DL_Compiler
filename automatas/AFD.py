# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from tools.components import *

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