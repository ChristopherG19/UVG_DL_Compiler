# Universidad del Valle de Guatemala
# Facultad de Ingenieria
# Departamento de Ciencias de la Computacion
# Diseno de lenguajes
# Christopher Garcia 20541

from tools.definitionsScanner import *

def tokens_returns(symbol):
	if symbol == 'id':
		return ID
	if symbol == 'number':
		return NUMBER
	if symbol == ';':
		return SEMICOLON
	if symbol == ':=':
		return ASSIGNOP
	if symbol == '<':
		return LT
	if symbol == '=':
		return EQ
	if symbol == '+':
		return PLUS
	if symbol == '-':
		return MINUS
	if symbol == '*':
		return TIMES
	if symbol == '/':
		return DIV
	if symbol == '(':
		return LPAREN
	if symbol == ')':
		return RPAREN
