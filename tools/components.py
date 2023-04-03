# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Clase Simbolo: Representa cada simbolo del autómata
class Simbolo():
    def __init__(self, symbol, tipo):
        self.symbol = symbol
        self.type = tipo
    
    def __str__(self):
        return self.symbol
    
    def __repr__(self):
        return str(self)

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
    
# Se crea un alfabeto para nombrar estados posteriormente           
def listAlphabet():
    a = list(map(chr, range(97, 123)))
    new = []
    for i in a:
        new.append(i.upper())
    new.reverse()
    return new
    