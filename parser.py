"""
    purplescript.parser
    ~~~~~~~~~~~~

    This module parses the tokens and builds the template line by line

    :copyright: (c) 2010 by Martin Rusev.
    :license: BSD, see LICENSE for more details.
"""
from lexer import get_tokens
from utils import *
# experimental
from compiler import *

class Parser(object):

      #  We are setting the lookahead method here
      def __init__(self, filename=None):

          self.previous = 0
          self.next= 0


          self.stream = get_tokens(filename)

          #  @template
          #  dictionary that holds the whole tempate line by line
          #  we pass this to the code generator
          self.template = {}

          # @skip_to
          # used when we consume several stream elements at once
          # Example: parse_variable consumes 3 elements - VARIABLE, ASSIGNMENT, VALUE
          # we set skip_to at VALUE so that _parse resumes the parsing at the element after VALUE
          self.skip_to = 0
          #
          #  used in the template dictionary for line tracing
          #
          self.line_number = 0
          self._parse()



      #
      #   Parses the stream
      #   stream element format:
      #        {'type': token.type, 'value' : token.value, 'line' : token.linenumber , 'position' : tok.lexposition}
      #
      def _parse(self):
          for index, item in enumerate(self.stream):

              self.current = index
              try:
                  self.previous = Struct(**self.stream[index - 1])
                  self.next = Struct(**self.stream[index + 1])
              except IndexError:
                  self.next = ''

              function_name = "parse_{_type}".format(_type=item['type'].lower())
              #print function_name
              getattr(self, function_name).__call__(value=item['value'],line=item['line'])



          #print self.template




      def parse_variable(self, *args, **kwargs):
          # Typical variables $var = 'string';
          if self.next.type == 'ASSIGNMENT':
              #ARRAY OR SIMPLE VARIABLE ASSIGNMENT
              variable_def = Struct(**self.stream[self.current+2])
              variable = kwargs['value']
              print variable_def.type

              if variable_def.type == 'ARRAY_BEGIN':
                  line = 'boo'
                  array_end = self._find_next(token_type='ARRAY_END')
                  print self.stream[array_end]
              else:
                  # CONSTANT
                  if variable.isupper():
                     line = "define({variable},{string});".format(variable=variable, string=variable_def.value)
                  else:
                     line = "${variable} = {string};".format(variable=variable, string=variable_def.value)

              self._set_line_number()
              self.template[self.line_number] = line


          pass
          #print value
          #return '${value}'.format(value=value)


      def parse_class(self, *args, **kwargs):
          return 'class {value}'.format(value=value)

      def parse_if(self, *args, **kwargs):
          return 'if\n'

      def parse_def(self, *args, **kwargs):
          return 'function '

      def parse_endclass(self,*args, **kwargs):
          return '\n}'

      def parse_end(self, *args, **kwargs):
           return '\n}'

      def parse_dot(self, *args, **kwargs):
          return '->'

      def parse_comma(self, *args, **kwargs):
          pass

      def parse_this(self, *args, **kwargs):
          return '$this->'

      def parse_comment(self, *args, **kwargs):

          line = "{value}".format(value=kwargs['value'])
          self._set_line_number()
          self.template[self.line_number] = line

      def parse_assignment(self, *args, **kwargs):
          return ' = '

      def parse_string(self, *args, **kwargs):
          pass
          #return value

      def parse_newline(self, *args, **kwargs):
          return '\n'

      def parse_lbracket(self, *args, **kwargs):
          return '['

      def parse_rbracket(self, *args, **kwargs):
          return ']'

      def parse_lparen(self, *args, **kwargs):
          return '('

      def parse_rparen(self, *args, **kwargs):
          return ')'

      def parse_array_begin(self, *args, **kwargs):
          return '{'

      def parse_array_end(self, *args, **kwargs):
          return '}'

      def parse_colon(self, *args, **kwargs):
          return ' => '

      def _set_line_number(self, *args, **kwargs):
          self.line_number = self.line_number+1

      # NOT VERY EFFECTIVE, ITERATES OVER THE WHOLE STREAM
      # MUST IMPLEMENT SOME KIND OF STREAM INDEX FOR FAST SEARCHING
      def _find_next(self, token_type=None, *args, **kwargs):
          for index, key in enumerate(self.stream):
              if key['type'] == token_type and index > self.current:
                  return index

if __name__ == '__main__':
    p = Parser(filename='test_syntax.txt')
    #c = Compiler(output_file= 'test.php' , template=p.template)