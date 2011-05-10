class Node(object):
    fields = []

    def __init__(self, *args, **kwargs):
        assert len(self.fields) == len(args), \
            '%s takes %d arguments' % (self.__class__.__name__,
                                       len(self.fields))
        try:
            self.lineno = kwargs['lineno']
        except KeyError:
            self.lineno = None
        for i, field in enumerate(self.fields):
            setattr(self, field, args[i])

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__,
                           ', '.join([repr(getattr(self, field))
                                      for field in self.fields]))



def node(name, fields):
    attrs = {'fields': fields}
    return type(name, (Node,), attrs)


Function = node('Function', ['name', 'params', 'nodes'])
InlineFunction = node('InlineFunction', ['params'])
Class = node('Class', ['name', 'nodes'])
This = node('This', []) # the most important word in php :)
Variable = node('Variable', ['name','value', 'position','type'])
Parameter = node('Parameter', ['name','value', 'position'])
Constant = node('Constant', ['name','value'])
Assignment = node('Assignment', [])
Array = node('Array', ['nodes'])
ArrayElement = node('ArrayElement', ['key', 'value', 'position'])
ArrayKeyReference = node('ArrayKeyReference', ['value'])
NewLine = node('NewLine', [])
For = node('For', ['key', 'value', 'array'])
