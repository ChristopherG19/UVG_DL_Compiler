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
            
        # print("\nFinal_States: ", self.finalStates)
        # print("\nDic Tokens", self.dicTokens)
        # print("\nDic Tokens V2", self.dicTokensV2)

        self.equivalent_states = {}
        # Key: dictokensV2, Value: finalStates
        for key, value in self.finalStates.items():
            for key2, value2 in self.dicTokensV2.items():
                if value == value2:
                    self.equivalent_states[key2] = [key]
                else:
                    ts = True
                    for val in value2:
                        if val not in value: 
                            ts = False
                        
                    if ts:
                        self.equivalent_states[key2] = [key]
        
        # print("\nEquivalent Tokens", self.equivalent_states)
    
    def simulate(self):
        a = dfaSimulation(self.dfaD)
        return a.SimulationTokens(self.text)
    
    def get_token(self, symbol, state):
        for key, value in self.equivalent_states.items():
            if state in value:
                for key2,value2 in self.dicTokens.items():
                    if symbol == value2:
                        return self.dicTokens[key2]

                if symbol == self.dicTokens[key]:
                    return self.dicTokens[key]
                else:
                    return self.dicTokens[key]
            else:
                for key, value in self.dicTokensV2.items():
                    if value == self.finalStates[state]:
                        return self.dicTokens[key]
        
    def print_listTokens(self, listTokens):
        for token in listTokens:
            if(token[1] == 'Error'):
                print(f"-> {token[0]}: Error léxico")
            else:
                temp = ""
                if "\n" in token[0] or token[0] == " " or token[0] == "":
                    temp = repr(token[0])
                else:
                    temp = token[0]
                print(f"-> {temp}: {self.get_token(token[0], token[1][0])}")
        
Scan = ScannerGen('scanners/AFD_yal4', 'yalex-tests/lectura.txt')
listToks = Scan.simulate()
Scan.print_listTokens(listToks)
print()