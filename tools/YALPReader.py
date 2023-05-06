# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from components import *
class YalpLector():
    def __init__(self, file):
        self.file = file
        self.tokensY = []
        self.grammar = []
        self.productions = []
        self.finalLines = []
    
    def read(self):
        with open(self.file, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            
        comment = False
        for line in lines:
            
            line = line.strip()
            if not line:
                continue
                        
            temp = ""
            for symbol in range(len(line)):
                if not comment:
                    if line[symbol] == '/':
                        if line[symbol+1] == '*':
                            comment = True
                            continue
                        else:
                            temp += line[symbol]
                    else:
                        temp += line[symbol]
                else:
                    if line[symbol] == '*':
                        if line[symbol+1] == '/':
                            continue
                    elif line[symbol] == '/':
                        if line[symbol-1] == '*':
                            comment = False
                            continue
                        
            if '->' in line or '→' in line:
                if ('->' in line):
                    line = line.replace('->', '→')
                inicio = line.find("/*") + 2
                fin = line.rfind("*/")
                subcadena = line[inicio:fin].strip()
                self.grammar.append(subcadena) 
                    
            NewLine = temp.strip()
            if NewLine:
                self.finalLines.append(temp.strip())  

        productionsLines = self.tokens()
        production = []
        for line in productionsLines:
            if (len(line) == 1 and line[0] == ';') and line.endswith(";"):
                self.productions.append(" ".join(production))
                production = []
            else:  
                production.append(line)
            
        print("\n------ Gramatica ------") 
        for i in self.grammar:
            print(i)
        print("\n------ Tokens ------")
        for i in self.tokensY:
            print(i)
        print("\n------ Producciones ------")
        for i in self.productions:    
            print(i)
        print()
        
    def tokens(self):
        linesWithoutTokens = []
        for line in self.finalLines:
            if("%token" not in line):
                linesWithoutTokens.append(line.strip())
            temp = ""
            for char in range(len(line)):
                temp += line[char]
                if(temp.lower() == "%token"):
                    tempLTokens = line.split(" ")[1:]
                    if(len(tempLTokens) > 1):
                        for tok in tempLTokens:
                            self.tokensY.append(tok)
                    else:
                        self.tokensY.append(tempLTokens[0])
        
        return linesWithoutTokens

a = YalpLector('./yalp-tests/slr-1.yalp')
a.read()