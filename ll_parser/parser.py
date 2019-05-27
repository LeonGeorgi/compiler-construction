# Copyright 2017 TU Dresden
# All rights reserved.
#
# Authors: Christian Menard
#          Norman Rink
from typing import Union

from ll_parser.ast import IntLit, FloatLit, Identifier, BinOp


class Parser:
    """Parser for arithmetic expressions

    Args:
       tokens (List[str]): List of all tokens

    Attributes:
       current_token (str): The token currently being processed
       remaining_tokens (List[str]): List of unprocessed tokens
    """

    def __init__(self, tokens):
        self.current_token = None
        self.remaining_tokens = tokens

    def consume_token(self):
        """Consume a token and return it

        Remove the next token from ``remaining_tokens`` and update
        ``current_token``.

        Returns:
            str: The current token
        """
        if len(self.remaining_tokens) > 0:
            self.current_token = self.remaining_tokens.pop(0)
        else:
            self.current_token = None
        return self.current_token

    def accept_token(self, expected):
        """Consume a token and verify

        Verify that the current token is the ``expected`` token, remove the
        next token from ``remaining_tokens`` and update ``current_token``.

        Args:
            expected (str): Expected token

        Returns:
            str: The current token

        Raises:
            RuntimeError: if the ``current_token`` is not the ``expected`` token
        """
        t = self.current_token
        if t is None:
            raise RuntimeError('Expected token %s but found end of stream' %
                               expected)
        if t.type != expected:
            raise RuntimeError('Expected token %s but found %s' % (expected,
                                                                   t.type))
        return self.consume_token()

    def parseS(self):
        """Parse non-terminal S"""
        self.consume_token()  # read the first token
        t = self.current_token

        if t is None:
            raise RuntimeError('Error while parsing S (end of stream)')

        if (t.type == 'LPARAN'
                or t.type == 'INT_LIT'
                or t.type == 'FLOAT_LIT'
                or t.type == 'IDENTIFIER'):
            tree = self.parseE()
            assert len(self.remaining_tokens) == 0
            # we should have processed all tokens by now

            return tree
        else:
            raise RuntimeError('Error while parsing S (current token %s)' % t)

    # tokens = ('PLUS', 'STAR', 'LPARAN', 'RPARAN', 'INT_LIT', 'FLOAT_LIT',
    #           'IDENTIFIER')

    def parseE(self) -> Union[IntLit, FloatLit, Identifier, BinOp]:
        """Parse non-terminal E"""
        t = self.current_token

        if t is None:
            raise RuntimeError('E')
        if t.type not in ('LPARAN', 'INT_LIT', 'FLOAT_LIT', 'IDENTIFIER'):
            raise RuntimeError('E')

        tval = self.parseT()
        return self.parseEp(left=tval)

    def parseT(self) -> Union[IntLit, FloatLit, Identifier, BinOp]:
        """Parse non-terminal T"""
        t = self.current_token

        if t is None:
            raise RuntimeError('T')

        if t.type not in ('LPARAN', 'INT_LIT', 'FLOAT_LIT', 'IDENTIFIER'):
            raise RuntimeError('T')

        fval = self.parseF()
        tpval = self.parseTp(left=fval)
        return tpval

    def parseF(self) -> Union[IntLit, FloatLit, Identifier]:
        """Parse non-terminal F"""
        t = self.current_token

        if t is None:
            raise RuntimeError('F')

        if t.type == 'LPARAN':
            self.consume_token()

            parsed_value = self.parseE()

            self.accept_token('RPARAN')
            return parsed_value
        elif t.type == 'INT_LIT':
            val = int(t.value)
            self.consume_token()
            return IntLit(val)
        elif t.type == 'FLOAT_LIT':
            val = float(t.value)
            self.consume_token()
            return FloatLit(val)
        elif t.type == 'IDENTIFIER':
            name = str(t)
            self.consume_token()
            return Identifier(name)
        else:
            raise RuntimeError('F')

    def parseTp(self, left: Union[IntLit, FloatLit, Identifier, BinOp]) -> Union[IntLit, FloatLit, Identifier, BinOp]:
        """
        Parse non-terminal Tp
        
        T' -> * F T'
        T' -> ε
        """

        t = self.current_token

        if t is None or t.type in ('PLUS', 'RPARAN'):
            return left
        elif t.type == 'STAR':
            self.consume_token()

            value = self.parseF()
            right = self.parseTp(value)
            return BinOp('MUL', left, right)
        else:
            raise RuntimeError('T\'')

    def parseEp(self, left: Union[IntLit, FloatLit, Identifier, BinOp]) -> Union[IntLit, FloatLit, Identifier, BinOp]:
        """Parse non-terminal Ep"""
        t = self.current_token

        if t is None or t.type == 'RPARAN':
            return left
        elif t.type == 'PLUS':
            self.consume_token()
            value = self.parseT()
            right = self.parseEp(value)
            return BinOp('ADD', left, right)
        else:
            raise RuntimeError('E\'')
