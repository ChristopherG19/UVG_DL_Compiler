# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Clase Stack
from tools.stack import Stack

"""
    Clase Conversion

    Returns:
        String postfix: 
            Expresión postfix creada a partir de una expresión infix
"""
class Conversion(object):
    def __init__(self, expression):
        self.infix = expression
        self.precedencia = {'*': 3, '.': 2, '|': 1, '(': 0, ')': 0, '': 0}
        self.operators = ['*', '.', '|']
        self.HighestPrecedence = 5

    def infixToPostfix(self):
        infixNew = ""
        postfixExp = ""
        stack = Stack()
        CantElements = len(self.infix)

        # Se añade la concatenación explícita
        for index in range(CantElements):
            element = self.infix[index]
            infixNew += element 
            try:
                if (element in '|(.'):
                    continue
                elif (((element in ')*') or (element not in '()*.|')) and (self.infix[index + 1] not in '*|)')):
                    infixNew += '.'
            except:
                pass
        
        # Se ordena la expresión dependiendo de la precedencia de operadores
        for element in infixNew:
            if (element == '('):
                stack.push(element)
                
            elif (element == ')'):
                while (not stack.isEmpty() and stack.peek() != '('):
                    postfixExp += stack.pop()
                stack.pop()
            
            elif (element in self.operators):
                while (not stack.isEmpty()):
                    el = stack.peek()
                    precedenceActualEl = self.precedencia[element]
                    precedenceLastEl = self.precedencia[el]

                    if (precedenceLastEl >= precedenceActualEl):
                        postfixExp += stack.pop()
                    else:
                        break
                    
                stack.push(element)    
                    
            else:
                postfixExp += element       
                    
        while (not stack.isEmpty()):
            postfixExp += stack.pop()
                    
        return postfixExp
