import sys
from purplescript.parser import Parser

input = sys.stdin
output = sys.stdout

class Compiler:

	def __init__(self, tree, file = sys.stdout):
		""" Compiler(tree, file=sys.stdout) -> None.
		 Prints the source for tree to file.
		 """
		self.f = file
		self._indent = 0
		self._variable = 'semi' # semi -> $example | normal -> example
		self._param = False  # True -> writes commas after parameters in function
		self._tabs = True # False -> disables tabs after assignment
		self._newline = True # False -> disables new line after functions 
		self._semicolon = True # True -> writes ; after parameters
		
		self.f.write("<?php\n")
		self.dispatch(tree)
		self.f.write('\n?>')
		self.f.flush()

	def fill(self, text = ""):
		self.f.write("\n"+"    "*self._indent + text)

	def enter(self):
		self._indent += 1
	
	def tabs(self):
		return "\t" * self._indent

	def leave(self):
		self._indent -= 1

	def write(self, text):
		"Append a piece of text to the current line."
		self.f.write(text)

	def curly(self, type):

		if type == 'left':
			tabs = self.tabs()
			self.enter()
			curly = "{"
		else:
			self.leave()
			tabs = self.tabs()
			curly = "}"
		
		
		self.f.write('\n{0}{1}\n'.format(tabs, curly))

	def dispatch(self, tree):
		"Dispatcher function, dispatching tree type T to method _T."
		if isinstance(tree, list):
			for t in tree:
				self.dispatch(t)
			return
		method = getattr(self, "_"+tree.__class__.__name__)
		method(tree)


	def _Class(self, tree):
		self.write('class ')
		self._variable = 'normal'
		self.dispatch(tree.name)
		self.curly('left')
		self.dispatch(tree.nodes)
		self.curly('right')


	def _Function(self, tree):
		self.write(self.tabs())
		self.write("function ")
		self._variable = 'normal'
		self.dispatch(tree.name)
		self._newline = False
		self._semicolon = False
		self.dispatch(tree.params)
		self.curly('left')
		self._variable = 'semi'
		self.dispatch(tree.nodes)
		self.curly('right')

	def _Parameter(self, tree):
		self._param = True
		self.dispatch(tree.name)
		self._param = False
		if tree.value != None:
			self.write('={0}'.format(tree.value))
		if tree.position != 'last':
			self.write(', ')

	def _InlineFunction(self, tree):
		self.write('(')
		self._variable = 'comma'
		self.dispatch(tree.params)
		self.write(')')
		if self._semicolon is True:
			self.write(';')
		if self._newline is True:
			self.write('\n')
			self._newline = False
		self._variable = 'normal'

	def _This(self, tree):
		if self._tabs is True:
			self.write(self.tabs())
			self._tabs = False 
	
		self.write('$this->')
		self._variable = 'normal'
	

	def _Variable(self, tree):
		if self._variable == 'normal':
			self.write(tree.name)
			if tree.type == 'dot':
				self.write('->')
		else:
			if not self._param and self._tabs is True:
				self.write(self.tabs())
			self.write('${0}'.format(tree.name))

	def _Constant(self, tree):
		self.write(self.tabs())
		self.write("define('{0}',{1});\n".format(tree.name, tree.value))

	def _ArrayKeyReference(self, tree):
		self.write('[')
		self.write(tree.value)
		self.write(']')


	def _Assignment(self, tree):
		self.write(' = ')
		self._tabs = False
		self._variable = 'semi'


	def _ArrayElement(self, tree):
		self.write(tree.key)
		if tree.value:
			self.write(' => ')
			self._semicolon = False
			self.dispatch(tree.value)
			self._semicolon = True
		if tree.position != 'last':
			self.write(',')
	
	def _Array(self, tree):
		self.write('array(')
		self.dispatch(tree.nodes)
		self.write(');')

	def _For(self, tree):
		'''
		Reference :  For -> 'key', 'start', 'end', 'nodes'
		'''
		if self._tabs:
			self.write(self.tabs())
		self.write('for(')
		self._tabs = False
		self.dispatch(tree.key)
		self.write('=')
		self.write(tree.start)
		self.write('; ')
		self.dispatch(tree.key)
		self.write('<=')
		self.write(tree.end)
		self.write('; ')
		self.dispatch(tree.key)
		self.write('++')
		self.write(')')
		self.curly('left')
		self.curly('right')
		self._tabs = True
			
	def _ForEach(self, tree):
		'''
		Reference: ForEach -> key', 'value', 'array', 'nodes'
		'''
		if self._tabs:
			self.write(self.tabs())
		self.write('foreach(')
		self._tabs = False
		self.dispatch(tree.array)
		self.write(' as ')
		# foreach($array as $key => $value)
		if tree.value:
			self.dispatch(tree.key)
			self.write(' => ')
			self.dispatch(tree.value)
		# foreac($array as $value)
		else: 
			self.dispatch(tree.key)

		self.write(')')
		self.curly('left')
		self.curly('right')
		self._tabs = True
	
	
	def _str(self, tree):
		self.write(tree)
	
	def _NoneType(self, tree):
		pass

	def params(self, params):
		for p in params:
			self.write('${0}, '.format(p))

if __name__== '__main__' : 
	_parser = Parser()

	test_file = 'flow'

	input_file = 'syntax/{0}.purple'.format(test_file)
	output_file = 'syntax/{0}.php'.format(test_file)
	
	input = open(input_file, 'r')
	output = open(output_file, 'w')
	
	data = input.read()
	result = _parser.parse(code=data)

	Compiler(result)
