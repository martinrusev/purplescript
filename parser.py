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
						   | inline_function_declaration
						   | variable_list 
						   | expr
						   '''
		p[0] = p[1]

	def p_assignment(self,p):
		'statement : ASSIGNMENT'
		p[0] = ast.Assignment()

	def p_array_key_reference(self, p):
		''' statement : LBRACKET string RBRACKET '''
		p[0] = ast.ArrayKeyReference(p[2])
	
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

	def p_inline_function_declaration(self, p):
		''' inline_function_declaration : LPAREN parameter_list RPAREN '''
		try:
			last = p[2][-1]
			last.position = 'last'
		except:
			pass
		p[0] = ast.InlineFunction(p[2])
	
	def p_function_declaration(self, p):
		'''function_declaration : DEF variable inline_function_declaration inner_statement_list END'''
		try:
			last = p[4][-1]
			last.position = 'last'
		except:
			pass
		p[0] = ast.Function(p[2], p[3], p[4])
		
	
	def p_class_declaration(self, p):
		'class_declaration : CLASS variable inner_statement_list ENDCLASS '
		p[0] = ast.Class(p[2], p[3])
		

	def p_array_param(self, p):
		''' array_param : string
						| string COLON variable_list
						| string COLON variable_list inline_function_declaration '''
		if len(p) == 4:
			p[0] = ast.ArrayElement(p[1], p[3], None)
		elif len(p) == 5:
			p[3].append(p[4])
			p[0] = ast.ArrayElement(p[1], p[3], None)
		else:
			p[0] = p[1]


	def p_array_param_list(self, p):
		''' array_param_list : array_param_list COMMA array_param
							 | array_param '''
		if len(p) == 4:
			p[0] = p[1] +  [p[3]]
		else:
			p[0] = [p[1]]

	
	def p_array_declaration(self, p):
		''' expr : LBRACE array_param_list RBRACE '''
		p[0] = ast.Array(p[2])
	

	def p_for_declaration(self, p):
		''' expr : FOR variable IN variable ENDFOR
				 | FOR variable COMMA variable IN variable ENDFOR '''
		p[0] = ast.For(p[2], p[4], p[6])

	def p_empty(self, p):
		'empty : '

	def p_new_line(self, p):
		'statement : NEW_LINE '
		p[0] = ast.NewLine()

	def p_error(self, t):
		import sys
		try:
			sys.stderr.write("Syntax error at '%s' on line %s.\n" % (t.value, t.lineno))
		except:
			pass

if __name__== '__main__' : 
	parser = Parser()
	file = open('syntax/flow.purple', 'r')
	data = file.read()
	result = parser.parse(code=data)

	for r in result:
		print r

