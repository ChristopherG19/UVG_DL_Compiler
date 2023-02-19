# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

class Stack():
    # Constructor
    def __init__(self):
        self.stack = []
        
    # Retorna el tamaño del stack
    def size(self):
        return len(self.stack)
        
    # Retorna true o false dependiendo si está vacío el stack o no
    def isEmpty(self):
        return True if (self.size() == 0) else False
    
    # Obtiene el valor en el top del stack sin removerlo
    def peek(self):
        return self.stack[-1] if (not self.isEmpty()) else "No Elements" 
    
    # Obtiene el valor en el top del stack y lo remueve
    def pop(self):
        return self.stack.pop() if (not self.isEmpty()) else "No Elements" 
    
    # Agrega un elemento al stack
    def push(self, element):
        self.stack.append(element)
        
    # Limpia el stack
    def clear(self):
        self.stack = []
    
    # Obtiene un elemento del stack en base a su posición
    def getElement(self, i):
        return self.stack[i]
        
    # Imprime el contenido del stack
    def __str__(self):
        for i in self.stack:
            print(i)