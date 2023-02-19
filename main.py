# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

from automatas.AFN import afn

word = 'ab*(a|b)a*b*'
a = afn(word)
a.Thompson_Construction()

# t = True
# while(t):
#     word = input("Ingrese expresión: ")
#     if word == 'exit':
#         t = False
#     else:
#         a = Conversion(word)
#         print(a.infixToPostfix())