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
from automatas.minimizacion import *

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
#             print("-----  AFN (Thompson) -----")
#             nfaCons = Construction(word, postfixExp, alphabet)
#             nfa = nfaCons.Thompson_Construction()
#             print(nfa)
#             print()

#             showGraphNFA(nfa, "Thompson")

#             print("-----  AFD (Subconjuntos) -----")
#             dfaSub = subconjuntos(nfa, alphabet, word, postfixExp)
#             dfaS = dfaSub.subconjuntos_construction()
#             print(dfaS)
#             print()

#             showGraphDFA(dfaS, "Subconjuntos")

#             print("-----  AFD (Directo)  -----")
#             T = directConstruction(word, postfixExp, alphabet)
#             dfaD = T.buildDFA()
#             print(dfaD)
#             print()

#             showGraphDFA(dfaD, "Directo")

#             print("-----  AFD Minimizado (Subconjuntos) -----")
#             miniS = Minimizador(dfaS, alphabet)
#             dfaMinS = miniS.minimize_afd()
#             print(dfaMinS)
#             print()

#             showGraphDFA(dfaMinS, "Minimizado_Subconjuntos")

#             print("-----  AFD Minimizado (Directo) -----")
#             miniD = Minimizador(dfaD, alphabet)
#             dfaMinD = miniD.minimize_afd()
#             print(dfaMinD)
#             print()

#             showGraphDFA(dfaMinD, "Minimizado_Directo")
            
#             cadena = input("Ingrese cadena: ")

#             nfaS = nfaSimulation(nfa, cadena)
#             print(f"(Thompson) Cadena ingresada: {cadena} | Resultado: {nfaS.Simulation()} es aceptada")

#             dfaSSim = dfaSimulation(dfaS, cadena)
#             print(f"(Subconjuntos) Cadena ingresada: {cadena} | Resultado: {dfaSSim.Simulation()} es aceptada")

#             dfaDSim = dfaSimulation(dfaD, cadena)
#             print(f"(Directo) Cadena ingresada: {cadena} | Resultado: {dfaDSim.Simulation()} es aceptada")

#             minDfaSSim = dfaSimulation(dfaMinS, cadena)
#             print(f"(SC minimizado) Cadena ingresada: {cadena} | Resultado: {minDfaSSim.Simulation()} es aceptada")

#             minDfaDSim = dfaSimulation(dfaMinD, cadena)
#             print(f"(D minimizado) Cadena ingresada: {cadena} | Resultado: {minDfaDSim.Simulation()} es aceptada")
            

''' Expresiones pruebas '''
# word = '(a*|b*)c' 
# word = '(b|b)*abb(a|b)*' 
# word = '(a|ε)b(a?)c?' 
# word = '(a|b)*a(a|b)(a|b)' 
# word = 'b*ab?' 
# word = 'b+abc+' 
# word = 'ab*ab*' 
# word = '0(0|1)*0' 
# word = '((ε|0)1*)*' 
# word = '(0|1)*0(0|1)(0|1)' 
# word = '(0*0)*(1*1)*' 
# word = '(0|1)1*(0|1)' 
# word = '0?(1|ε)?0*' 
# word = '((1?)*)*' 
# word = '(01)*(10)*' 

''' Expresiones prelaboratorio '''
# word = 'ab*ab*' 
# word = '0?(1?)?0*' 
# word = '(a*|b*)c' 
# word = '(b|b)*abb(a|b)*' 
# word = '(a|ε)b(a+)c?' 
# word = '(a|b)*a(a|b)(a|b)' 

word = 'a(a|b|c)bc'
cadena = 'aabc'

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

showGraphNFA(nfa, "Thompson")

print("-----  AFD (Subconjuntos) -----")
dfaSub = subconjuntos(nfa, alphabet, word, postfixExp)
dfaS = dfaSub.subconjuntos_construction()
print(dfaS)
print()

showGraphDFA(dfaS, "Subconjuntos")

print("-----  AFD (Directo)  -----")
T = directConstruction(word, postfixExp, alphabet)
dfaD = T.buildDFA()
print(dfaD)
print()

showGraphDFA(dfaD, "Directo")

print("-----  AFD Minimizado (Subconjuntos) -----")
miniS = Minimizador(dfaS, alphabet)
dfaMinS = miniS.minimize_afd()
print(dfaMinS)
print()

showGraphDFA(dfaMinS, "Minimizado_Subconjuntos")

print("-----  AFD Minimizado (Directo) -----")
miniD = Minimizador(dfaD, alphabet)
dfaMinD = miniD.minimize_afd()
print(dfaMinD)
print()

showGraphDFA(dfaMinD, "Minimizado_Directo")

nfaS = nfaSimulation(nfa, cadena)
print(f"(Thompson) Cadena ingresada: {cadena} | Resultado: {nfaS.Simulation()} es aceptada")

dfaSSim = dfaSimulation(dfaS, cadena)
print(f"(Subconjuntos) Cadena ingresada: {cadena} | Resultado: {dfaSSim.Simulation()} es aceptada")

dfaDSim = dfaSimulation(dfaD, cadena)
print(f"(Directo) Cadena ingresada: {cadena} | Resultado: {dfaDSim.Simulation()} es aceptada")

minDfaSSim = dfaSimulation(dfaMinS, cadena)
print(f"(SC minimizado) Cadena ingresada: {cadena} | Resultado: {minDfaSSim.Simulation()} es aceptada")

minDfaDSim = dfaSimulation(dfaMinD, cadena)
print(f"(D minimizado) Cadena ingresada: {cadena} | Resultado: {minDfaDSim.Simulation()} es aceptada")

print()
