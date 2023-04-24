# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

class dfaSimulation():
    def __init__(self, AFD, w=None):
        self.AFD = AFD
        self.w = w
        self.tokenList = []
        
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
                if(trans.inState == t and str(trans.symbol.label) == str(symbol)):
                    if(trans.fnState not in NewStates):
                        NewStates.append(trans.fnState)

        return NewStates
    
    def Simulation(self):
        ActualState = self.AFD.initialState
        for i in self.w:
            ActualState = self.move(ActualState, i)
            if (ActualState is None):
                return False

        for element in ActualState:
            if (element in self.AFD.finalStates):
                return "Si"
            else:
                return "No" 
            
        return "No"
    
    def SimulationTokens(self, text):
        print()
        ActualState = self.AFD.initialState
        temp = ""
        coins = []
        for i in range(len(text)):
            for j in range(len(text[i])):         
                temp += text[i][j]       
                ActualState = self.move(ActualState, text[i][j])
                if ActualState:
                    #print("\nSi", repr(temp), ActualState)
                    if (j+1 < len(text[i])):
                        NewActualState = self.move(ActualState, text[i][j+1])
                        if not NewActualState:
                            coins.append((temp, ActualState))
                            ActualState = self.AFD.initialState
                            temp = ""
                        else:
                            NewActualState = self.move(ActualState, text[i][j+1])
                            if not NewActualState:
                                temp = ""
                    else:
                        if (i+1 < len(text)):
                            for j in range(len(text[i+1])):
                                if (j+1 < len(text[i+1])):
                                    NewActualState = self.move(ActualState, text[i+1][j+1])
                                    if not NewActualState:
                                        coins.append((temp, ActualState))
                                        ActualState = self.AFD.initialState
                                        temp = ""
                                    else:
                                        NewActualState = self.move(NewActualState, text[i][j+1])
                                        if not NewActualState:
                                            temp = ""
                                    break
                else:
                    #print("No", repr(temp))
                    ActualState = self.AFD.initialState
                    if (j+1 < len(text[i])):
                        NewActualState = self.move(ActualState, text[i][j+1])
                        if NewActualState:
                            coins.append((temp, "Error"))
                            temp = ""
                            NewActualState = self.move(NewActualState, text[i][j+1])
                            if NewActualState:
                                ActualState = self.AFD.initialState
                   
        return coins           
                             
"""
def SimulationTokens(self, text):
        print()
        ActualState = self.AFD.initialState[0]
        coincidencias = []
        temp = ""
        for line in text:
            for i in range(len(line)): 
                next, notTrans = True, True
                char = line[i]
                print(repr(temp))
                while(next):
                    for trans in self.AFD.transitions:
                        if(trans.inState == ActualState and trans.symbol.label == char):
                            temp += line[i]
                            ActualState = trans.fnState
                            next, notTrans = False, False
                            break
                        
                    if notTrans:
                        if (ActualState == self.AFD.initialState[0]):
                            print("Error lexico", line[i])
                            temp = ""
                            next = False
                        else:
                            print("Token?", temp)
                            temp = ""
                            ActualState = self.AFD.initialState[0]
            if temp:
                if (ActualState == self.AFD.initialState[0]):
                    print("Error lexico", line[i])
                    temp = ""
                else:
                    print("Token?", temp)
                    temp = ""
                    ActualState = self.AFD.initialState[0]
                        
                
        print(coincidencias)
"""