# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from infixToPostfix import Conversion
from components import *
from all import *

class YalLector():
    def __init__(self, file):
        self.file = file
        self.regexFinal = ""
        self.definiciones = []
        self.cleanDefiniciones = []
        self.rules = []
        self.tempRegex = ""
        self.dirtyFunctionsRules = {}
        
    def read(self):
        with open(self.file, 'r') as file:
            lines = file.readlines()
            
        capturing_rules = False
        for line in lines:
            if(line.startswith('(*')):
                continue
            if(line.startswith('let')):
                self.definiciones.append(line)
                
            if(line.startswith('rule')):
                capturing_rules = True
            
            if capturing_rules:
                if line != "\n" or line != " ":
                    self.rules.append(line)

        # Definiciones
        print("Definiciones:")
        for i in self.definiciones:
            print("\t","-"*40)
            print("\t-> ", i, end='')
            print("\t","-"*40)

        # Limpiar definiciones y crear diccionario de llave(token), valor(descripción)
        for defin in self.definiciones:
            name_desc = defin.split('=')
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
                        desc = desc.replace('[', '').replace(']', '').replace('"', '')
                        newregex = []
                        for ch in desc:
                            sym = Simbolo(ch)
                            symS = Simbolo('|')
                            symS.setType(True)
                            newregex.append(sym)
                            newregex.append(symS)
                            
                        # Se elimina el último or que se agrega    
                        newregex = newregex[:-1]
                        newDef = Definition(name, newregex)
                        self.cleanDefiniciones.append(newDef)
                                    
            else:
                desc = self.modify_desc(desc)
                newDef = Definition(name, desc)
                self.cleanDefiniciones.append(newDef)
                
        print()
        # Limpieza de rules
        self.rules.remove(self.rules[0])
        self.rules.remove(self.rules[-1])
        
        self.tempRegex = self.get_rule_regex(self.rules)
        
        for j in self.rules:
            self.create_descriptions(j)

        print("Definiciones procesadas (completas)")
        for definition in self.cleanDefiniciones:
            print("-"*80)
            print(definition.lintDesc())
            print("-"*80)
            print()

        print()
        ls = [l.label for l in self.tempRegex]
        print("Regex sin procesar:", "".join(ls))
        print()
        
        #self.tempRegex = self.convert_to_defs()

        self.regexFinal = self.get_final_regex()
        ls = [l.label if not l.isSpecialChar else repr(l.label) for l in self.regexFinal]
        print("Regex final en infix:", "".join(ls))

        return self.regexFinal

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

    # Se crean las definiciones: Token, Descripcion y Funcion
    def create_descriptions(self, line):
        while '(*' in line:
            start = line.find('(*')
            end = line.find('*)', start) + 2
            line = line[:start] + line[end:]

        # Eliminar comillas y espacios en blanco
        line = line.replace("|", '', 1)
        line = line.replace("'", '')
        line = line.replace('"', '')
        
        line = line.strip()

        name = ""
        func = None

        temp = line.split()
        if(len(temp) == 1):
            name = temp[0]

        if ('{' in line and '}'):
            partes = line.split('{')
            name = partes[0].strip()  # la primera parte es 'id'
            func = '{' + partes[1]    # la segunda parte es '{ return ID }'
                    
        if name == ":=":
            name = ":"   

        for defi in self.cleanDefiniciones:
            if defi.name == name:
                defi.func = func
            
        names = [defin.name for defin in self.cleanDefiniciones]

        if name not in names:
            newDef = Definition(name, None, func)
            self.cleanDefiniciones.append(newDef)
            
        return line

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
    
    def modify_desc(self, desc):
        desc = desc.replace('"', '').replace("'", '')
        
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
    
    def get_rule_regex(self, rules):
        
        regex_list = []
        regex_symbols = []
        symS = Simbolo('|')
        symS.setType(True)
        
        for line in rules:
            while '(*' in line:
                start = line.find('(*')
                end = line.find('*)', start) + 2
                line = line[:start] + line[end:]

            # Eliminar comillas y espacios en blanco
            line = line.replace("|", '', 1)
            line = line.replace("'", '')
            line = line.replace('"', '')
            line = line.replace(' ', '')
    
            line = line.strip()

            if(line.startswith(':=')):
                line = line.replace('=',"")

            # Eliminar las llaves y su contenido
            open_bracket = line.find('{')
            close_bracket = line.find('}')
            if open_bracket != -1 and close_bracket != -1:
                line = line[:open_bracket] + line[close_bracket+1:]
                    
            regex_list.append(line)
            
        for symbol in regex_list:
            sym = Simbolo(symbol)
            regex_symbols.append(sym)
            regex_symbols.append(symS)
                    
        # Se elimina el último or que se agrega    
        regex_symbols = regex_symbols[:-1]
        return regex_symbols

    def convert_to_defs(self):
        newTemp = []
        symS = Simbolo('|')
        symS.setType(True)
        
        for t in self.tempRegex:
            for defi in self.cleanDefiniciones:
                if defi.name == t.label:
                    newTemp.append(defi)
                    newTemp.append(symS)
      
        # Se elimina el último or que se agrega    
        newTemp = newTemp[:-1]

        return newTemp

    def isTerminal(self, token):
        for defi in self.cleanDefiniciones:
            if (defi.name == token.label):
                if(defi.desc != None):
                    return False
        return True

    def get_definition(self, token):
        for defi in self.cleanDefiniciones:
            if (defi.name == token.label):
                if(defi.desc != None):
                    return defi.desc

    def bottom_Down(self, actualT, newRegex):
        for tok in actualT:
            if(not self.isTerminal(tok)):
                newRegex = self.bottom_Down(self.get_definition(tok), newRegex)
            else:
                newSym = Simbolo(tok.label)
                
                if(tok.isSpecialChar):
                    newSym.setSpecialType(True)
                
                if(tok.isOperator):
                    newSym.setType(True)
  
                newRegex.append(newSym)
                
        return newRegex

    def get_final_regex(self):
        final_regex = self.tempRegex
        newRegex = []
        Final = self.bottom_Down(final_regex, newRegex)
        return Final

print()
yal = YalLector('./yalex-tests/slr-4.yal')
word = yal.read()
print()

Obj = Conversion(word)
postfixExp = Obj.infixToPostfix()

print()
alphabet = Obj.get_alphabet()
print("Alfabeto: ", alphabet)

print("-----  AFD (Directo)  -----")
T = directConstruction(word, postfixExp, alphabet)
dfaD = T.buildDFA()
print(dfaD)
print()

showGraphDFA(dfaD, "Arbol Yal")