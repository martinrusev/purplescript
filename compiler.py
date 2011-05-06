import sys
from purplescript.parser import Parser

input = sys.stdin
output = sys.stdout
curly_left = "\n\t{\n"
curly_right = "\n}\n"

class Compiler:

	def __init__(self, tree, file = sys.stdout):
		""" Compiler(tree, file=sys.stdout) -> None.
		 Print the source for tree to file.
		 """
		self.f = file
		self._indent = 0
		self._variable = 'semi' # semi -> $example | normal -> example
		self._param = False  # True -> writes commas after parameters in function
		
		self.f.write("<?php\n")
		self.dispatch(tree)
		print >>self.f,""
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
		self.write('(')
		self.dispatch(tree.params)
		self._variable = 'semi'  # restore state
		self.write(')')
		self.curly('left')
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
		self.write(');\n')
		self._variable = 'normal'

	def _This(self, tree):
		self.write(self.tabs())
		self.write('$this->')
		self._variable = 'normal'
	

	def _Variable(self, tree):

		if self._variable == 'normal':
			self.write(tree.name)
			if tree.type == 'dot':
				self.write('->')
		else:
			if not self._param:
				self.write(self.tabs())
			self.write('${0}'.format(tree.name))

		if tree.type == 'assign':
			self.write(' =')
			

	def _Constant(self, tree):
		self.write(self.tabs())
		self.write("define('{0}',{1});\n".format(tree.name, tree.value))

	def _ArrayKeyReference(self, tree):
		self.write('[')
		self.write(tree.value)
		self.write(']')


	def _Assignment(self, tree):
		self.write(' =')
		self._variable = 'semi'
			
	def _str(self, tree):
		self.write(tree)
	
	def _NoneType(self, tree):
		pass

	def params(self, params):
		for p in params:
			self.write('${0}, '.format(p))

if __name__== '__main__' : 
	_parser = Parser()

	test_file = 'class'

	input_file = 'syntax/{0}.purple'.format(test_file)
	output_file = 'syntax/{0}.php'.format(test_file)
	
	input = open(input_file, 'r')
	output = open(output_file, 'w')
	
	data = input.read()
	result = _parser.parse(code=data)

	Compiler(result)
