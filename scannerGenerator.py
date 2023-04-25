# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

import pickle
import os
from simulation.dfaSimulation import *
from tools.components import get_tokens_States, get_final_States, get_final_States_tokens

class ScannerGen():
    def __init__(self, nameFile, inputText):
        self.name = nameFile
        with open(self.name, 'rb') as f:
            self.dfaD = pickle.load(f)
            self.dfaVerify = pickle.load(f)
            self.definiciones = pickle.load(f)
        f.close()

        self.cleanDefinitions = [] 
        for definition in self.definiciones:
            self.cleanDefinitions.append(definition.Create_CleanDefinition())

        print(self.cleanDefinitions)

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
        
    def get_new_list_tokens(self, listTokens):
        self.newListTokens = []
        for token in listTokens:
            if(token[1] == 'Error'):
                self.newListTokens.append((token[0], "Error léxico"))
            else:
                self.newListTokens.append((token[0], self.get_token(token[0], token[1][0])))

        return self.newListTokens
    
    def get_tok_brackets(self, texto):
        cadena = ""
        i = 0
        while i < len(texto):
            if texto[i:i+6] == "return":
                i += 6
                while i < len(texto) and texto[i] == " ":
                    i += 1
                while i < len(texto) and texto[i] != "}":
                    cadena += texto[i]
                    i += 1
                break
            else:
                i += 1
        return cadena.strip()
    
    
    def get_brackets_info(self, texto):
        llave_abierta = texto.find("{")
        llave_cerrada = texto.rfind("}")
        if llave_abierta >= 0 and llave_cerrada >= 0:
            return texto[llave_abierta+1:llave_cerrada].strip()
        else:
            return None
    
    def build_scanner(self):
        self.scanner_file = f"scanners/scanner_yal{self.name[-1]}.py"
        with open(self.scanner_file, "w") as f:
            f.write("# Universidad del Valle de Guatemala\n")
            f.write("# Facultad de Ingenieria\n")
            f.write("# Departamento de Ciencias de la Computacion\n")
            f.write("# Diseno de lenguajes\n")
            f.write("# Christopher Garcia 20541\n")
            
            f.write("\nfrom tools.definitionsScanner import *\n\n")
            f.write("def tokens_returns(symbol):\n")
            for element in self.cleanDefinitions:
                if(element[2] != 'Sin funcion'):
                    func = self.get_brackets_info(element[2])
                    f.write(f"\tif symbol == '{element[0]}':\n\t\t{func}\n")
                        
Scan = ScannerGen('scanners_dfa/AFD_yal3', 'yalex-tests/lectura.txt')
listToks = Scan.simulate()
Scan.print_listTokens(listToks)
Scan.get_new_list_tokens(listToks)
print()
Scan.build_scanner()
print()