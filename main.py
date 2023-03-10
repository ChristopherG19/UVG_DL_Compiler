# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from automatas.AFN import *
from tools.showGraph import showGraph
from tools.verification import Verification

# a(a|b)*b

#a*
#a**
#(a|b)*
#(a|b)
#(a*|b)* 
#(a|b)*a(a|b)*(a|b)
#(a|b)*ab*(a|b)*(a|b)a+a?
#|a||a||

t = True
print()
while(t):
    word = input("Ingrese expresión: ")
    if word == 'exit':
        t = False
        print()
    else:
        print("\nExpresión ingresada: "+word)
        veri = Verification(word).Comprobacion()

        errores = 0
        for regla in veri:
            if(not regla[0]):
                errores += 1
            
        if (errores > 0):
            print("Tienes los siguientes errores: \n")
            for regla in veri:
                if(not regla[0]):
                    if (regla[3] == 'A'):
                        print('-> ',regla[1])
                        print("Revisar paréntesis de cierre o apertura de las siguientes posiciones: ", ",".join(str(x) for x in regla[2]))
                        print()
                    elif (regla[3] == 'B'):
                        print('-> ',regla[1])
                        if(type(regla[2]) == list):
                            print("Revisar or's en las siguientes posiciones: ", ",".join(str(x) for x in regla[2]))
                        else:
                            print("Revisar or's en la expresion ingresada: ", regla[2])
                        print()
                    elif (regla[3] == 'C'):
                        print('-> ',regla[1])
                        print("Revisar expresión ingresada: ", regla[2])
                        print()
                    elif (regla[3] == 'D'):
                        print('-> ',regla[1])
                        print("Revisar expresión ingresada en la posición: ",",".join(str(x) for x in regla[2]))
                        print()
            SystemExit()
        else:
            cons = Construction(word)
            nfa = cons.Thompson_Construction()
            print(nfa)
            showGraph(nfa)
            print()
        