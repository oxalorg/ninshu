import ply.lex as lex
import unittest


class NinLexer():
    reserved = {
        'jutsu': 'JUTSU',
        'seal': 'SEAL',
        'shurikens': 'SHURIKENS',
        'throw': 'THROW',
        'miss': 'MISS',
        'refill': 'REFILL'
    }

    literals = ['{', '}', ';']

    tokens = [
        'NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EQ', 'LPAREN', 'RPAREN',
        'ID'
    ] + list(reserved.values())

    # Tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULT = r'\*'
    t_DIV = r'/'
    t_EQ = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ignore = " \t"

    # t_ignore_COMMENT = r'\#.*'

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ID')
        # Look up symbol table information and return a tuple
        # t.value = (t.value, symbol_lookup(t.value))
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)

    def test_next_tok(self):
        t = self.lexer.token()
        return {'type': t.type, 'value': t.value}


# Unit tests
class LexTest(unittest.TestCase):
    def setUp(self):
        self.lexer = NinLexer()
        self.lexer.build()

    def test_simple(self):
        self.lexer.test('2 + 3')

        t = self.lexer.test_next_tok()
        self.assertEqual('NUMBER', t['type'])
        self.assertEqual(2, t['value'])

        t = self.lexer.test_next_tok()
        self.assertEqual('PLUS', t['type'])
        self.assertEqual('+', t['value'])

        t = self.lexer.test_next_tok()
        self.assertEqual('NUMBER', t['type'])
        self.assertEqual(3, t['value'])

    def test_medium(self):
        self.lexer.test('* Trolololol /')

        t = self.lexer.test_next_tok()
        self.assertEqual('MULT', t['type'])
        self.assertEqual('*', t['value'])

        t = self.lexer.test_next_tok()
        self.assertEqual('ID', t['type'])
        self.assertEqual('Trolololol', t['value'])

        t = self.lexer.test_next_tok()
        self.assertEqual('DIV', t['type'])
        self.assertEqual('/', t['value'])

    def test_advanced(self):
        self.lexer.test('jutsu { } seal')

        t = self.lexer.test_next_tok()
        self.assertEqual('JUTSU', t['type'])
        self.assertEqual('jutsu', t['value'])

        t = self.lexer.test_next_tok()
        self.assertEqual('{', t['type'])
        self.assertEqual('{', t['value'])

        t = self.lexer.test_next_tok()
        self.assertEqual('}', t['type'])
        self.assertEqual('}', t['value'])

        t = self.lexer.test_next_tok()
        self.assertEqual('SEAL', t['type'])
        self.assertEqual('seal', t['value'])


if __name__ == '__main__':
    unittest.main()
