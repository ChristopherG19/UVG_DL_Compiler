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
        
        return 0
        
    def separate(self):
        # Crear lista de conjuntos
        groups = [self.AFD.finalStates]
        groups.append(list(set(self.AFD.states) - set(self.AFD.finalStates)))
        
        while True:
            newGroups = []
            for group in groups:
                if (len(group) == 1):
                    newGroups.append(group)
                    continue
                
                partition = self.divideGroup(group, groups)
                newGroups.extend(partition)
                
            if (newGroups == groups):
                break
            groups = newGroups
        return groups
        
    def divideGroup(self, group, groups):
        partition = []
        for symbol in self.alphabet:
            next_states = set([t.fnState for t in self.AFD.transitions if t.inState in group and t.symbol == symbol])
            for oldGroup in groups:
                if(next_states.issubset(set(oldGroup)) and oldGroup not in partition):
                    partition.append(oldGroup)
                    break
                
        return partition if partition else group
