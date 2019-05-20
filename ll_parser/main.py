#! /usr/bin/python3
# Copyright 2017 TU Dresden
# All rights reserved.
#
# Authors: Christian Menard
#          Norman Rink

import sys

from .lexer import lexer
from .parser import Parser


def main():
    # read input
    lexer.input(sys.stdin.read())

    # Tokenize
    tokens = list(lexer)

    # parse
    parser = Parser(tokens)
    parser.parseS()


if __name__ == '__main__':
    main()
