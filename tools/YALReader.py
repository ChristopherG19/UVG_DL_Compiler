# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from tools.components import *

class YalLector():
    def __init__(self, file):
        self.file = file
        self.regexFinal = ""
        self.definiciones = []
        self.cleanDefiniciones = []
        self.rules = []
        self.tempRegex = ""

    def read(self):
        with open(self.file, 'r') as file:
            lines = file.readlines()
            
        lines_without_c = []
        capturing_rules = False
        comment = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            temp = ""
            for symbol in range(len(line)):
                if not comment:
                    if line[symbol] == '(':
                        if line[symbol+1] == '*':
                            comment = True
                            continue
                        else:
                            temp += line[symbol]
                    else:
                        temp += line[symbol]
                else:
                    if line[symbol] == '*':
                        if line[symbol+1] == ')':
                            continue
                    elif line[symbol] == ')':
                        if line[symbol-1] == '*':
                            comment = False
                            continue
                    
            
            NewLine = temp.strip()
            if NewLine:
                lines_without_c.append(temp.strip())
                
        Errors = []

        for pos, cleanLine in enumerate(lines_without_c):
            split_line_temp = cleanLine.strip().split("=", 1)
            if len(split_line_temp) == 2:
                leftSide, rightSide = (el.strip() for el in split_line_temp)
                if(leftSide.strip().split(" ")[0].lower() == "let"):
                    self.definiciones.append(cleanLine)
                elif(leftSide.strip().split(" ")[0].lower() == "rule"):
                    for i in range(pos, len(lines_without_c)):
                        self.rules.append(lines_without_c[i].strip())                     
                    break
                else:
                    er = leftSide.strip().split(" ")[0]
                    Errors.append((None, leftSide, f"{er} no definido"))
            else:
                Errors.append((None, split_line_temp[0], "Asignacion incorrecta"))
        
        # Definiciones
        print("Definiciones:")
        for i in self.definiciones:
            print("\t","-"*40)
            print("\t-> ", i)
            print("\t","-"*40)

        # Limpiar definiciones y crear diccionario de llave(token), valor(descripción)
        for defin in self.definiciones:
            name_desc = defin.split('=', 1)
            name = name_desc[0].split(' ')[1]
            desc = name_desc[1].strip()
            if(desc.startswith('[') and desc.endswith(']')):
                if(self.has_escape_characters(desc)):
                    asciiCodes = self.get_list_ascii(desc)
                    regexAscii = self.convert_ascii(asciiCodes)
                    newDef = Definition(name, regexAscii)
                    self.cleanDefiniciones.append(newDef)
                else:
                    if('-' in desc): 
                        ranges = self.get_ranges(desc)
                        regexRanges = self.convert_ranges(ranges)
                        newDef = Definition(name, regexRanges)
                        self.cleanDefiniciones.append(newDef)
                    else:
                        desc = desc.replace('[', '').replace(']', '').replace('"', '').replace("'", "")
                        newregex = []
                        for ch in desc:
                            sym = Simbolo(ch)
                            symS = Simbolo('|')
                            symS.setType(True)
                            newregex.append(sym)
                            newregex.append(symS)
                            
                        # Se elimina el último or que se agrega    
                        newregex = newregex[:-1]
                        symPA = Simbolo('(')
                        symPA.setType(True)
                        symPC = Simbolo(')')
                        symPC.setType(True)
                        newregex.insert(0, symPA)
                        newregex.append(symPC)
                        newDef = Definition(name, newregex)
                        self.cleanDefiniciones.append(newDef)
                                    
            else:
                desc = self.modify_desc(desc)
                newDef = Definition(name, desc)
                self.cleanDefiniciones.append(newDef)
                
        print()
        # Limpieza de rules
        if(self.rules != []):
            self.rules.remove(self.rules[0])
            
            # Se obtiene la regex temporal sin procesar
            self.tempRegex, self.tempRegexV2 = self.get_rule_regex(self.rules)
            
            print("Definiciones procesadas (completas)")
            for definition in self.cleanDefiniciones:
                print("-"*70)
                print(definition.lintDesc())
                print("-"*70)
                print()

            print()
            ls = [l.label for l in self.tempRegex]
            print("Regex sin procesar:", "".join(ls))
            print()
            
            self.regexFinal = self.get_final_regex(self.tempRegex)
            self.regexFinalV2 = self.get_final_regex(self.tempRegexV2)
            ls = [l.label if not l.isSpecialChar else repr(l.label) for l in self.regexFinal]
            print("Regex final en infix:", "".join(ls))

        return (self.regexFinal, self.regexFinalV2, self.cleanDefiniciones)

    # Verificar si existen caracteres de escape
    def has_escape_characters(self, line):
        escape_chars = ['\\','\n', '\r', '\t', '\b', '\f', '\v', '\a']
        for i in escape_chars:
            if i in line:
                return True
        return False
    
    # Convertir a ascii los delimitadores, simbolo para denotar el espacio en blanco °
    def get_list_ascii(self, line):
        listAscii = []
        
        i = 0
        while i < len(line):
            if line[i] in "[]'":
                i += 1
                continue
            elif line[i] == '\\':
                if i < len(line) - 1 and line[i+1] == 't':
                    listAscii.append(ord('\t'))
                    i += 2
                    continue
                elif i < len(line) - 1 and line[i+1] == 'n':
                    listAscii.append(ord('\n'))
                    i += 2
                    continue
                elif i < len(line) - 1 and line[i+1] == 's':
                    listAscii.append(ord(' '))
                    i += 2
                    continue
            elif line[i] in (' ', '\t', '\n'):
                if (line[i] == ' '):
                    listAscii.append(ord(' '))
                else:
                    listAscii.append(ord(line[i]))
                i += 1
                continue
            else:
                i += 1

        return listAscii
    
    # Convertir lista ascii a regex
    def convert_ascii(self, asciiCodes):
        regexAscii = []
        symS = Simbolo('|')
        symS.setType(True)
        
        for code in asciiCodes:
            if(type(code) == str):
                sym = Simbolo(code)
                sym.setSpecialType(True)
                regexAscii.append(sym)
                regexAscii.append(symS)
            else:
                sym = Simbolo(chr(code)) 
                sym.setSpecialType(True)
                regexAscii.append(sym)
                regexAscii.append(symS)
        
        # Se elimina el último or que se agrega    
        regexAscii = regexAscii[:-1]
        symPA = Simbolo('(')
        symPA.setType(True)
        symPC = Simbolo(')')
        symPC.setType(True)
        regexAscii.insert(0, symPA)
        regexAscii.append(symPC)
        
        return regexAscii

    # Se crean los rangos
    def get_ranges(self, line):
        ranges = []
        line = line.replace("'", '')
        
        for pos, charac in enumerate(line):
            if charac in "[]'":
                continue
            else:
                if charac == '-':
                    start = ord(line[pos-1])
                    end = ord(line[pos+1])
                    ranges.append([start, end])
        return ranges
    
    # Rangos a regex
    def convert_ranges(self, ranges):
        regexRanges = []
        newRanges = []
        symS = Simbolo('|')
        symS.setType(True)
        
        # Se lee cada rango encontrado
        for i in ranges:
            elementsRange = []
            # Se obtienen los elementos entre cada límite del rango
            for j in range(i[0], i[1]+1):
                sym = Simbolo(chr(j))
                elementsRange.append(sym)
            newRanges.append(elementsRange)
        
        for rango in newRanges:    
            for symbol in rango:
                regexRanges.append(symbol)
                regexRanges.append(symS)
        
        # Se elimina el último or que se agrega    
        regexRanges = regexRanges[:-1]
        
        symPA = Simbolo('(')
        symPA.setType(True)
        symPC = Simbolo(')')
        symPC.setType(True)
        regexRanges.insert(0, symPA)
        regexRanges.append(symPC)
        
        return regexRanges
    
    # Se modifican las descripciones para que tomen un formato adecuado
    def modify_desc(self, desc):
        desc = desc.replace('"', '').replace("'", '').replace(" ", "")
        
        newDesc = []
        elemCor = ''
        elem = ''
        in_cor = False
        
        symS = Simbolo('|')
        symS.setType(True)
        
        for char in desc:         
            if char.isalnum():
                elem += char
            else:
                if elem != '':
                    sym = Simbolo(elem)
                    newDesc.append(sym)
                    
                if elem == '_':
                    sym = Simbolo(elem)
                    newDesc.append(sym)
                    
                if elem == '→':
                    sym = Simbolo(ord(elem))
                    newDesc.append(sym)
        
                if char == '[':
                    in_cor = True
                    newSim = Simbolo('(')
                    newSim.setType(True)
                    newDesc.append(newSim)

                elif char == ']':
                    in_cor = False
                    for i in elemCor:
                        news = Simbolo(i)
                        newDesc.append(news)
                        newDesc.append(symS)
                    newDesc.pop()
                    newSim = Simbolo(')')
                    newSim.setType(True)
                    newDesc.append(newSim)
                    elemCor = ''
                elif in_cor:
                    elemCor += char
        
                sym2 = Simbolo(char)
                if char == '.':
                    newDesc.append(sym2)
                if char != '.' and char != '[' and char != ']' and not in_cor:
                    if(sym2.label == '_'):
                        sym2.setType(False)
                        newDesc.append(sym2)
                    else:
                        sym2.setType(True)
                        newDesc.append(sym2)
                elem = ''
                
        symPA = Simbolo('(')
        symPA.setType(True)
        symPC = Simbolo(')')
        symPC.setType(True)
        newDesc.insert(0, symPA)
        newDesc.append(symPC)
            
        return newDesc
    
    # Se obtiene la regex a partir de rule
    def get_rule_regex(self, rules):
        
        regex_list = []
        regex_symbols = []
        symS = Simbolo('|')
        symS.setType(True)
        tempRules = []

        for line in rules:
            # Eliminar comillas y espacios en blanco
            line = line.replace("'", '')
            line = line.replace('"', '')
    
            line = line.strip()
            if(line[0] == '|'):
                tempRules.append(symS)
                tempRules.append(line[1:])
            else:
                tempRules.append(line)

        ListRules = []
        tempLi = []
        tempEl = ""
        for element in tempRules:
            if(element == tempRules[-1]):
                ListRules.append([element.strip()])
            if type(element) == Simbolo and element.label == '|' and element.isOperator:
                tempLi.append(tempEl)
                ListRules.append(tempLi)
                ListRules.append(element)
                tempLi = []
                tempEl = ""
            else:
                tempEl += element.strip()+" "
            
        # Se limpian espacios extra
        listTokensDef = []
        for TokenDef in ListRules:
            if type(TokenDef) == Simbolo and TokenDef.label == '|' and TokenDef.isOperator:
                continue
            else:
                parts = TokenDef[0].strip().split(" ", 1)  
                if len(parts) == 1:
                    listTokensDef.append([parts[0].strip(), None])
                else:
                    if(parts[0].strip() == 'â†’'):
                        listTokensDef.append(['\u2192', parts[1].strip()])
                    else:
                        listTokensDef.append([parts[0].strip(), parts[1].strip()])

        # Se obtienen los tokens para la regex y se guarda la descripción
        for el in listTokensDef:
            name, func = el
            
            # Se agrega a la lista del regex
            regex_list.append(name.strip())
            
            # Se crean las definiciones
            for defi in self.cleanDefiniciones:
                if defi.name == name:
                    defi.func = func
        
            names = [defin.name for defin in self.cleanDefiniciones]
            if name not in names:
                newDef = Definition(name, None, func)
                self.cleanDefiniciones.append(newDef)
        
        for symbol in regex_list:
            sym = Simbolo(symbol)
            regex_symbols.append(sym)
            regex_symbols.append(symS)
                    
        # Se elimina el último or que se agrega    
        regex_symbols = regex_symbols[:-1]
        newRegex_symbols = []
        
        # Se agregan terminaciones a cada subarbol
        for i, elem in enumerate(regex_symbols):
            if (not elem.isOperator) or i == 0:
                newRegex_symbols.append(elem)
            else:
                anterior = newRegex_symbols[i-1]
                newSim = Simbolo('#'+anterior.label) 
                newRegex_symbols.append(newSim)

        if newRegex_symbols[-1].label != '|':
            anterior = newRegex_symbols[-1]
            newSim = Simbolo('#'+anterior.label) 
            newRegex_symbols.append(newSim)
        
        finalRegexSymbols = []  
        for i in range(len(newRegex_symbols)):
            finalRegexSymbols.append(newRegex_symbols[i])
            if (i+1) % 2 == 0 and i != len(newRegex_symbols)-1:
                finalRegexSymbols.append(symS)
                
        return (regex_symbols, finalRegexSymbols)

    # Se determina si un token es o no un terminal
    def isTerminal(self, token):
        for defi in self.cleanDefiniciones:
            if (defi.name == token.label):
                if(defi.desc != None):
                    return False
        return True

    # Se obtiene la definicion de un token
    def get_definition(self, token):
        for defi in self.cleanDefiniciones:
            if (defi.name == token.label):
                if(defi.desc != None):
                    return defi.desc

    # Algoritmo bottom_down para lectura de tokens y definiciones
    def bottom_Down(self, actualT, newRegex):
        for tok in actualT:
            if(not self.isTerminal(tok)):
                newRegex = self.bottom_Down(self.get_definition(tok), newRegex)
            else:
                newSym = Simbolo(tok.label)
                newSym.setToken(tok.token)
                
                if(tok.isSpecialChar):
                    newSym.setSpecialType(True)
                
                if(tok.isOperator):
                    newSym.setType(True)
  
                newRegex.append(newSym)
                
        return newRegex

    # Regex final con las sustituciones hechas
    def get_final_regex(self, finalRegex):
        final_regex = finalRegex
        newRegex = []
        Final = self.bottom_Down(final_regex, newRegex)
        return Final
