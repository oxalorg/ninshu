import ply.yacc as yacc
from lexer import NinLexer
import sys
import os
import logging
from njast import *
from njvisitor import *


class NinParser():

    precedence = (('left', 'PLUS', 'MINUS'),
                  ('left', 'MULT', 'DIV'),
                  ('right', 'UMINUS'), )

    identifiers = {}

    def __init__(self, Lexer, log=True):
        self.Lexer = Lexer
        self.Lexer.build()
        self.tokens = self.Lexer.tokens
        self.lexer = self.Lexer.lexer
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        if not log:
            self.logger.disabled = True

    def p_ninja_showdown(self, p):
        """
        showdown    : chakra
                    | showdown chakra
        """
        if len(p) == 2:
            p[0] = Showdown([p[1]])
        else:
            p[1].append(p[2])
            p[0] = p[1]
        tree = VisitorDispatch(p[0])
        print(tree.GLOBALS)

    def p_chakra(self, p):
        """
        chakra      : combo_move
                    | JUTSU '{' combo_move '}' SEAL
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = JutsuSeal([p[3]])
        self.logger.debug("chakra: {}".format(p[0]))

    def p_combo_move(self, p):
        """
        combo_move  : move
                    | combo_move move
        """
        if len(p) == 2:
            p[0] = Combo([p[1]])
        else:
            p[1].append(p[2])
            p[0] = p[1]
        # combo = Combo()
        # for move in moves:
        #     combo.children.append(move)
        # p[0] = combo
        # p[0] = Combo(moves)

    def p_move(self, p):
        """
        move    : hand_sign ';'
                | yinyang
        """
        p[0] = p[1]

    def p_yinyang(self, p):
        """
        yinyang : YIN predicate '{' combo_move '}' YANG '{' combo_move '}'
        """
        p[0] = YinYang(p[2], p[4], p[8])
        self.logger.debug("YinYang: {}".format(p[0]))

    def p_predicate(self, p):
        """
        predicate   : expression '>' expression
                    | expression '<' expression
                    | expression EQ expression
        """
        p[0] = BinOp(p[1], p[2], p[3])

    def p_hand_sign(self, p):
        """
        hand_sign   : ID '=' expression
                    | expression
        """
        if len(p) == 4:
            p[0] = HandSign(p[1], p[3])
        else:
            p[0] = p[1]
        self.logger.debug("hand_sign: {}".format(p[0]))

    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression MULT expression
                   | expression DIV expression
        """
        p[0] = BinOp(p[1], p[2], p[3])

    def p_expression_UMINUS(self, p):
        """
        expression : MINUS expression %prec UMINUS
        """
        p[0] = UnOp(p[1], p[2])

    def p_expression_variable(self, p):
        """
        expression  : NUMBER
        """
        p[0] = Number(p[1])

    def p_expression_ID(self, p):
        """
        expression  : ID
        """
        p[0] = Variable(p[1])

    def build(self, **kwargs):
        yacc.yacc(module=self)

    def run(self, data=None):
        if data:
            yacc.parse(data)
        else:
            while 1:
                try:
                    s = input('ninshu > ')
                except (EOFError, KeyboardInterrupt):
                    break
                yacc.parse(s)
        print(self.identifiers)


if __name__ == '__main__':
    Lexer = NinLexer()
    parser = NinParser(Lexer)
    parser.build()
    print(sys.argv)
    parent_dir = os.path.abspath(os.path.join(sys.argv[0], os.pardir))
    if len(sys.argv) > 1:
        input_file = os.path.join(parent_dir, sys.argv[1])
        with open(input_file, 'r') as f:
            input_string = f.read().replace('\n', '')
        parser.run(input_string)
    else:
        parser.run()
