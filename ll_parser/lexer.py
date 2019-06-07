# Copyright 2017 TU Dresden
# All rights reserved.
#
# Authors: Christian Menard
#          Norman Rink


"""Lexer module

This module defines the ``lexer`` using a python implementation of Lex.
"""


import ply.lex as lex


tokens = ('LET', 'IN', 'EQUALS', 'PLUS', 'STAR', 'LPARAN', 'RPARAN', 'INT_LIT',
          'FLOAT_LIT', 'IDENTIFIER')

# regular expressions
t_EQUALS = r'='
t_PLUS = r'\+'
t_STAR = r'\*'
t_LPARAN = r'\('
t_RPARAN = r'\)'
t_ignore = ' \t\n"'


# since the general IDENTIFIER rule also matches 'let and in' we check these
# cases specifically.
def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value == 'let':
        t.type = 'LET'
    if t.value == 'in':
        t.type = 'IN'
    return t


def t_FLOAT_LIT(t):
    r'[0-9]+\.[0-9]+(E(\+|\-)?[0-9]+)?'
    t.value = float(t.value)
    return t


def t_INT_LIT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(0)


# define the lexer
lexer = lex.lex()
