import sys
import cStringIO
import os
from purplescript.parser import Parser

input = sys.stdin
output = sys.stdout

def unparse(nodes):
	result = []
	for node in nodes:
		result.append(unparse_node(node))

	return False
#return ''.join(result)

def unparse_node(node, is_expr=False):

	print type(node)



	pass

def interleave(inter, f, seq):
	"""Call f on each item in seq, calling inter() in between.
	"""
	seq = iter(seq)
	try:
		f(seq.next())
	except StopIteration:
		pass
	else:
		for x in seq:
			inter()
			f(x)


curly_left = "\n\t{\n"
curly_right = "\n}\n"

class Compiler:

	def __init__(self, tree, file = sys.stdout):
		"""Unparser(tree, file=sys.stdout) -> None.
		 Print the source for tree to file."""
		self.f = file
		self._indent = 0
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
		self.f.write('class {0}'.format(tree.name))
		self.curly('left')
		self.dispatch(tree.nodes)
		self.curly('right')


	def _Function(self, tree):
		self.write("{0}function {1}()".format(self.tabs(), tree.name))
		self.curly('left')
	
		self.curly('right')

if __name__== '__main__' : 
	_parser = Parser()
	file = open('syntax/class.txt', 'r')
	data = file.read()
	result = _parser.parse(code=data)

	Compiler(result)
	#output.write(unparse(result))
