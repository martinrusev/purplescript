"""
    purplescript.parser
    ~~~~~~~~~~~~
    :copyright: (c) 2011 by Martin Rusev.
    :license: BSD, see LICENSE for more details.
"""
from ply import yacc
from lexer import Lexer

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


	def p_class_declaration_statement(self, p):
		'class_declaration_statement : CLASS VARIABLE ENDCLASS'
		p[0] = p[1]
		
	def p_empty(self, p):
		'empty : '

	def p_error(self, p):
		import sys
		sys.stderr.write("Syntax error at '%s' on line %s.\n" % (p.value, p.lineno))

if __name__== '__main__' : 
	parser = Parser()
	file = open('syntax/class.txt', 'r')
	data = file.read()
	result = parser.parse(code=data)
	print result

