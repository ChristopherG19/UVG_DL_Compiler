# Universidad del Valle de Guatemala
# Facultad de Ingenieria
# Departamento de Ciencias de la Computacion
# Diseno de lenguajes
# Christopher Garcia 20541

from tools.definitionsScanner import *

def tokens_returns(symbol):
	if symbol == 'ws':
		return WHITESPACE
	if symbol == 'number':
		return NUMBER
	if symbol == '+':
		return PLUS
	if symbol == '*':
		return TIMES
	if symbol == '(':
		return LPAREN
	if symbol == ')':
		return RPAREN
