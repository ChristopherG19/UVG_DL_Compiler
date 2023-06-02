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
from tools.YALReader import *
import pickle
 
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

# word = '(a|b)*a(a|b)(a|b)'
# cadena = 'aabc'

nameFile = "slr-5"
yal = YalLector(f'./yalex-tests/{nameFile}.yal')
word, wordVerify, definitions = yal.read()

Obj = Conversion(word)
Obj2 = Conversion(wordVerify)
postfixExp = Obj.infixToPostfix()
postfixExpV2 = Obj2.infixToPostfix()
alphabet = Obj.get_alphabet()
alphabetV2 = Obj2.get_alphabet()
print("Alfabeto: ", alphabet)

newSim = Simbolo('#') 
newSim2 = Simbolo('.') 
newSim2.setType(True)
NPos = postfixExp.copy()
NPos.append(newSim)
NPos.append(newSim2)

print()
ls = [l.label if not l.isSpecialChar else repr(l.label) for l in NPos]
print("Postfix: ", "".join(ls))
print()

print("-----  AFD (Directo)  -----")
T = directConstruction(word, postfixExp, alphabet)
dfaD = T.buildDFA()
print(dfaD)
print()
dfaD.alphabet = alphabet
showGraphDFA(dfaD, "Directo")

#print("-----  AFD (Directo_V2)  -----")
T = directConstruction(wordVerify, postfixExpV2, alphabetV2)
dfaD_V2 = T.buildDFA()
dfaD_V2.alphabet = alphabet
showGraphDFA(dfaD_V2, "Directo_V2")

with open(f'./scanners_dfa/AFD_yal{nameFile[-1]}', 'wb') as f:
    pickle.dump(dfaD, f)
    pickle.dump(dfaD_V2, f)
    pickle.dump(definitions, f)

# --------------------------------------------------------------
# Mostrar arboles: Laboratorio C
# --------------------------------------------------------------
# nameFile = "slr-4"
# yal = YalLector(f'./yalex-tests/{nameFile}.yal')
# word = yal.read()

# Obj = Conversion(word)
# postfixExp = Obj.infixToPostfix()
# alphabet = Obj.get_alphabet()
# print("Alfabeto: ", alphabet)

# newSim = Simbolo('#') 
# newSim2 = Simbolo('.') 
# newSim2.setType(True)
# NPos = postfixExp.copy()
# NPos.append(newSim)
# NPos.append(newSim2)

# print()
# ls = [l.label if not l.isSpecialChar else repr(l.label) for l in NPos]
# print("Postfix: ", "".join(ls))
# print()

# T = Tree(NPos)
# T.generateTree()       
# T.print_final_Tree(f"tree_yal{nameFile[-1]}")

print()
