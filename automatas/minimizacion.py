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
        
        if len(P[0]) == self.AFD.numStates:
            while True:
                result = []
                G_temp = []
                
                for Gi in G:
                    Gi.sort()
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
                            # Se obtienen los subgrupos
                            key = subgroup[0]
                            if key not in subgroups:
                                subgroups[key] = [(subgroup[1], subgroup[2])]
                            else:
                                subgroups[key].append((subgroup[1], subgroup[2]))

                    # Lista de estados con valores únicos
                    estados_unicos = []

                    # Recorremos cada estado
                    for estado in subgroups:
                        # Valor del estado actual
                        valor_actual = subgroups[estado]
                        
                        # Creamos una lista para agrupar los estados con valores idénticos
                        grupo = [estado]
                        
                        # Recorremos los demás estados para comparar su valor con el valor actual
                        for otro_estado in subgroups:
                            if estado != otro_estado and subgroups[otro_estado] == valor_actual:
                                grupo.append(otro_estado)
                        
                        grupo.sort()
                        # Si encontramos estados con el mismo valor, los agregamos al grupo
                        # de lo contrario, los agregamos como un estado único
                        if len(grupo) >= 1 and grupo not in estados_unicos:
                            estados_unicos.append(grupo)
                            
                    result.extend(estados_unicos)

                if (G == result):
                    break
                    
                G = result  

            return G
                
        else:    
            # Crear lista de conjuntos
            P = [self.AFD.finalStates]
            P.append(list(set(self.AFD.states) - set(self.AFD.finalStates)))
            G = P    
            while True:
                result = []
                G_temp = []
                
                for Gi in G:
                    Gi.sort()
                    if(Gi == []):
                        continue
                    
                    if (len(Gi) == 1):
                        if(Gi not in result):
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
                            # Se obtienen los subgrupos
                            key = subgroup[2]    
                            if key not in subgroups:
                                subgroups[key] = [subgroup[0]]
                            else:
                                subgroups[key].append(subgroup[0])
       
                    not_same_group = []
                    for key in subgroups.keys():
                        if key[0] not in Gi:
                            if([key[0]] not in result):
                                not_same_group += subgroups[key]

                    if len(not_same_group) != 0:
                        result.append(not_same_group)
                        for key, value in subgroups.items():
                            if value not in result:
                                result.append(value)
                            
                    elif len(not_same_group) == 0:
                        subgroups = {}

                        for group in G_temp:
                            for subgroup in group:
                                # Se obtienen los subgrupos
                                key = subgroup[0]
                                if key not in subgroups:
                                    subgroups[key] = [(subgroup[1], subgroup[2])]
                                else:
                                    subgroups[key].append((subgroup[1], subgroup[2]))
                        # Lista de estados con valores únicos
                        estados_unicos = []

                        # Recorremos cada estado
                        for estado in subgroups:
                            # Valor del estado actual
                            valor_actual = subgroups[estado]
                            
                            # Creamos una lista para agrupar los estados con valores idénticos
                            grupo = [estado]
                            
                            # Recorremos los demás estados para comparar su valor con el valor actual
                            for otro_estado in subgroups:
                                if estado != otro_estado and subgroups[otro_estado] == valor_actual:
                                    grupo.append(otro_estado)
                            
                            grupo.sort()
                            # Si encontramos estados con el mismo valor, los agregamos al grupo
                            # de lo contrario, los agregamos como un estado único
                            if len(grupo) >= 1 and grupo not in estados_unicos:
                                estados_unicos.append(grupo)
                                        
                        result.extend(estados_unicos)
                                
                        result = sorted(result, key=lambda x: x[0])
                    else:
                        if (list(set(Gi)-set(not_same_group)) not in result):
                            result.append(list(set(Gi)-set(not_same_group)))

                if (G == result):
                    break
                    
                G = result  

            return G     
