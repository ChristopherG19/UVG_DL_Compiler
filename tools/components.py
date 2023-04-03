# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Clase Simbolo: Representa cada simbolo del autómata
class Simbolo():
    def __init__(self, symbol):
        self.label = symbol
        self.isOperator = False
        self.isSpecialChar = False
    
    def setType(self, isOperator):
        self.isOperator = isOperator
        
    def setSpecialType(self, isSpecial):
        self.isSpecialChar = isSpecial

    def __str__(self):
        if(self.isSpecialChar):
            return repr(self.label).replace("'", "")
        
        return self.label
    
    def __repr__(self):
        return str(self)
        # return f"{self.label},{1 if self.isOperator else 0},{1 if self.isSpecialChar else 0} "

# Clase Estado: Representa cada estado del autómata
class Estado():
    def __init__(self, stateNum):
        self.stateNum = stateNum
        
    def __str__(self):
        return f"q{self.stateNum}"
    
    def __repr__(self):
        return str(self)

# Clase Transición: Representa las transiciones del autómata
class Transition():
    def __init__(self, inState, symbol, fnState):
        self.inState = inState
        self.symbol = symbol
        self.fnState = fnState
        
    def __str__(self):
        return f"{self.inState}-{self.symbol}-{self.fnState}"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        if isinstance(other, Transition):
            return self.inState == other.inState and self.symbol == other.symbol and self.fnState == other.fnState
        return False
    
class Definition():
    def __init__(self, name, desc, func=None):
        self.name = name
        self.desc = desc
        self.func = func

    def __str__(self) -> str:
        return f"{self.name}: {self.desc}"

    def __repr__(self):
        return str(self)
    
    def lintDesc(self):
        if self.desc == None:
            valDesc = "Sin descripcion" 
        else:
            if any(s.isSpecialChar == True for s in self.desc):
                tempLD = []
                for i in self.desc:
                    if i.isSpecialChar:
                        tempLD.append(repr(i.label).replace("'", ""))
                    else:
                        tempLD.append(i.label.replace("'", ""))
                valDesc = ''.join(tempLD)
            else:
                tempLD = [s.label for s in self.desc]
                valDesc = ''.join(tempLD)
        
        #valDesc2 = "Sin Desc" if self.desc is None else self.desc
        valFunc = "Sin funcion" if self.func is None else self.func
        
        return f"\t-> Token: {self.name}\n\t   Desc: {valDesc}\n\t   Funcion: {valFunc}"
    
    def __eq__(self, other):
        if isinstance(other, Definition):
            return self.name == other.name
        return False    

# Se crea un alfabeto para nombrar estados posteriormente           
def listAlphabet():
    a = list(map(chr, range(97, 123)))
    new = []
    for i in a:
        new.append(i.upper())
    new.reverse()
    return new
    