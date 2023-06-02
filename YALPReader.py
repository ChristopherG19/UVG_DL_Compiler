# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

import copy
import pickle
from automatas.AFD import AFD
from tools.components import *
from tools.showGraph import showGraphDFA
from prettytable import PrettyTable

class YalpLector():
    def __init__(self, file, tokensYal, tokensText, numberFile):
        self.file = file
        self.tokensYalp = []
        self.grammar = []
        self.grammarSymbols = []
        self.productions = []
        self.finalLines = []
        self.numberFile = numberFile
        self.checkProductions = {}
        self.prods = []
    
        with open(tokensYal, 'rb') as f:
            pickle.load(f)
            pickle.load(f)
            self.tokensY = pickle.load(f)
            
        with open(tokensText, 'rb') as f:
            self.tokensText = pickle.load(f)

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
        self.terminales = []
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
                        newItem = ProductionItem(elem, self.tokenBrackets[elem])
                        newItem.setType(True)
                        listProd.append(newItem)
                        self.terminales.append(elem)
                    else:
                        if elem in [x.lower() for x in self.tokensVeri]:
                            newItem = ProductionItem(elem.upper(), self.tokenBrackets[elem.upper()])
                            newItem.setType(True)
                            listProd.append(newItem)
                            self.terminales.append(elem.upper())
                        else:
                            newItem = ProductionItem(elem, elem[0].upper())
                            newItem.setType(False)
                            listProd.append(newItem)

                listRight.append(listProd)
               
            for rightS in listRight: 
                newT = ProductionItem(sides[0].strip().replace(":",""), sides[0].strip()[0].upper())
                newT.setType(False)
                self.ProductionsFinal.append(Production(newT, rightS))
                
        self.prods = [copy.deepcopy(objeto) for objeto in self.ProductionsFinal]
                
        self.simboloInicial = self.ProductionsFinal[0].ls
        Aumentada = self.ProductionsFinal[0].ls
        newItemB = ProductionItem(f"{Aumentada}'")
        newProdAumentada = Production(newItemB, [dotItem, Aumentada])
        self.AumentadaEl = Aumentada
        self.AumentadaElB = newItemB
        self.ProductionsFinal.insert(0, newProdAumentada)        
        
        print("\n------ Producciones Finales ------")
        for x in self.ProductionsFinal:
            print(x)
        print()

        return self.get_Final_States(newProdAumentada)
        
    def get_gramatical_symbols(self):
        self.gramaticaSymbol = set()
        for i in self.ProductionsFinal:
            for j in i.rs:
                if j.dot:
                    continue
                else:
                    self.gramaticaSymbol.add(j.label)
            self.gramaticaSymbol.add(i.ls.label)
                
        self.grammarSymbols = sorted(list(self.gramaticaSymbol))
                 
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
            for i in range(len(prod.rs)):
                if(prod.rs[i].dot):
                    if(i+1 < len(prod.rs)):
                        comp = [k for k, v in self.tokenBrackets.items() if v == symbol]
                        if(prod.rs[i+1].label == symbol or prod.rs[i+1].label == (comp[0] if len(comp)>0 else None)):
                            indice = prod.rs.index([x for x in prod.rs if x.dot][0])
                            if indice < len(prod.rs):
                                newPrRS = prod.rs.copy()
                                temp = prod.rs[indice+1]
                                newPrRS[indice+1] = prod.rs[indice]
                                newPrRS[indice] = temp
                                newProd = Production(prod.ls, newPrRS)
                                newState.append(newProd)

        return self.closure(newState)
      
    def first(self, symbol):
        firstSet = []
        stack = [symbol]
        checkProds = [symbol]

        if symbol in self.terminales:
            return stack
        else:
            while stack:
                check = stack.pop(0)
                for prod in self.ProductionsFinal:
                    if prod.ls.label == check:
                        if prod.rs[0].label in self.terminales:
                            firstSet.append(prod.rs[0].label)
                        else:
                            if prod.rs[0].label not in stack and prod.rs[0].label not in checkProds:
                                stack.append(prod.rs[0].label)
                                checkProds.append(prod.rs[0].label)
        
        return firstSet
        
            
    def follow(self, symbol, visited=None):
        if visited is None:
            visited = set()

        followSet = []

        if symbol == self.simboloInicial.label:
            followSet.append('$')

        for prod in self.ProductionsFinal:
            for i in range(len(prod.rs)):
                if symbol == prod.rs[i].label:
                    if prod.rs[i].label == prod.rs[-1].label:
                        if symbol != prod.ls.label and prod.ls.label not in visited:
                            visited.add(prod.ls.label)
                            fol = self.follow(prod.ls.label, visited)
                            for el in fol:
                                if el not in followSet:
                                    followSet.append(el)
                    if (i + 1) < len(prod.rs):
                        firs = self.first(prod.rs[i + 1].label)
                        for el in firs:
                            if el not in followSet:
                                followSet.append(el)

        return followSet
      
    def get_Final_States(self, aumentada):
        self.get_gramatical_symbols()
        NumStates = 0
        finalStates = {}
        C = self.closure([aumentada])
        finalStates[f"I{NumStates}"] = C
        transitions = []
        Items = [C]
        movements = []
        Nmovements = []
        for group in Items:
            for symbol in self.grammarSymbols:
                result = self.goto(group, symbol)
                if(result != []):
                    movements.append((group, symbol, result))
                    if result not in finalStates.values():
                        Items.append(result)
                        NumStates += 1
                        finalStates[f"I{NumStates}"] = result
                        for k,v in finalStates.items():
                            if v == group:
                                transitions.append(Transition(k, symbol, f"I{NumStates}"))
                    else:
                        for k,v in finalStates.items():
                            if v == group:
                                for k2,v2 in finalStates.items():
                                    if v2 == result:
                                        transitions.append(Transition(k, symbol, k2))
        
        for x,y in finalStates.items():
            for m in movements:
                if m[0] == y:
                    for x2,y2 in finalStates.items():
                        if m[2] == y2:
                            Nmovements.append((x, m[1], x2))
                            break
                    
        # for val in Nmovements:
        #     print(val[0], val[1], val[2])
        #     print()
        
        InState = None
        FnState = None            
        for k,v in finalStates.items():
            print(k, len(v))
            for el in v:
                if el.ls.label == self.AumentadaElB.label:
                    for i in range(len(el.rs)):
                        if el.rs[i].label == self.AumentadaEl.label and el.rs[i-1].dot:
                            FnState = k
                            break
                    for i in range(len(el.rs)):
                        if(i+1 < len(el.rs)):
                            if el.rs[i].dot and el.rs[i+1].label == self.AumentadaEl.label:
                                InState = k
                                break
                print(el)
            print()

        # print("Estado inicial", InState)
        # print("Estado final", FnState)
        # print("Cantidad de estados:", len(finalStates.keys()))
        # print("Transiciones:")
        # for trans in transitions:
        #   print(trans)
        # print("Estados:", list(finalStates.keys()))
        
        lr0 = AFD(InState, [FnState], len(finalStates.keys()), transitions, list(finalStates.keys()))
        showGraphDFA(lr0, f"LR0_{self.numberFile}")
                
        action = []
        goto = []
        
        for ele in self.grammarSymbols:
            if ele != self.AumentadaElB.label:
                if ele.isupper():
                    action.append(ele)
                else:
                    goto.append(ele)  
        
        action.append('$')    
        
        actions = self.get_actions_list(action, finalStates, Nmovements, FnState)
        gotos = self.get_goto_list(goto, transitions)
        
        columnsActions = {}
        for elA in action:
            column = []
            for act in actions[0]:
                if elA == act[1]:
                    column.append((act[0], act[2]))
                    
            for act in actions[1]:
                for el in act[1]:
                    if elA == el:
                        column.append((act[0], act[2]))

            columnsActions[elA] = column
        
        finalColumnA = {}
        for x,y in columnsActions.items():

            check = {}
            for el in y:
                if el[0] not in check:
                    check[el[0]] = [el[1]]
                else:
                    check[el[0]].append(el[1])
                    
            for a, b in check.items():
                if len(b) > 1 and len(set(b)) > 1: 
                    return (a,b) 
            
            newColumn = ['' for x in range(len(finalStates.keys()))]
            for i in y:
                newColumn[int(i[0][1:])] = i[1]
            
            if(x == '$'):
                newColumn[int(FnState[1:])] = 'acc'
            
            finalColumnA[x] = newColumn
            
        columnsGoto = {}
        for elG in goto:
            column = []
            for got in gotos:
                if elG == got[1]:
                    column.append((got[0], got[2][1:]))
                    
            columnsGoto[elG] = column

        finalColumnG = {}
        for x,y in columnsGoto.items():
            newColumn = ['' for x in range(len(finalStates.keys()))]
            for i in y:
                newColumn[int(i[0][1:])] = i[1]

            finalColumnG[x] = newColumn

        prettyT = PrettyTable()
        prettyT.add_column("State", list(finalStates.keys()))
            
        for elA in action:
            prettyT.add_column(elA, finalColumnA[elA])

        for elG in goto:
            prettyT.add_column(elG, finalColumnG[elG])            

        prettyT.align = "c"
        prettyT.title = "Tabla de parseo SLR(1)"
        print(prettyT)
        
        with open(f'./tables/tabla_parseo_slr{self.numberFile}.txt', 'w', encoding="utf-8") as f:
            f.write(prettyT.get_string())
        
        return self.simulate(list(finalStates.keys()), actions, gotos, FnState)
            
    def get_actions_list(self, action, statesR, gotosM, fnState):
        actions_shift = []
        actions_reduce = []
        
        for nState, states in statesR.items():
            for symbol in action:
                for state in states:
                    for i in range(len(state.rs)):
                        if(i+1 < len(state.rs)):
                            if state.rs[i].dot and state.rs[i+1].label == symbol:
                                for gotoM in gotosM:
                                    if(gotoM[0] == nState and gotoM[1] == symbol):
                                        # print((nState, symbol, 'S'+gotoM[2][1:]))
                                        actions_shift.append((nState, symbol, 'S'+gotoM[2][1:]))
                                        break
        
        self.dicProds = {}
        for el in range(1,len(self.prods)+1):
            self.dicProds[el] = self.prods[el-1]      
            
        for nState, states in statesR.items():
            for state in states:
                if state.rs[-1].dot:
                    # print(nState, state, self.follow(state.ls.label))
                    prodVeri = Production(state.ls, state.rs[:-1])
                    if(nState != fnState):
                        for x,y in self.dicProds.items():
                            if (y.ls.label == prodVeri.ls.label):
                                for m, n in zip(y.rs, prodVeri.rs):
                                    if(len(y.rs) == len(prodVeri.rs)):
                                        if m.label == n.label:
                                            # print(nState, state, x)
                                            followL = self.follow(state.ls.label)
                                            actions_reduce.append((nState, followL, 'r'+str(x)))
                                            break
        
        return (actions_shift, actions_reduce)
        
    def get_goto_list(self, goto, transitions):
        gotos_l = []
        
        for trans in transitions:
            for el in goto:
                if trans.symbol == el:
                    gotos_l.append((trans.inState, trans.symbol, trans.fnState))
        
        return gotos_l
        
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
            print()
        else:
            print("Tokens Yalp presentes en Yal: Si estan todos definidos\n")

        for k,v in repeated.items():
            print(f"Token: {k} definido mas de una vez ({v} en total)")
        
        for tok in ignoreTokens:
            if tok in notDefined or tok not in alltokens:
                continue
            else:
                print(f"Token: {tok} ignorado")   
            
        self.tokensVeri = list(set(alltokens) - notDefined)
        return linesWithoutTokens
    
    def simulate(self, states, actions, gotos, fnState):
        result = "No"
        tokensLectura = []
        for tok in self.tokensText:
            for x,y in self.tokenBrackets.items():
                if(x == tok[1]):
                    if y == None:
                        continue
                else:
                    if(y == tok[1]):
                        tokensLectura.append((tok[0], x))
                            
        stackStates = [states[0]]
        stackSymbols = ['$']
        stackInput = []
        Actions = []
        
        for tok in tokensLectura:
            stackInput.append(tok[1])
        stackInput.append("$")

        allStacksStates = []
        allStackSymbols = []
        allStackInput = []
        
        allStacksStates.append(stackStates.copy())
        allStackSymbols.append(stackSymbols.copy())
        allStackInput.append(stackInput.copy())

        # Se agrega el primer simbolo
        first_Action = self.check_action(actions, stackStates[-1], stackInput[0], fnState)
        stackSymbols.append(stackInput.pop(0))
        if first_Action[0] == 'S':
            Actions.append(f'Shift to I{first_Action[1:]}')
            stackStates.append(f'I{first_Action[1:]}')
        elif first_Action[0] == 'r':
            getProd = self.dicProds[int(first_Action[1:])]
            Actions.append(f'Reduce by {getProd}')
            for x in range(len(getProd.rs)):
                stackSymbols.pop(0)
            stackSymbols.append(getProd.ls.label)
            
        while(1):
            allStacksStates.append(stackStates.copy())
            allStackSymbols.append(stackSymbols.copy())
            allStackInput.append(stackInput.copy())
            new_Action = self.check_action(actions, stackStates[-1], stackInput[0], fnState)
            if new_Action[0] == 'S':
                stackSymbols.append(stackInput.pop(0))
                Actions.append(f'Shift to I{new_Action[1:]}')
                stackStates.append(f'I{new_Action[1:]}')
                
            elif new_Action[0] == 'r':
                getProd = self.dicProds[int(new_Action[1:])]
                Actions.append(f'Reduce by {getProd}')
                
                for x in range(len(getProd.rs)):
                    stackSymbols.pop(-1)
                    stackStates.pop(-1)
                stackSymbols.append(getProd.ls.label)
                
                for goto in gotos:
                    if(goto[0] == stackStates[-1] and goto[1] == stackSymbols[-1]):
                        stackStates.append(goto[2])
                        break
            elif new_Action == 'Accept':
                Actions.append('Accept')
                result = "Yes"
                break
            else:
                Actions.append(new_Action)
                break
            
        if any([len(Actions) > len(x) for x in [allStacksStates, allStackInput, allStackSymbols]]) or any([len(Actions) < len(x) for x in [allStacksStates, allStackInput, allStackSymbols]]):
            print()
            for x in Actions:
                print("-",x[:-1]+allStackInput[0][0])
        else:
            prettyT = PrettyTable()
            prettyT.add_column("State", [x for x in range(len(Actions))])
            prettyT.add_column("Stack", allStacksStates)
            prettyT.add_column("Symbols", allStackSymbols)
            prettyT.add_column("Input", allStackInput)
            prettyT.add_column("Actions", Actions)

            prettyT.align = "c"
            prettyT.title = "Tabla de parseo SLR(1) Simulación "
            print(prettyT)
            
            with open(f'./tables/tabla_parseo_sim_slr{self.numberFile}.txt', 'w', encoding="utf-8") as f:
                f.write(prettyT.get_string())

        return result
    
    def check_action(self, actions, state, symbol, fnState):
        # Se revisan shifts
        for shift in actions[0]:
            if(shift[0] == state and shift[1] == symbol):
                return shift[2]
            
        # Se revisan reduces
        for reduce in actions[1]:
            if(reduce[0] == state and symbol in reduce[1]):
                return reduce[2]
            
        if state == fnState and symbol == "$":
            return "Accept"
        
        return f"Error sintáctico en estado {state} con {symbol}"
    
numberFile = 1
a = YalpLector(f'./yalp-tests/slr-{numberFile}.yalp', f'./scanners_dfa/AFD_yal{numberFile}', f'./tokens/tokens_text_yal{numberFile}',numberFile)
result = a.read()
print()
print("-"*50)
if type(result) == tuple:
    print(f"Lectura final del archivo, es aceptado: No\nConflicto en {result[0]} por estas acciones {','.join(result[1])}")
else:
    print("Lectura final del archivo, es aceptado:", result)
print("-"*50)
print()