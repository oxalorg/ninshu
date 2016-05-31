import ply.lex as lex


class NinLexer():
    reserved = {
        'justu': 'JUTSU',
        'seal': 'SEAL',
        'shurikens': 'SHURIKENS',
        'throw': 'THROW',
        'miss': 'MISS',
        'refill': 'REFILL'
    }

    tokens = [
        'NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EQ', 'LPAREN',
        'RPAREN', 'ID'
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
        t.type = reserved.get(t.value, 'ID')
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
        for tok in self.lexer:
            print(tok)


testLex = NinLexer()
testLex.build()
testLex.test('2 + 3')
