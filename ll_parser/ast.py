# Copyright 2017 TU Dresden
# All rights reserved.
#
# Authors: Christian Menard
#          Norman Rink


"""AST module

This module contains multiple classes that each represent an AST
node. Furthermore, it defines the function ``indent(s, n)`` as a helper for
pretty printing.
"""

import textwrap


def indent(s, n):
    """Add indentation to multiline string

    Args:
       s (str): Input string
       n (int): Number of indentation spaces

    Returns:
        str: ``s`` indented by ``n`` spaces
    """
    return textwrap.indent(s, n * ' ')


class IntLit:
    """Integer literal AST node

    Args:
       value (int): Value of the integer literal

    Attributes:
       value (int): Value of the integer literal
    """

    def __init__(self, value):
        self.value = value

    def calculate(self):
        return self.value

    def __str__(self):
        """Convert to string (pretty print)"""
        return 'INTEGER LIT. <%d>\n' % (self.value)


class FloatLit:

    def __init__(self, value):
        """Float literal AST node

        Args:
           value (float): Value of the float literal

        Attributes:
           value (float): Value of the float literal
        """
        self.value = value

    def calculate(self):
        return self.value

    def __str__(self):
        """Convert to string (pretty print)"""
        return 'FLOAT LIT. <%f>\n' % (self.value)


class Identifier:
    def __init__(self, name):
        """Identifier AST node

        Args:
           name (str): Name of the identifier

        Attributes:
           name (str): Name of the identifier
        """
        self.name = name
        self.value = None

    def __str__(self):
        """Convert to string (pretty print)"""
        return 'IDENTIFIER <%s>\n' % self.name


class BinOp:
    def __init__(self, kind, left, right):
        """Binary Operator AST node

        Args:
           kind (str): Name of the operation ('MUL' or 'ADD')
           left: AST node left to the operator
           right: AST node right to the operator

        Attributes:
           name (str): Name of the identifier
           left: AST node left to the operator
           right: AST node right to the operator
        """

        self.kind = kind
        self.left = left
        self.right = right

    def __str__(self):
        """Convert to string (pretty print)"""
        result = 'BINARY OP. <%s>\n' % self.kind
        result += indent(str(self.left), 2)
        result += indent(str(self.right), 2)
        return result


class Let:
    """Let AST node

    Args:
       name (str): Name of the identifier
       init: AST node representing the initializer expression
       expr: AST node representing the nested expression

    Attributes:
       name (str): Name of the identifier
       init: AST node representing the initializer expression
       expr: AST node representing the nested expression
    """

    def __init__(self, name, init, expr):
        self.name = name
        self.init = init
        self.expr = expr

    def __str__(self):
        """Convert to string (pretty print)"""
        result = 'LET %s BE\n' % self.name
        result += indent(str(self.init), 2)
        result += 'IN\n'
        result += indent(str(self.expr), 2)
        return result
