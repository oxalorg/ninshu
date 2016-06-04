"""Visits the AST"""
from njast import *
import operator as op


class Visitor():
    def __init__(self, node):
        self.visit(node)

    def visit(self, node):
        method_name = 'visitor_' + node.__class__.__name__
        visitor_dispatch = getattr(self, method_name)
        return visitor_dispatch(node)


class VisitorDispatch(Visitor):
    GLOBALS = {}
    OPERATORS = {'+': op.add,
                 '-': op.sub,
                 '/': op.truediv,
                 '*': op.mul,
                 '<': op.lt,
                 '>': op.gt}

    def visitor_ListNode(self, node):
        for child in node.children:
            self.visit(child)

    def visitor_Showdown(self, node):
        return self.visitor_ListNode(node)

    def visitor_Combo(self, node):
        return self.visitor_ListNode(node)

    def visitor_JutsuSeal(self, node):
        return self.visitor_ListNode(node)

    def visitor_YinYang(self, node):
        predicate = self.visit(node.predicate)
        if predicate:
            return self.visit(node.yin)
        else:
            return self.visit(node.yang)

    def visitor_HandSign(self, node):
        self.GLOBALS[node.var] = self.visit(node.expr)

    def visitor_BinOp(self, node):
        return self.OPERATORS[node.op](self.visit(node.left),
                                       self.visit(node.right))

    def visitor_UnOp(self, node):
        if node.op == '-':
            return -1 * self.visit(node.expr)

    def visitor_Number(self, node):
        return node.value

    def visitor_Variable(self, node):
        try:
            return self.GLOBALS[node.value]
        except LookupError:
            raise
