# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

class node():
    def __init__(self, symbol, leftC=None, rightC=None, number=None):
        self.symbol = symbol
        self.number = number
        self.leftChild = leftC
        self.rightChild = rightC
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = set()
        self.elements = []
        self.nullable = False
        
    def calculate_positions(self):
        if self.symbol not in ".|*+?":
            if self.symbol == 'ε':
                self.nullable = True
            else:
                self.firstpos.add(self)
                self.lastpos.add(self)
                self.nullable = False
        else:
            if self.symbol in "*+?":
                self.leftChild.calculate_positions()
                self.firstpos.update(self.leftChild.firstpos)
                self.lastpos.update(self.leftChild.lastpos)
                self.nullable = True
                  
            elif self.symbol == "|":
                self.leftChild.calculate_positions()
                self.rightChild.calculate_positions()
                
                self.nullable = self.leftChild.nullable or self.rightChild.nullable
                
                self.firstpos.update(self.leftChild.firstpos)
                self.firstpos.update(self.rightChild.firstpos)
                self.lastpos.update(self.leftChild.lastpos)
                self.lastpos.update(self.rightChild.lastpos)
                
            elif self.symbol == ".":
                self.leftChild.calculate_positions()
                self.rightChild.calculate_positions()
                
                self.nullable = self.leftChild.nullable and self.rightChild.nullable
                
                self.firstpos.update(self.leftChild.firstpos)
                if self.leftChild.nullable:
                    self.firstpos.update(self.leftChild.firstpos)
                    self.firstpos.update(self.rightChild.firstpos)
                else: 
                    self.firstpos.update(self.leftChild.firstpos)
                    
                if self.rightChild.nullable:
                    self.lastpos.update(self.leftChild.lastpos)
                    self.lastpos.update(self.rightChild.lastpos)
                else:
                    self.lastpos.update(self.rightChild.lastpos)
                
        self.calculate_followpos()

    def calculate_followpos(self):
        if self.symbol == ".":
            for position in self.leftChild.lastpos:
                position.followpos.update(self.rightChild.firstpos)
                
        elif self.symbol == "*":
            for position in self.leftChild.lastpos:
                position.followpos.update(self.leftChild.firstpos)
                
        elif self.symbol == "ε":
            pass
    
    def traverse_tree(self, node):
        firstP = [n.number for n in node.firstpos]
        lastP = [n.number for n in node.lastpos]
        followP = [n.number for n in node.followpos]
        self.elements.append([node.symbol, firstP, lastP, followP, node.number])
            
        if node.leftChild is not None:
            self.traverse_tree(node.leftChild)
        if node.rightChild is not None:
            self.traverse_tree(node.rightChild)

        return self.elements

    def __str__(self):
        result = f"\nSymbol: {self.symbol}\n"
        result += f"Firstpos: {[pos.number for pos in self.firstpos]}\n"
        result += f"Lastpos: {[pos.number for pos in self.lastpos]}\n"
        result += f"Followpos: {[pos.number for pos in self.followpos]}\n"
        if self.leftChild:
            result += f"Left child: {self.leftChild}\n"
        if self.rightChild:
            result += f"Right child: {self.rightChild}\n"
        return result
