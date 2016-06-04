"""AST for ninshu"""


class ASTNode():
    pass


class ListNode(ASTNode):
    def __init__(self, children=[]):
        self.children = children

    def append(self, item):
        self.children.append(item)


class Showdown(ListNode):
    pass


class Combo(ListNode):
    pass


class JutsuSeal(ListNode):
    pass


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
