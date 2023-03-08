# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

class nfaSimulation():
    def __init__(self, AFN, w):
        self.AFN = AFN
        self.w = w
    
    def intersection(self, lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

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
            for trans in self.AFN.transitions:
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
            for trans in self.AFN.transitions:
                if(trans.inState == t and trans.symbol == "ε"):
                    if(trans.fnState not in Result):
                        Result.append(trans.fnState)
                        pila.append(trans.fnState)
                            
        return Result
    
    def Simulation(self):
        AcceptState = [self.AFN.finalState]
        
        S = self.e_closure([self.AFN.initialState])
        cadena = []
        for i in self.w:
            cadena.append(i)
        cadena.reverse()
            
        while(len(cadena) > 0):
            c = cadena.pop()
            S = self.e_closure(self.move(S, c))

        # Si la cadena es aceptada se retornará "sí", de lo contrario "no"
        if (self.intersection(S, AcceptState) != []):
            return "Si"
        else:
            return "No"    
    