# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from automatas.AFN import *
from automatas.subconjuntos import *
from tools.showGraph import *
from tools.verification import Verification
from simulation.nfaSimulation import *
from simulation.dfaSimulation import *
from automatas.construccionDirecta import *

# a(a|b)*b

#a*
#a**
#(a|b)*
#(a|b)
#(a*|b)* 
#(a|b)*a(a|b)*(a|b)
#(a|b)*ab*(a|b)*(a|b)a+a?
#|a||a||

# t = True
# print()
# while(t):
#     word = input("Ingrese expresión: ")
#     if word == 'exit':
#         t = False
#         print()
#     else:
#         print("\nExpresión ingresada: "+word)
        
#         # Se realiza la evaluación de la expresión
#         veri = Verification(word).Comprobacion()
#         errores = 0
#         for regla in veri:
#             if(not regla[0]):
#                 errores += 1
            
#         if (errores > 0):
#             print("Tienes los siguientes errores: \n")
#             for regla in veri:
#                 if(not regla[0]):
#                     if (regla[3] == 'A'):
#                         print('-> ',regla[1])
#                         print("Revisar paréntesis de cierre o apertura de las siguientes posiciones: ", ",".join(str(x) for x in regla[2]))
#                         print()
#                     elif (regla[3] == 'B'):
#                         print('-> ',regla[1])
#                         if(type(regla[2]) == list):
#                             print("Revisar or's en las siguientes posiciones: ", ",".join(str(x) for x in regla[2]))
#                         else:
#                             print("Revisar or's en la expresion ingresada: ", regla[2])
#                         print()
#                     elif (regla[3] == 'C'):
#                         print('-> ',regla[1])
#                         print("Revisar expresión ingresada: ", regla[2])
#                         print()
#                     elif (regla[3] == 'D'):
#                         print('-> ',regla[1])
#                         print("Revisar expresión ingresada en la posición: ",",".join(str(x) for x in regla[2]))
#                         print()
#             SystemExit()
#         else:
#             #Se obtiene la expresión en postfix y el alfabeto
#             Obj = Conversion(word)
#             postfixExp = Obj.infixToPostfix()
#             alphabet = Obj.get_alphabet(word)
#             print("Infix: ", word)
#             print("Postfix: ", postfixExp)
#             print("Alfabeto: ", alphabet)
#             print()
            
#             # Inicio de creación de autómatas
#             print("-----  AFN  -----")
#             nfaCons = Construction(word, postfixExp, alphabet)
#             nfa = nfaCons.Thompson_Construction()
#             print(nfa)
#             print()
            
#             print("-----  AFD (Subconjuntos)  -----")
#             dfaSub = subconjuntos(nfa, alphabet, word, postfixExp)
#             dfa = dfaSub.subconjuntos_construction()
#             print(dfa)
#             print()
            
#             # Se crean las imágenes de los autómatas
#             showGraphNFA(nfa, "Thompson")
#             showGraphDFA(dfa, "Subconjuntos")
            
#Se obtiene la expresión en postfix y el alfabeto
word = '(a*|b*)c'
# word = '(b|b)*abb(a|b)*'
Obj = Conversion(word)
postfixExp = Obj.infixToPostfix()
alphabet = Obj.get_alphabet(word)
print("Infix: ", word)
print("Postfix: ", postfixExp)
print("Alfabeto: ", alphabet)
print()

print("-----  AFN (Thompson) -----")
nfaCons = Construction(word, postfixExp, alphabet)
nfa = nfaCons.Thompson_Construction()
print(nfa)
print()
print("-----  AFD (Subconjuntos) -----")
dfaSub = subconjuntos(nfa, alphabet, word, postfixExp)
dfaS = dfaSub.subconjuntos_construction()
print(dfaS)
print()
print("-----  AFD (Directo)  -----")
T = directConstruction(word, postfixExp, alphabet)
dfaD = T.buildDFA()
print(dfaD)
print()

prueba = 'c'

nfaS = nfaSimulation(nfa, prueba)
print(f"(Thompson) Cadena ingresada: {prueba} | Resultado: {nfaS.Simulation()} es aceptada")

dfaSim = dfaSimulation(dfaS, prueba)
print(f"(Subconjuntos) Cadena ingresada: {prueba} | Resultado: {dfaSim.Simulation()} es aceptada")

dfaDir = dfaSimulation(dfaD, prueba)
print(f"(Directo) Cadena ingresada: {prueba} | Resultado: {dfaDir.Simulation()} es aceptada")

print()

showGraphNFA(nfa, "Thompson")
showGraphDFA(dfaS, "Subconjuntos")
showGraphDFA(dfaD, "Directo")
