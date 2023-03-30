# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

class YalLector():
    def __init__(self, file):
        self.file = file
        self.regexFinal = ""
        self.definiciones = []
        self.cleanDefiniciones = {}
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

        for i in self.definiciones:
            print(i, end='')

        #Limpiar definiciones y crear diccionario de llave(token), valor(descripción)
        for defin in self.definiciones:
            name_desc = defin.split('=')
            name = name_desc[0].split(' ')[1]
            desc = name_desc[1].strip()
            
            if(desc.startswith('[') and desc.endswith(']')):
                if(self.has_escape_characters(desc)):
                    asciiCodes = self.get_list_ascii(desc)
                    regexAscii = self.convert_ascii(asciiCodes)
                    self.cleanDefiniciones[name] = regexAscii
                else:
                    if('-' in desc): 
                        ranges = self.get_ranges(desc)
                        regexRanges = self.convert_ranges(ranges)
                        self.cleanDefiniciones[name] = regexRanges
                    else:
                        desc = desc.replace('[', '').replace(']', '').replace('"', '')
                        newregex = ""
                        for ch in desc:
                            newregex += ch+'|'
                            
                        # Se elimina el último or que se agrega    
                        newregex = newregex[:-1]
                        self.cleanDefiniciones[name] = newregex
                                    
            else:
                
                self.cleanDefiniciones[name] = desc
                
        print()
        # Limpieza de rules
        cleanRules = []
        for j in self.rules:
            j = self.remove_comments(j)
            j = j.strip()
            cleanRules.append(j)

        self.rules = cleanRules
        self.rules.remove(self.rules[0])

        # Regex temporal basada en las reglas
        self.tempRegex = "".join(self.rules)

        # Impresion definiciones
        for key, value in self.cleanDefiniciones.items():
            print(key, value)
        print()
        print("Temp regex:",self.tempRegex)
        print()
        self.regexFinal = self.get_final_regex()
        print("Regex Final:", self.regexFinal)

    def remove_comments(self, line):
        if 'rule' in line:
            return line
        
        while '(*' in line:
            start = line.find('(*')
            end = line.find('*)', start) + 2
            line = line[:start] + line[end:]
            
        # Eliminar comillas y espacios en blanco
        line = line.replace(' ', '')
        line = line.replace("'", '')
        line = line.replace('"', '')
        
        # Eliminar las llaves y su contenido
        open_bracket = line.find('{')
        close_bracket = line.find('}')
        if open_bracket != -1 and close_bracket != -1:
            functionRule = line[open_bracket+1:close_bracket]
            self.dirtyFunctionsRules[line] = functionRule
            line = line[:open_bracket] + line[close_bracket+1:]
            
        return line
    
    def has_escape_characters(self, line):
        escape_chars = ['\\','\n', '\r', '\t', '\b', '\f', '\v', '\a']
        for i in escape_chars:
            if i in line:
                return True
        return False
    
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
    
    def convert_ascii(self, asciiCodes):
        regexAscii = ""
        for code in asciiCodes:
            regexAscii += str(code)+"|"
        
        # Se elimina el último or que se agrega    
        regexAscii = regexAscii[:-1]
        return f'({regexAscii})'
    
    def convert_ranges(self, ranges):
        regexRanges = ""
        newRanges = []
        # Se lee cada rango encontrado
        for i in ranges:
            elementsRange = []
            # Se obtienen los elementos entre cada límite del rango
            for j in range(i[0], i[1]+1):
                elementsRange.append(chr(j))
            newRanges.append(elementsRange)
        
        for rango in newRanges:    
            cadena = ""
            for chara in rango:
                cadena += chara+"|"
            regexRanges += cadena
        
        # Se elimina el último or que se agrega    
        regexRanges = regexRanges[:-1]
        
        return regexRanges
    
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
                listAscii.append(ord(line[i]))
                i += 1
                continue
            else:
                i += 1

        return listAscii

    def get_final_regex(self):
        final_regex = self.tempRegex
        definitions = list(self.cleanDefiniciones.keys())
        dictionaryDefs = self.cleanDefiniciones
        print()
        
        while(any(elem in final_regex for elem in definitions)):
            for token in definitions:
                if token in final_regex:
                    final_regex = final_regex.replace(token, dictionaryDefs[token])
                
        return final_regex

print()
print('-'*20)
yal = YalLector('./yamel-tests/slr-4.yal')
yal.read()
print('-'*20)
print()