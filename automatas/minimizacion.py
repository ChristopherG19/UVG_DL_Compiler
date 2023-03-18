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
        print(groups)
        #new_trans = self.createNewTrans(groups)
        #new_afd = self.buildAFD(new_trans)
        
        return "\n"

    def separate(self):
        # Crear lista de conjuntos
        P = [self.AFD.finalStates]
        P.append(list(set(self.AFD.states) - set(self.AFD.finalStates)))

        G = P

        while True:
            result = []
            G_temp = []
            
            for Gi in G:
                if(Gi == []):
                    continue
                
                if (len(Gi) == 1):
                    result.append(Gi)
                    continue
                
                for symbol in self.alphabet:
                    #next_states = set([t.fnState for t in self.AFD.transitions if t.inState in Gi and t.symbol == symbol])

                    next_states = []
                    for t in self.AFD.transitions:
                        if t.inState in Gi and t.symbol == symbol:
                            next_states.append([t.inState, symbol, t.fnState])

                    if next_states not in G_temp:
                        G_temp.append(next_states)
                        
                subgroups = {}
                for group in G_temp:
                    for subgroup in group:
                        key = subgroup[2]
                        if key not in subgroups:
                            subgroups[key] = [subgroup[0]]
                        else:
                            subgroups[key].append(subgroup[0])

                not_same_group = []
                for key in subgroups.keys():
                    if key[0] not in Gi:
                        not_same_group += subgroups[key]
                
                if len(not_same_group) != 0:
                    result.append(not_same_group)
                    for key, value in subgroups.items():
                        if value not in result:
                            result.append(value)
                else:
                    if (list(set(Gi)-set(not_same_group)) not in result):
                        result.append(list(set(Gi)-set(not_same_group)))
        
            if (G == result):
                break
                  
            G = result  

        return G     
