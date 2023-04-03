# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Clase Stack
from stack import Stack

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
        infixNew = ""
        infixNewV2 = ""
        postfixExp = ""
        stack = Stack()
        CantElements = len(self.infix)
        inside_quotes = False
        
        # Se verifican números compuestos
        index = 0
        while index < CantElements:
            element = self.infix[index]
            if element.isdigit():
                # Si es un dígito, leemos el número compuesto completo
                num_compuesto = element
                while index + 1 < CantElements and self.infix[index+1].isdigit():
                    num_compuesto += self.infix[index+1]
                    index += 1
                if(len(num_compuesto) > 1):
                    infixNewV2 += f"'{num_compuesto}'"
                else:
                    infixNewV2 += num_compuesto
            else:
                infixNewV2 += element 
            index += 1

        print("Regex final considerando números compuestos:")
        print(infixNewV2)
        print()

        CantElementsNew = len(infixNewV2)
        # Se añade la concatenación explícita
        for index in range(CantElementsNew):
            element = infixNewV2[index]
            infixNew += element 
            if (element == "'"):
                inside_quotes = not inside_quotes
            if (element in '|(.'):
                continue
            if ((index+1) < len(infixNewV2)):
                if (not inside_quotes and
                    ((element in ')*+?') or (element not in '?+()*.|')) and 
                    (infixNewV2[index + 1] not in '+*?|)')):
                    infixNew += '.'
        
        # Primero transformar a números compuestos 
        # y de alguna manera agregar la concatenación explícita tomando en cuenta comillas
                
        # countNumCom = 0

        # Se ordena la expresión dependiendo de la precedencia de operadores
        for element in infixNew:
                
            if (element == '('):
                stack.push(element)
                
            elif (element == ')'):
                while (not stack.isEmpty() and stack.peek() != '('):
                    postfixExp += stack.pop()
                stack.pop()
                
            # elif (element == "'"):
            #     countNumCom += 1
            #     print(element, countNumCom)
            #     stack.push(element)
            #     if (countNumCom == 2):
            #         while(not stack.isEmpty() and stack.peek() != '('):
            #             postfixExp += stack.pop()
            #         stack.pop()
            
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
    
    def get_alphabet(self, expression):
        # Obtención de alfabeto
        alphabet = []
        for i in expression:
            if(i not in '().*+|$?' and i not in alphabet):
                alphabet.append(i)
                
        return sorted(alphabet)
