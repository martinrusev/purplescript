"""
    purplescript.parser
    ~~~~~~~~~~~~

    This module builds the token list for the template

    :copyright: (c) 2010 by Martin Rusev.
    :license: BSD, see LICENSE for more details.
"""
from lexer import get_tokens

class Parser(object):

      def __init__(self, filename=None):
          self.previous = 0
          self.next= 0
          self.stream = get_tokens(filename)
          self.template = []
          self._parse()


      def _parse(self):
          for index, item in enumerate(self.stream):

              try:
                  self.previous = self.stream[index - 1]
                  self.next = self.stream[index + 1]
              except IndexError:
                  self.next = ''

              function_name = "parse_{_type}".format(_type=item['type'].lower())
              print function_name
              getattr(self, function_name).__call__(current=index,value=item['value'],line=item['line'])



          print self.template


      def parse_class(self, *args, **kwargs):
          return 'class {value}'.format(value=value)

      def parse_if(self, *args, **kwargs):
          return 'if\n'

      def parse_def(self, *args, **kwargs):
          return 'function '

      def parse_variable(self, *args, **kwargs):
          pass
          #print value
          #return '${value}'.format(value=value)

      def parse_endclass(self,*args, **kwargs):
          return '\n}'

      def parse_end(self, *args, **kwargs):
           return '\n}'

      def parse_dot(self, *args, **kwargs):
          return '->'

      def parse_this(self, *args, **kwargs):
          return '$this->'

      def parse_comment(self, *args, **kwargs):
          print self.next
          #return '{value}'.format(value=value)

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

if __name__ == '__main__':
    p = Parser(filename='test_syntax.txt')