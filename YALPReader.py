# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

import pickle
from tools.components import *
from automatas import *

class YalpLector():
    def __init__(self, file, tokensYal):
        self.file = file
        self.tokensYalp = []
        self.grammar = []
        self.productions = []
        self.finalLines = []
    
        with open(tokensYal, 'rb') as f:
            pickle.load(f)
            pickle.load(f)
            self.tokensY = pickle.load(f)
            
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
                
        tokensYa = []
        tokenBrackets = {}
        for i in self.tokensY:
            a = i.Create_CleanDefinition()
            if a[2] != 'Sin funcion':
                valueBrackets = self.getTokensYal(self.get_brackets_info(a[2]))
                tokensYa.append(valueBrackets)
                if (a[0] not in tokenBrackets):
                    tokenBrackets[valueBrackets] = a[0]
            else:
                tokenBrackets[a[0].upper()] = None
                    
        productionsLines = self.tokens(tokensYa)
        production = []
        for line in productionsLines:
            if (len(line) == 1 and line[0] == ';') and line.endswith(";"):
                self.productions.append(" ".join(production))
                production = []
            else:  
                production.append(line)
            
        print("------ Gramatica ------") 
        for i in self.grammar:
            print(i)
            
        print("\n------ Tokens Yalp ------")
        for i in self.tokensYalp:
            print(i)
            
        print("\n------ Producciones ------")
        newProductions = []
        for i in self.productions:    
            temp = i.split(" ")
            newP = []
            for t in temp:
                if t.isupper():
                    newP.append(t)
                    continue
                else:
                    t = t.capitalize()
                    newP.append(t)
            i = " ".join(newP)
            newProductions.append(i)
            print(i)
            
        print()
        self.productions = newProductions

        newProductions = []
        for production in self.productions:
            tempLine = production.split(" ")
            tempNewProduction = []
            for elem in tempLine:
                if elem == tempLine[0]:
                    tempNewProduction.append(elem+" →")
                else:
                    tempNewProduction.append(elem)
            newProductions.append(" ".join(tempNewProduction))
        
        print()
        ProductionsFinal = []
        for element in newProductions:
            arrow = "→"
            if ("->" in element):
                arrow = "->"
            elif ("→" in element):
                arrow = "→"
                
            sides = element.split(arrow)
            sides = [elem.strip() for elem in sides]
            listRight = []

            for prod in [x.strip() for x in sides[1].split("|")]:
                listProd = []
                for elem in prod.split(" "):
                    if(elem.isupper()):
                        newItem = ProductionItem(elem, tokenBrackets[elem])
                        newItem.setType(True)
                        listProd.append(newItem)
                    else:
                        newItem = ProductionItem(elem[0], elem.lower())
                        newItem.setType(False)
                        listProd.append(newItem)
                        
                listRight.append(listProd)
               
            for rightS in listRight: 
                newT = ProductionItem(sides[0].strip()[0], sides[0].strip().lower())
                newT.setType(False)
                ProductionsFinal.append(Production(newT, rightS))
                
        dotItem = ProductionItem('°')
        dotItem.setFinal(True)
        Aumentada = self.productions[0][0]
        newItem = ProductionItem(Aumentada)
        newItemB = ProductionItem(f"{Aumentada}'")
        newProd = Production(newItemB, [dotItem, newItem])
        ProductionsFinal.insert(0, newProd)        
        
        
        for x in ProductionsFinal:
            print(x)
        
        print()
        
    def get_brackets_info(self, texto):
        llave_abierta = texto.find("{")
        llave_cerrada = texto.rfind("}")
        if llave_abierta >= 0 and llave_cerrada >= 0:
            return texto[llave_abierta+1:llave_cerrada].strip()
        else:
            return None
        
    def getTokensYal(self, text):
        return text.split(" ",1)[1]
        
    def tokens(self, Defined):
        linesWithoutTokens = []
        ignoreTokens = []
        print("\n------ Verificacion de tokens ------\n")
        for line in self.finalLines:
            if("%token" not in line):
                if("IGNORE" in line):
                    tempToks = line.split(" ")[1:]
                    if len(tempToks) > 1:
                        for i in tempToks:
                            ignoreTokens.append(i)
                    else:
                        ignoreTokens.append(tempToks[0])
                else:
                    if("%%" in line):
                        continue
                    linesWithoutTokens.append(line.strip())
            
        alltokens = []
        notDefined = set()
        for line in self.finalLines:
            if("%token" in line):
                tempLTokens = line.split(" ")[1:]
                if(len(tempLTokens) > 1):
                    for tok in tempLTokens:
                        if tok not in self.tokensYalp:
                            if tok in Defined:
                                if tok not in ignoreTokens:
                                    self.tokensYalp.append(tok)
                            else:
                                notDefined.add(tok)

                        alltokens.append(tok)             
                else:
                    if tempLTokens[0] not in self.tokensYalp:
                        if(tempLTokens[0] in Defined):
                            if tempLTokens[0] not in ignoreTokens:
                                self.tokensYalp.append(tempLTokens[0])
                        else:
                            notDefined.add(tempLTokens[0])

                        alltokens.append(tempLTokens[0])           
                
        repeated = {}
        for tok in alltokens:
            count = alltokens.count(tok)
            if count > 1:
                if tok not in repeated:
                    repeated[tok] = count
                
        if notDefined:
            print("Tokens Yalp presentes en Yal: No estan todos definidos\n")
            for el in notDefined:
                print(f"Token: {el} no definido en yal")
        else:
            print("Tokens Yalp presentes en Yal: Si estan todos definidos\n")

        for k,v in repeated.items():
            print(f"Token: {k} definido mas de una vez ({v} en total)")
        
        for tok in ignoreTokens:
            if tok in notDefined or tok not in alltokens:
                continue
            else:
                print(f"Token: {tok} ignorado")   
                
        return linesWithoutTokens

numberFile = 4
a = YalpLector(f'./yalp-tests/slr-{numberFile}.yalp', f'./scanners_dfa/AFD_yal{numberFile}')
a.read()