"""
    purplescript.parser
    ~~~~~~~~~~~~
    :copyright: (c) 2011 by Martin Rusev.
    :license: BSD, see LICENSE for more details.
"""
from ply import yacc
from lexer import Lexer
from ast import *
import itertools


class Parser(object):
	
	def __init__(self):
		self.lexer = Lexer()
		self.tokens = self.lexer.tokens
		self.parser = yacc.yacc(module=self, debug=2)

	def parse(self, code):
		return self.parser.parse(code, lexer=self.lexer)


	def p_start(self, p):
		'start : top_statement_list'
		p[0] = p[1]

	def p_top_statement_list(self, p):
		'''top_statement_list : top_statement_list top_statement
							  | empty'''
		if len(p) == 3:
			p[0] = p[1] + [p[2]]
		else:
			p[0] = []

	
	def p_top_statement(self, p):
		'''top_statement : class_declaration_statement '''
		if len(p) == 2:
			p[0] = p[1]
		else:
			pass
	
	
	def p_inner_statement_list(self, p):
		'''inner_statement_list : inner_statement_list inner_statement
								| empty'''
		if len(p) == 3:
			p[0] = p[1] + [p[2]]
		else:
			p[0] = []

	def p_inner_statement(self, p):
		'''inner_statement : statement
						   | function_declaration_statement
						   | class_declaration_statement '''
		p[0] = p[1]


	def p_statement_block(self, p):
		'statement : LBRACE inner_statement_list RBRACE'
		p[0] = Block(p[2])	


	def p_variable(self, p):
		'variable : VARIABLE'
		p[0] = p[1]
	
	
	def p_parameter(self, p):
		'''parameter : VARIABLE '''
		p[0] = p[1]

	def p_parameter_list(self, p):
		'''parameter_list : parameter_list COMMA parameter
						  | parameter 
						  | empty '''
		if len(p) == 4:
			p[0] = [p[1]]  + [p[3]]
		else:
			p[0] = p[1]
	
	def p_function_declaration_statement(self, p):
		'function_declaration_statement : DEF variable LPAREN parameter_list RPAREN inner_statement_list END'
		p[0] = Function(p[2], p[4], p[5])
	
	
	def p_class_declaration_statement(self, p):
		'class_declaration_statement : CLASS variable inner_statement_list ENDCLASS '
		p[0] = Class(p[2], p[3])
		
	def p_empty(self, p):
		'empty : '

	def p_error(self, t):
		import sys
		try:
			sys.stderr.write("Syntax error at '%s' on line %s.\n" % (t.value, t.lineno))
		except:
			pass

if __name__== '__main__' : 
	parser = Parser()
	file = open('syntax/class.txt', 'r')
	data = file.read()
	result = parser.parse(code=data)

	for r in result:
		print r
