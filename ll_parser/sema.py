# Copyright 2017 TU Dresden
# All rights reserved.
#
# Authors: Christian Menard
#          Norman Rink
from typing import List, Any, Tuple

from . import ast


class Sema:

    def __init__(self, ast):
        self.ast = ast
        self.symbol_table: List[Tuple[str, Any]] = list()

    def check(self):
        return self.check_node(self.ast)#[0]

    def check_node(self, node):
        if isinstance(node, ast.Let):
            return self.check_let(node)
        elif isinstance(node, ast.Identifier):
            return self.check_identifier(node)
        elif isinstance(node, ast.BinOp):
            return self.check_binop(node)
        elif isinstance(node, ast.IntLit):
            return True, node.value
        elif isinstance(node, ast.FloatLit):
            return True, node.value
        else:
            raise RuntimeError('unexpected AST node')

    def check_binop(self, node):
        assert isinstance(node, ast.BinOp)

        left_ok, left_value = self.check_node(node.left)
        right_ok, right_value = self.check_node(node.right)

        if node.kind == 'MUL':
            result = left_value * right_value
        elif node.kind == 'ADD':
            result = left_value + right_value
        else:
            raise RuntimeError(f'Illegal operation type: {node.kind}')
        ok = left_ok and right_ok
        return ok, result

    def check_let(self, node):
        assert isinstance(node, ast.Let)
        ok1, result = self.check_node(node.init)
        self.symbol_table.append((node.name, result))
        ok2, result = self.check_node(node.expr)
        self.symbol_table.pop()
        return ok1 and ok2, result

    def check_identifier(self, node):
        assert isinstance(node, ast.Identifier)
        ok = node.name in {name for name, _ in self.symbol_table}
        if ok:
            symbols = [entry for entry in self.symbol_table if entry[0] == node.name]
            value = symbols[-1][1]
            return ok, value
        else:
            return ok, None
