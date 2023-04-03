# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Clase Stack
from stack import Stack
from components import *

"""
    Clase Conversion

    Returns:
        String postfix: 
            Expresión postfix creada a partir de una expresión infix
"""
class Conversion(object):
    def __init__(self, expression):
        self.infix = expression
        self.precedencia = {'*': 3, '+': 3, '?': 3,'.': 2, '|': 1, '(': 0, ')': 0, '': 0}
        self.operators = ['*', '.', '|', '+', '?']
        self.HighestPrecedence = 5

    def infixToPostfix(self):
        infixNew = []
        postfixExp = []
        stack = Stack()
        CantElements = len(self.infix)

        # Se añade la concatenación explícita
        for index in range(CantElements):
            element = self.infix[index]
            infixNew.append(element) 
            if (element.label in '|(.'):
                continue
            if ((index+1) < len(self.infix)):
                if (((element.label in ')*+?') or (element.label not in '?+()*.|')) and 
                    (self.infix[index + 1].label not in '+*?|)')):
                    dotSym = Simbolo('.')
                    dotSym.setType(True)
                    infixNew.append(dotSym) 
        
        # Se ordena la expresión dependiendo de la precedencia de operadores
        for element in infixNew:
                
            if (element.isOperator and element.label == '('):
                stack.push(element)
                
            elif (element.isOperator and element.label == ')'):
                while (not stack.isEmpty() and stack.peek().label != '('):
                    postfixExp.append(stack.pop())
                stack.pop()
            
            elif (element.isOperator and element.label in self.operators):
                while (not stack.isEmpty()):
                    el = stack.peek()
                    precedenceActualEl = self.precedencia[element.label]
                    precedenceLastEl = self.precedencia[el.label]

                    if (precedenceLastEl >= precedenceActualEl):
                        postfixExp.append(stack.pop())
                    else:
                        break
                    
                stack.push(element)    
                    
            else:
                postfixExp.append(element)     
                    
        while (not stack.isEmpty()):
            postfixExp.append(stack.pop())
                           
        newSim = Simbolo('#') 
        newSim.setType(True)
        newSim2 = Simbolo('.') 
        newSim2.setType(True)
        postfixExp.append(newSim)
        postfixExp.append(newSim2)
        return postfixExp
    
    def get_alphabet(self, expression):
        # Obtención de alfabeto
        alphabet = []
        for symbol in expression:
            if(not symbol.isOperator and symbol.label not in '().*+|$?' and symbol.label not in alphabet):
                alphabet.append(symbol.label)
                
        return sorted(alphabet)
