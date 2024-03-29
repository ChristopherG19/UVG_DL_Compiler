# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# Facultad de Ingenieria
# Departamento de Ciencias de la Computacion
# Diseno de lenguajes
# Christopher Garcia 20541

import pickle
from tools.definitionsScanner import *

tokens = []
with open('tokens/tokens_yal5', 'rb') as f:
	tokens = pickle.load(f)

def tokens_returns(symbol):
	if symbol == 'characters':
		return CHARACTERS
	if symbol == 'ws':
		return WHITESPACE
	if symbol == 'minusword':
		return WORDMIN
	if symbol == 'mayusword':
		return WORDMAY
	if symbol == '/*':
		return LEFTCOMMENT
	if symbol == '→':
		return ARROW
	if symbol == '*/':
		return RIGHTCOMMENT
	if symbol == '%token':
		return TOKEN
	if symbol == '|':
		return OR
	if symbol == 'IGNORE':
		return IGNORE
	if symbol == '%%':
		return SPLIT
	if symbol == ':':
		return TWOPOINTS
	if symbol == ';':
		return FINISHDECLARATION

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


