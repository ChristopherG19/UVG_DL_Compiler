# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Clase Stack
from tools.stack import Stack
from tools.infixToPostfix import Conversion

class afn:
    def __init__(self, expression):
        self.expression = expression
        self.epsilon = "ε"
        self.states = set()
        self.symbols = []
        self.transitions = []
        self.numEstados = []
        
        # Obtención de simbolos
        for i in self.expression:
            if(i not in '().*+|$?' and i not in self.symbols):
                self.symbols.append(i)
        self.symbols = sorted(self.symbols)
        
        #Se obtiene la expresión en postfix
        self.Obj = Conversion(self.expression)
        self.postfixExp = self.Obj.infixToPostfix()
                
    def Thompson_Construction(self):
        0
        
        
    def symbol(self):
        0
        
    def concat(self):
        0
        
    def kleene(self):
        0
        
    def union(self):
        0        
        
        
        
        