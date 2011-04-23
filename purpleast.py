class Node(object):
	def __init__(self,type=None, children=None, leaf=None):

		self.type = type
		self.leaf = leaf
		if children is None:
			children = []
		self.children = children

	def append(self, val):
		self.children.append(val)

	def __str__(self):
		return '\n'.join(str(x) for x in self)

	def __iter__(self):
		return iter(self.children)
