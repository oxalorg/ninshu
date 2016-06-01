import ply.yacc as yacc
from lexer import NinLexer
import sys
import logging


class NinParser():

    precedence = (('left', 'PLUS', 'MINUS'),
                  ('left', 'MULT', 'DIV'),
                  ('right', 'UMINUS'), )

    identifiers = {}

    def __init__(self, Lexer, log=True):
        self.tokens = Lexer.tokens
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        if not log:
            self.logger.disabled = True

    def p_combo_move(self, p):
        """
        combo_move  : move
        """
        p[0] = p[1]

    def p_move(self, p):
        """
        move    : hand_sign
        """
        p[0] = p[1]

    def p_hand_sign(self, p):
        """
        hand_sign   : ID EQ expression
                    | expression
        """
        if len(p) == 4:
            self.identifiers[p[1]] = p[3]
        else:
            p[0] = p[1]

    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression MULT expression
                   | expression DIV expression
        """
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        self.logger.debug(p[0])

    def p_expression_UMINUS(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = -p[2]

    def p_expression_variable(self, p):
        """
        expression  : NUMBER
        """
        p[0] = p[1]

    def p_expression_ID(self, p):
        """
        expression  : ID
        """
        try:
            p[0] = self.identifiers[p[1]]
        except LookupError:
            # If a variable isn't defined yet, silently make it 42
            p[0] = 42
            # cuz why not?

    def build(self, **kwargs):
        yacc.yacc(module=self)

    def run(self):
        while 1:
            try:
                s = input('ninshu > ')
            except (EOFError, KeyboardInterrupt):
                break
            yacc.parse(s)
        print(self.identifiers)


if __name__ == '__main__':
    Lexer = NinLexer()
    Lexer.build()
    lexer = Lexer.lexer
    parser = NinParser(Lexer)
    parser.build()
    parser.run()
