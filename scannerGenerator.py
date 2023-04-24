# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

import pickle
from simulation.dfaSimulation import *
from tools.components import get_tokens_States, get_final_States, get_final_States_tokens

class ScannerGen():
    def __init__(self, nameFile, inputText):
        with open(nameFile, 'rb') as f:
            self.dfaD = pickle.load(f)
            self.dfaVerify = pickle.load(f)
        f.close()

        self.finalStates = get_final_States(self.dfaD.finalStates, self.dfaD.transitions)
        self.dicTokens = get_tokens_States(self.dfaVerify.finalStates, self.dfaVerify.transitions)
        self.dicTokensV2 = get_final_States_tokens(self.dfaVerify.finalStates, self.dfaVerify.transitions)
        
        with open(inputText) as f:
            self.text = f.readlines()
            
        print("\nFinal_States: ", self.finalStates)
        print("\nDic Tokens", self.dicTokens)
        print("\nDic Tokens V2", self.dicTokensV2)
    
        print()
        equivalent_states = {}
        for key, value in self.finalStates.items():
            for key2, value2 in self.dicTokensV2.items():
                if value == value2:
                    equivalent_states[key2] = [key]
                else:
                    ts = True
                    for val in value2:
                        if val not in value: 
                            ts = False
                        
                    if ts:
                        equivalent_states[key2] = [key]
                    
        print(equivalent_states)
        print()
                    
        prueba = 'C'
        simbolo = '*)'
        for key, value in equivalent_states.items():
            if prueba in value:
                if simbolo == self.dicTokens[key]:
                    print(self.dicTokens[key])
    
    def simulate(self):
        a = dfaSimulation(self.dfaD)
        a.SimulationTokens(self.text)
    
a = ScannerGen('scanners/AFD_yal0', 'yalex-tests/lectura.txt')
a.simulate()