# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

class dfaSimulation():
    def __init__(self, AFD, w):
        self.AFD = AFD
        self.w = w
        
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
            for trans in self.AFD.transitions:
                if(trans.inState == t and trans.symbol == symbol):
                    if(trans.fnState not in NewStates):
                        NewStates.append(trans.fnState)

        return NewStates
    
    def Simulation(self):
        ActualState = self.AFD.initialState
        for i in self.w:
            ActualState = self.move(ActualState, i)
            if (ActualState is None):
                return False

        if (ActualState[0] in self.AFD.finalStates):
            return "Si"
        else:
            return "No" 