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
        self.grammarSymbols = []
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
        self.tokenBrackets = {}
        for i in self.tokensY:
            a = i.Create_CleanDefinition()
            if a[2] != 'Sin funcion':
                valueBrackets = self.getTokensYal(self.get_brackets_info(a[2]))
                tokensYa.append(valueBrackets)
                if (a[0] not in self.tokenBrackets):
                    self.tokenBrackets[valueBrackets] = a[0]
            else:
                self.tokenBrackets[a[0]] = None

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
                    newP.append(t)
            i = " ".join(newP)
            newProductions.append(i)
            print(i)
            
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

        self.ProductionsFinal = []
        dotItem = ProductionItem('°')
        dotItem.setFinal(True)
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
                        newItem = ProductionItem(self.tokenBrackets[elem], elem)
                        newItem.setType(True)
                        listProd.append(newItem)
                    else:
                        newItem = ProductionItem(elem[0].upper(), elem)
                        newItem.setType(False)
                        listProd.append(newItem)

                listRight.append(listProd)
               
            for rightS in listRight: 
                newT = ProductionItem(sides[0].strip()[0].upper(), sides[0].strip())
                newT.setType(False)
                self.ProductionsFinal.append(Production(newT, rightS))
                
        #print(self.ProductionsFinal)
                
        Aumentada = self.productions[0][0].upper()
        newItem = ProductionItem(Aumentada)
        newItemB = ProductionItem(f"{Aumentada}'")
        newProdAumentada = Production(newItemB, [dotItem, newItem])
        self.ProductionsFinal.insert(0, newProdAumentada)        
        
        # for x in self.ProductionsFinal:
        #     print(x)
                        
        finalStates = self.get_Final_States(newProdAumentada)
        
        print()
        
    def get_gramatical_symbols(self):
        self.gramaticaSymbol = set()
        for i in self.grammar:
            for j in i.split(" "):
                if j != ' ' and j != '' and j != '|' and j != '->' and j != '→':
                    if(j.isalnum()):
                        self.gramaticaSymbol.add(j)
                    else:
                        self.gramaticaSymbol.add(j)
                    
        self.grammarSymbols = list(self.gramaticaSymbol)
                    
    def closure(self, productions):
        dotItem = ProductionItem('°')
        dotItem.setFinal(True)
        J = productions
        for prod in J:
            for i in range(len(prod.rs)):
                if(prod.rs[i].dot):
                    if(i+1 < len(prod.rs)):
                        if(not prod.rs[i+1].terminal):
                            for produ in self.ProductionsFinal:
                                if produ.ls.label == prod.rs[i+1].label:
                                    if(not any([v.dot for v in produ.rs])):
                                        produ.rs.insert(0, dotItem)
                                    if produ not in J:
                                        J.append(produ)
        
        return J
    
    def goto(self, items, symbol):
        newState = []
        for prod in items:
            #print("Produccion: ", prod)
            for i in range(len(prod.rs)):
                if(prod.rs[i].dot):
                    if(i+1 < len(prod.rs)):
                        comp = [k for k, v in self.tokenBrackets.items() if v == symbol]
                        if(prod.rs[i+1].label == symbol or prod.rs[i+1].label == (comp[0] if len(comp)>0 else None)):
                            #print(symbol, prod)
                            indice = prod.rs.index([x for x in prod.rs if x.dot][0])
                            if indice < len(prod.rs):
                                newPrRS = prod.rs.copy()
                                temp = prod.rs[indice+1]
                                newPrRS[indice+1] = prod.rs[indice]
                                newPrRS[indice] = temp
                                newProd = Production(prod.ls, newPrRS)
                                #print(symbol, newProd)
                                newState.append(newProd)

        return self.closure(newState)
        
    def get_Final_States(self, aumentada):
        self.get_gramatical_symbols()

        NumStates = 0
        finalStates = {}
        C = self.closure([aumentada])
        finalStates[f"I{NumStates}"] = C
        transitions = []
        Items = [C]
        for group in Items:
            for symbol in self.grammarSymbols:
                result = self.goto(group, symbol)
                if(result != []):
                    if result not in finalStates.values():
                        NumStates += 1
                        finalStates[f"I{NumStates}"] = result
                        for k,v in finalStates.items():
                            if v == group:
                                transitions.append([k, symbol, f"I{NumStates}"])
                    if result not in Items:
                        Items.append(result)
        print()
        for k,v in finalStates.items():
            print(k, len(v))
            for el in v:
                print(el)
            print()
        print()
        print(transitions)
        
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

numberFile = 1
a = YalpLector(f'./yalp-tests/slr-{numberFile}.yalp', f'./scanners_dfa/AFD_yal{numberFile}')
a.read()