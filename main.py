import re

KEYWORDS = {'if', 'else', 'while', 'def', 'return'}
OPERATORS = {'+', '-', '*', '/', '=', '==', '<', '>', '!=', '>=', '<='}
DELIMITERS = {':', ',', '(', ')'}

def is_identifier(token):
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token)

def tokenize(code):
    tokens = []
    lines = code.split('\n')
    
    for line_num, line in enumerate(lines):
        i = 0
        while i < len(line):
            char = line[i]
            
            if char.isspace():
                i += 1
                continue

            # Comments
            if char == '#':
                tokens.append(('COMMENT', line[i:]))
                break

            # Strings
            if char in ('"', "'"):
                quote = char
                j = i + 1
                while j < len(line) and line[j] != quote:
                    j += 1
                j += 1
                tokens.append(('STRING', line[i:j]))
                i = j
                continue

            # Numbers
            if char.isdigit():
                j = i
                while j < len(line) and line[j].isdigit():
                    j += 1
                tokens.append(('NUMBER', line[i:j]))
                i = j
                continue

            # Identifiers or keywords
            if char.isalpha() or char == '_':
                j = i
                while j < len(line) and (line[j].isalnum() or line[j] == '_'):
                    j += 1
                word = line[i:j]
                token_type = 'KEYWORD' if word in KEYWORDS else 'IDENTIFIER'
                tokens.append((token_type, word))
                i = j
                continue

            # Operators (multi-char like ==, <=)
            two_char_op = line[i:i+2]
            if two_char_op in OPERATORS:
                tokens.append(('OPERATOR', two_char_op))
                i += 2
                continue
            elif char in OPERATORS:
                tokens.append(('OPERATOR', char))
                i += 1
                continue

            # Delimiters
            if char in DELIMITERS:
                tokens.append(('DELIMITER', char))
                i += 1
                continue

            # Unknown character (skip)
            i += 1

        tokens.append(('NEWLINE', '\\n'))
    
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def match(self, expected_type, expected_value=None):
        tok_type, tok_val = self.current()
        if tok_type == expected_type and (expected_value is None or tok_val == expected_value):
            self.pos += 1
            return True
        return False

    def expect(self, expected_type, expected_value=None):
        if not self.match(expected_type, expected_value):
            raise SyntaxError(f'Expected {expected_type} {expected_value}, got {self.current()}')

    def parse(self):
        self.parse_stmt_list()

    def parse_stmt_list(self):
        while self.current()[0] != 'EOF' and self.current()[0] != 'DEDENT':
            self.parse_stmt()

    def parse_stmt(self):
        if self.match('KEYWORD', 'if'):
            self.parse_expr()
            self.expect('DELIMITER', ':')
            self.expect('NEWLINE')
            self.parse_stmt_list()  # Nested block
        elif self.match('KEYWORD', 'while'):
            self.parse_expr()
            self.expect('DELIMITER', ':')
            self.expect('NEWLINE')
            self.parse_stmt_list()
        elif self.match('KEYWORD', 'def'):
            self.expect('IDENTIFIER')
            self.expect('DELIMITER', '(')
            self.parse_param_list()
            self.expect('DELIMITER', ')')
            self.expect('DELIMITER', ':')
            self.expect('NEWLINE')
            self.parse_stmt_list()
        elif self.match('KEYWORD', 'return'):
            self.parse_expr()
            self.expect('NEWLINE')
        elif self.current()[0] == 'IDENTIFIER':
            self.match('IDENTIFIER')
            if self.match('OPERATOR', '='):
                self.parse_expr()
        elif self.current()[0] == 'COMMENT':
            self.match('COMMENT')  # Yorumu atla
            self.expect('NEWLINE')  # Satır sonunu bekle

        elif self.current()[0] == 'NEWLINE':
            self.match('NEWLINE')
        else:
            raise SyntaxError(f'Invalid statement: {self.current()}')

    def parse_param_list(self):
        if self.current()[0] == 'IDENTIFIER':
            self.match('IDENTIFIER')
            while self.match('DELIMITER', ','):
                self.expect('IDENTIFIER')


    def parse_term(self):
        self.parse_factor()
        while self.current()[1] in ('*', '/'):
            self.match('OPERATOR')
            self.parse_factor()

    def parse_factor(self):
        tok_type, tok_val = self.current()
        if tok_type == 'NUMBER' or tok_type == 'IDENTIFIER' or tok_type == 'STRING':
            self.match(tok_type)
        elif self.match('DELIMITER', '('):
            self.parse_expr()
            self.expect('DELIMITER', ')')
        else:
            raise SyntaxError(f'Invalid factor: {self.current()}')
    def parse_expr(self):
        self.parse_comparison()

    def parse_comparison(self):
        self.parse_arith_expr()
        while self.current()[0] == 'OPERATOR' and self.current()[1] in ('>', '<', '>=', '<=', '==', '!='):
            self.match('OPERATOR')
            self.parse_arith_expr()

    def parse_arith_expr(self):
        self.parse_term()
        while self.current()[1] in ('+', '-'):
            self.match('OPERATOR')
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.current()[1] in ('*', '/'):
            self.match('OPERATOR')
            self.parse_factor()
    

code = '''
def foo(x):
    if x > 5:
        return x + 1
# bu bir yorum
'''

tokens = tokenize(code)
parser = Parser(tokens)
parser.parse()
print("Syntax is correct!")