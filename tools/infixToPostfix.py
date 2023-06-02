# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Clase Stack
from tools.stack import Stack
from tools.components import *

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
        
        newInfix = []
        if(type(self.infix) == str):
            for i in self.infix:
                newSym = Simbolo(i)
                if i in self.operators or i in '()':
                    newSym.setType(True)
                newInfix.append(newSym)
            self.infix = newInfix
        
        infixNew = []
        postfixExp = []
        stack = Stack()
        CantElements = len(self.infix)

        # Se añade la concatenación explícita
        for index in range(CantElements):
            element = self.infix[index]
            infixNew.append(element) 
            if ((index+1) < len(self.infix)):
                if (element.isOperator):
                    if(element.label in '*+?)'):
                        if(not self.infix[index + 1].isOperator or self.infix[index + 1].label == '('):
                            dotSym = Simbolo('.')
                            dotSym.setType(True)
                            infixNew.append(dotSym) 
                elif (not element.isOperator):
                    if(not self.infix[index + 1].isOperator):
                        dotSym = Simbolo('.')
                        dotSym.setType(True)
                        infixNew.append(dotSym) 
                    elif(self.infix[index + 1].label == '('):
                        dotSym = Simbolo('.')
                        dotSym.setType(True)
                        infixNew.append(dotSym) 
                    elif(self.infix[index + 1].label == 'ε'):
                        dotSym = Simbolo('.')
                        dotSym.setType(True)
                        infixNew.append(dotSym) 
        
        print()
        ls = [l.label if not l.isSpecialChar else repr(l.label) for l in infixNew]
        print("Regex final infix Concatenaciones: ", "".join(ls))
        print()
        
        # Se ordena la expresión dependiendo de la precedencia de operadores
        for element in infixNew:
            #print(element, element.isOperator)
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
                           
        return postfixExp
    
    def get_alphabet(self):
        # Obtención de alfabeto
        alphabet = []
        for symbol in self.infix:
            if(not symbol.isOperator and symbol.label not in alphabet):
                alphabet.append(symbol.label)
                
        return sorted(alphabet)
