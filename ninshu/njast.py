"""AST for ninshu"""


class ASTNode():
    pass


class Showdown(ASTNode):
    def __init__(self, children=[]):
        self.childen = children


class Combo(ASTNode):
    def __init__(self, children=[]):
        self.children = children
        # self.parent = parent

    def append(self, item):
        self.children.append(item)


class JutsuSeal(ASTNode):
    def __init__(self, children=[]):
        self.children = children


class YinYang(ASTNode):
    def __init__(self, predicate, yin, yang):
        self.predicate = predicate
        self.yin = yin
        self.yang = yang


class HandSign(ASTNode):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class Number(ASTNode):
    def __init__(self, value):
        self.value = value


class Variable(ASTNode):
    def __init__(self, value):
        self.value = value
