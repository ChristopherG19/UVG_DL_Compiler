# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from tools.node import *

class Tree():
    def __init__(self, postfixExp):
        self.postfixExp = postfixExp

    def generateTree(self):
        stackNodes = []
        
        numPos = 1
        
        for symbol in self.postfixExp:
            if (symbol not in '.|*+?'):
                newNode = node(symbol, number=numPos)
                stackNodes.append(newNode)
                numPos += 1
            else:
                if (symbol in '*?+'):
                    leftNewNode = stackNodes.pop()
                    newNode = node(symbol, leftNewNode)
                    stackNodes.append(newNode)
                else:
                    rightNewNode = stackNodes.pop()
                    leftNewNode = stackNodes.pop()
                    newNode = node(symbol, leftNewNode, rightNewNode)
                    stackNodes.append(newNode)

        return stackNodes.pop()
                    
    def printTree(self, tree):
        for node in tree:
            print(node)
                    
            
        
        
    