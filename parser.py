"""
    purplescript.parser
    ~~~~~~~~~~~~
    :copyright: (c) 2011 by Martin Rusev.
    :license: BSD, see LICENSE for more details.
"""
from ply import yacc
from purplescript.lexer import Lexer
import purplescript.ast as ast

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
		'''top_statement : class_declaration 
						 | function_declaration                
						 | variable
						 | constant
						 '''
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
						   | function_declaration
						   | variable_list 
						   | variable_list ASSIGNMENT variable_list '''
		if len(p) == 4:
			try: 
				assign = p[1][-1]
				assign.type = 'assign'
			except:
				pass
			p[0] = p[1] + [p[3]]
		else:
			p[0] = p[1]

	def p_statement_block(self, p):
		'statement : LBRACE inner_statement_list RBRACE'
		p[0] = ast.Block(p[2])	
	
	def p_this(self, p):
		'this : THIS'
		p[0] = ast.This()
	
	def p_string(self, p):
		'string : STRING'
		p[0] = p[1]

	def p_constant(self, p):
		''' constant : CONSTANT 
					 | CONSTANT ASSIGNMENT string '''
		p[0] = ast.Constant(p[1], p[3])


	def p_variable_list(self, p):
		'''variable_list : variable_list variable
						 | variable
						 | this
					     | empty '''
		if len(p) == 3:
			p[0] = p[1] + [p[2]]
		else:
			p[0] = [p[1]]
	
	def p_variable(self, p):
		'''variable : VARIABLE
					| VARIABLE DOT '''
		if len(p) == 3:
			p[0] = ast.Variable(p[1], None, None, 'dot')
		else:
			p[0] = ast.Variable(p[1], None, None, None)
	
	
	def p_parameter(self, p):
		'''parameter : variable
					 | variable ASSIGNMENT string
					 | string '''

		if len(p) == 4:
			p[0] = ast.Parameter(p[1], p[3], None)
		else:
			p[0] = ast.Parameter(p[1], None, None)

	def p_parameter_list(self, p):
		'''parameter_list : parameter_list COMMA parameter
						  | parameter 
						  | empty '''
		if len(p) == 4:
			p[0] = p[1] +  [p[3]]
		else:
			p[0] = [p[1]]
	
	def p_function_declaration(self, p):
		'''function_declaration : LPAREN parameter_list RPAREN
								| DEF variable LPAREN parameter_list RPAREN inner_statement_list END'''
		if len(p) == 4:
			try:
				last = p[2][-1]
				last.position = 'last'
			except:
				pass
			p[0] = ast.InlineFunction(p[2])
		else:
			try:
				last = p[4][-1]
				last.position = 'last'
			except:
				pass
			
			p[0] = ast.Function(p[2], p[4], p[6])
		
	
	def p_class_declaration(self, p):
		'class_declaration : CLASS variable inner_statement_list ENDCLASS '
		p[0] = ast.Class(p[2], p[3])
		
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
	file = open('syntax/class.purple', 'r')
	data = file.read()
	result = parser.parse(code=data)

	for r in result:
		print r
