#! /usr/bin/python3
# Copyright 2017 TU Dresden
# All rights reserved.
#
# Authors: Christian Menard
#          Norman Rink

import sys

from ll_parser.sema import Sema
from .lexer import lexer
from .parser import Parser


def main():
    # read input
    lexer.input(input("INPUT: "))

    # Tokenize
    tokens = list(lexer)

    # parse and create AST
    parser = Parser(tokens)
    ast = parser.parseS()


    # perform semantic analysis
    sema = Sema(ast)
    ok = sema.check()

    # pretty print the AST
    print(str(ast))
    print(f'Result: {ok}')


if __name__ == '__main__':
    main()
