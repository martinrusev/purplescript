"""
    purplescript.compiler
    ~~~~~~~~~~~~

    :copyright: (c) 2010 by Martin Rusev.
    :license: BSD, see LICENSE for more details.
"""
class CodeGenerator(object):

    def __init__(output_file=None, template=None):
        with open(output_file, 'w+') as f:
             line = "{_type}, {value}:{line}-{pos}".format(value=tok.value, _type=tok.type, line=tok.lineno, pos=tok.lexpos)
             f.write(line)