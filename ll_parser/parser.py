# Copyright 2017 TU Dresden
# All rights reserved.
#
# Authors: Christian Menard
#          Norman Rink

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
            print(self.parseE())
            # we should have processed all tokens by now
            assert len(self.remaining_tokens) == 0
        else:
            raise RuntimeError('Error while parsing S (current token %s)' % t)

    # tokens = ('PLUS', 'STAR', 'LPARAN', 'RPARAN', 'INT_LIT', 'FLOAT_LIT',
    #           'IDENTIFIER')

    def parseE(self):
        """Parse non-terminal E"""
        t = self.current_token

        if t is None:
            raise RuntimeError('E')
        if t.type not in ('LPARAN', 'INT_LIT', 'FLOAT_LIT', 'IDENTIFIER'):
            raise RuntimeError('E')

        tval = self.parseT()
        return self.parseEp(left=tval)

    def parseT(self):
        """Parse non-terminal T"""
        t = self.current_token

        if t is None:
            raise RuntimeError('T')

        if t.type not in ('LPARAN', 'INT_LIT', 'FLOAT_LIT', 'IDENTIFIER'):
            raise RuntimeError('T')

        fval = self.parseF()
        tpval = self.parseTp(fval)
        return tpval

    def parseF(self):
        """Parse non-terminal F"""
        t = self.current_token

        if t is None:
            raise RuntimeError('F')

        if t.type == 'LPARAN':
            self.consume_token()

            val = self.parseE()

            self.accept_token('RPARAN')
            return val
        elif t.type == 'INT_LIT':
            val = int(t.value)
            self.consume_token()
            return val
        elif t.type == 'FLOAT_LIT':
            val = float(t.value)
            self.consume_token()
            return val
        elif t.type == 'IDENTIFIER':
            self.consume_token()
            # TODO
        else:
            raise RuntimeError('F')

    def parseTp(self, left):
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

            fval = self.parseF()
            tpval = self.parseTp(left * fval)

            return tpval
        else:
            raise RuntimeError('T\'')

    def parseEp(self, left):
        """Parse non-terminal Ep"""
        t = self.current_token

        if t is None or t == 'RPARAN':
            return left
        elif t.type == 'PLUS':
            self.consume_token()
            tval = self.parseT()
            epval = self.parseEp(left + tval)
            return epval
        else:
            raise RuntimeError('E\'')
