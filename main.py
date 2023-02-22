# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from automatas.AFN import *
from tools.showGraph import showGraph

# a(a|b)*b

#a*
#a**
#(a|b)*
#(a|b)
# '(a*|b)*' # aaaaabbbbb
# word = '(a|b)*a(a|b)*(a|b)'
word = '(a|b)*ab*(a|b)*(a|b)a+a?'
cons = Construction(word)
nfa = cons.Thompson_Construction()
print(nfa)
showGraph(nfa)

# self.numStates = numStates        
# self.states = states
# self.initialState = InState
# self.finalState = FnState
# self.transitions = transitions

# self.inState = inState
# self.symbol = symbol
# self.fnState = fnState

# t = True
# while(t):
#     word = input("Ingrese expresión: ")
#     if word == 'exit':
#         t = False
#     else:
#         a = Conversion(word)
#         print(a.infixToPostfix())