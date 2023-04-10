# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from automatas.AFD import *

class Minimizador():
    def __init__(self, AFD, alphabet):
        self.AFD = AFD
        self.alphabet = alphabet
        
    def minimize_afd(self):
        groups = self.separate()
        groups = [sorted(sublista) for sublista in groups]
        groupsInOrder = sorted(groups, key=len)
        
        ABC = listAlphabet()
        names = {}
        
        # Se renombran los estados
        for newState in groupsInOrder:
            name = ABC.pop()
            names[name] = newState

        print(names)

        new_transitions = []
        newInState = None

        for trans in self.AFD.transitions:
            inState = None
            fnState = None
            for key, value in names.items():
                if trans.inState in value:
                    inState = key
                if trans.fnState in value:
                    fnState = key
                
            newT = Transition(inState, trans.symbol, fnState)
            if (newT not in new_transitions):
                new_transitions.append(newT)
              
        for key, value in names.items():
            if self.AFD.initialState in value:
                newInState = key
           
        newFnStates = [key for key, value in names.items() if any(elem in value for elem in self.AFD.finalStates)]     
                        
        return AFD(newInState, newFnStates, len(names), new_transitions, list(names.keys()))

    def separate(self):
        # Crear lista de conjuntos
        P = [self.AFD.finalStates]
        P.append(list(set(self.AFD.states) - set(self.AFD.finalStates)))
        G = P
             
        # Hasta no poder partir más los grupos se ejecuta el código
        veri = True
        while(veri):
            parts_dict = {}
            
            # Se evaluan las particiones y se encuentran aquellos grupos donde coincida
            # el símbolo y las transiciones
            for partition in G:
                for state in partition:
                    for symbol in self.alphabet:
                        parts_dict.update(self.build_parts_dict(G, state, symbol))

            # Se evalua si pertenecen a un mismo grupo y se crean las particiones
            states_partition = []
            new_parts = []  
            for partition in G:
                for state in partition:
                    value = parts_dict[state]    
                    value.append(G.index(partition))
                    
                    if(value not in states_partition):
                        states_partition.append(value)
                        new_parts.append([state]) 
                    else:
                        if(value in states_partition):
                            index = states_partition.index(value)
                            new_parts[index].append(state)
                            
            if(G == new_parts):
                veri = False
            else:
                G = new_parts      
                
        return G
    
    # Método para encontrar todos los estados que pertenecen a un grupo
    def build_parts_dict(self, G, state, symbol):
        parts_dict = {}
        for partitionB in G:
            if any(trans.fnState in partitionB for trans in self.AFD.transitions if trans.inState == state and trans.symbol == symbol):
                if state not in parts_dict:
                    parts_dict[state] = [[symbol, G.index(partitionB)]]
                else:
                    value = parts_dict[state]
                    value.append([symbol, G.index(partitionB)])
                    parts_dict[state] = value
            else:
                if state not in parts_dict:
                    parts_dict[state] = []
        return parts_dict