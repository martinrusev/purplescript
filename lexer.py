"""
	purplescript.lexer
	~~~~~~~~~~~~
	:copyright: (c) 2011 by Martin Rusev.
	:license: BSD, see LICENSE for more details.
"""
__version__ = '0.1'

from ply import lex
from helper import merge_lists

class Lexer(object):

	reserved_words = {
			'if' : 'IF',
			'elseif': 'ELSEIF',
			'else' : 'ELSE',
			'endif': 'ENDIF',
			'for': 'FOR',
			'in': 'IN',
			'endfor': 'ENDFOR',
			'end' : 'END',
			'endclass' : 'ENDCLASS',
			'def' : 'DEF',
			'class' : 'CLASS',
			'extends' : 'EXTENDS',
			'implements' : 'IMPLEMENTS',
			}

	operators = (
			'ASSIGNMENT',
			'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
			'OR', 'AND', 'NOT', 'LT', 'LE', 'GT', 'GE',
			'EQ', 'NE',
			)

	delimiters = (
			'LPAREN', 'RPAREN', 'LBRACKET',
			'RBRACKET', 'LBRACE', 'RBRACE',
			'COMMA', 'SEMI', 'COLON', 'DOT',
			)

	increment_decrement = (
			'INCREMENT', 'DECREMENT',
			)

	object_oriented =(
			'THIS',
			)

	data_types = (
			'STRING',
			)

	generic_tokens = (
			'COMMENT', 'VARIABLE','CONSTANT', 'NUMBER', 'NEW_LINE',
			)


	tokens = merge_lists(
			operators, delimiters, object_oriented,
			increment_decrement, data_types, generic_tokens,
			reserved_words.values(),
			)

	# OPERATORS
	t_ASSIGNMENT       = r'='
	t_PLUS             = r'\+'
	t_MINUS            = r'-'
	t_TIMES            = r'\*'
	t_DIVIDE           = r'/'
	t_MODULO           = r'%'
	t_OR               = r'\|\|'
	t_AND              = r'&&'
	t_NOT              = r'!'
	t_LT               = r'<'
	t_GT               = r'>'
	t_LE               = r'<='
	t_GE               = r'>='
	t_EQ               = r'=='
	t_NE               = r'!='


	# DELIMITERS
	t_LPAREN           = r'\('
	t_RPAREN           = r'\)'
	t_LBRACKET         = r'\['
	t_RBRACKET         = r'\]'
	t_LBRACE           = r'\{'
	t_RBRACE           = r'\}'
	t_COMMA            = r','
	t_SEMI             = r';'
	t_COLON            = r':'
	t_DOT              = r'\.'


	# Increment/decrement
	t_INCREMENT        = r'\+\+'
	t_DECREMENT        = r'--'


	def t_NUMBER(self, t):
		r'[0-9]+'
		t.type = self.reserved_words.get(t.value, 'NUMBER')
		return t

	def t_VARIABLE(self, t):
		r'[A-Za-z][a-z_0-9]+'
		t.type = self.reserved_words.get(t.value,'VARIABLE')
		return t
	

	def t_CONSTANT(self, t):
		r'[A-Z_]+'
		t.type = self.reserved_words.get(t.value,'CONSTANT')
		return t
	
	
	# OBJECT ORIENTED STUFF
	def t_THIS(self, t):
		r'@'
		return t

	# DATA TYPES
	def t_STRING(self, t):
		r"\'([^\\\n]|(\\.))*?\'" 
		return t

	def t_newline(self,t):
		ur'\n+'
		t.lexer.lineno += t.value.count("\n")

	t_ignore  = '\t'

	def t_error(self, t):
		#print "Illegal character '%s'" % t.value[0]
		t.lexer.skip(1)

	def t_COMMENT(self, t):
		r'//.*'
		t.lexer.lineno += 1
		return t

	def build(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)

	def input(self, s):
		self.build()
		self.lexer.paren_count = 0
		self.lexer.input(s)

	def token(self):
		t = self.lexer.token()

		return t
		try:
			return self.token_stream.next()
		except StopIteration:
			return None	


if __name__== '__main__' : 
	import os.path
	import sys

	lexer = Lexer()
	token_list = []
	file = 'syntax/flow.purple'

	try:
		os.path.isfile(file)
		with open(file, 'r') as f:
			data = f.read()
			lexer.input(data)
		while True:
			tok = lexer.token()

			if not tok: break

			element = {'type': tok.type, 'value':tok.value, 'line': tok.lineno, 'position':tok.lexpos}
			token_list.append(tok)
		
		print token_list
	except: 
		print "Unexpected error:", sys.exc_info()[0]
		raise

