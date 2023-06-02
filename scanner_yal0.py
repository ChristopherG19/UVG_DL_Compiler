# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# Facultad de Ingenieria
# Departamento de Ciencias de la Computacion
# Diseno de lenguajes
# Christopher Garcia 20541

import pickle
from tools.definitionsScanner import *

tokens = []
with open('tokens/tokens_yal0', 'rb') as f:
	tokens = pickle.load(f)

def tokens_returns(symbol):
	if symbol == 'ws':
		return NONE
	if symbol == 'id':
		if t.value = 0: return ID else: return NONE
	if symbol == '+':
		return PLUS
	if symbol == '*':
		return TIMES
	if symbol == '(':
		return LPAREN
	if symbol == ')':
		return RPAREN
	if symbol == '*)':
		return STARTCOMMENT

	return symbol

for token in tokens:
	if(token[1] == 'Error'):
		print(f'-> Valor: {token[0]} | Token: Error lexico')
	else:
		temp = ''
		if '\n' in token[0] or token[0] == ' ' or token[0] == '':
			temp = repr(token[0])
		else:
			temp = token[0]
		print(f'-> Valor: {temp} | Token: {tokens_returns(token[1])}')


