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
            
        print()
            
        #Limpiar definiciones
        for defin in self.definiciones:
            nombre_desc = defin.split('=')
            name = nombre_desc[0].split(' ')[1]
            if(type(nombre_desc[1]) == str):
                print(nombre_desc)

        print()
        
        cleanRules = []
        for j in self.rules:
            j = self.remove_comments(j)
            j = j.strip()
            cleanRules.append(j)

        self.rules = cleanRules
        self.rules.remove(self.rules[0])

        self.tempRegex = "".join(self.rules)

        print("Temp regex:",self.tempRegex)

    def remove_comments(self, line):
        
        if 'rule' in line:
            return line
        
        while '(*' in line:
            start = line.find('(*')
            end = line.find('*)', start) + 2
            line = line[:start] + line[end:]
            
        line = line.replace(' ', '')
        line = line.replace("'", '')
        line = line.replace('"', '')
        
        # Eliminar las llaves y su contenido
        open_bracket = line.find('{')
        close_bracket = line.find('}')
        if open_bracket != -1 and close_bracket != -1:
            line = line[:open_bracket] + line[close_bracket+1:]
            
        return line

yal = YalLector('./yamel-tests/slr-1.yal')
yal.read()