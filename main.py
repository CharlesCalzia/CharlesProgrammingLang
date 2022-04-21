from ply import lex, yacc
import math

tokens = [
    'VARIABLE',
    'INT',
    'FLOAT',
    'STRING',
    'PLUS',
    'MINUS',
    'TIMES',
    'POWER',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'EQUALS',
]

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_POWER = r'\^'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUALS = '='
t_VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'

reserved = {
    'cwrite': 'cwrite',
    'cread': 'cread',
    'clear': 'clear',
}

tokens+=reserved.values()
print(tokens)

variables = {"pi": 3.1415926535, "e": 2.718281828}


def t_clear(t):
    r'clear'
    global variables
    variables = {"pi": 3.1415926535, "e": 2.718281828}

def t_FLOAT(t):
    r'[+-]?\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print(f"Float value too large: {t.value}")
        t.value = None
    return t

def t_INT(t):
    r'(?:-)?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(f"Integer value too large: {t.value}")
        t.value = None
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character {t.value[0]!r} on line {t.lexer.lineno}")
    t.lexer.skip(1)

def t_COMMENT(t):
    r'\#\#.*'
    pass


t_ignore = ' \t'

lexer = lex.lex()

# Parsing

def p_assign(t):
    'expression : VARIABLE EQUALS expression'
    variables[t[1]] = t[3]

def p_expression_cwrite(t):
    'expression : cwrite LPAREN expression RPAREN'
    print(t)
    print(t[0])

def p_expression_cread(t):
    'expression : cread LPAREN expression RPAREN'
    t[0] = t[1]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': 
        try: t[0] = t[1] / t[3]
        except ZeroDivisionError: print('Cannot divide by zero')
    elif t[2] == '^': t[0] = t[1] ** t[3]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_int(t):
    'expression : INT'
    t[0] = int(t[1])

def p_expression_float(t):
    'expression : FLOAT'
    t[0] = float(t[1])

def p_expression_string(t):
    'expression : STRING'
    t[0] = t[1]

def p_error(t):
    if t is None: # lexer error
        return
    print(f"Syntax Error: {t.value!r}")

def p_variable(t):
    'expression : VARIABLE'
    try:
        t[0] = variables[t[1]]
    except LookupError:
        print(f"Undefined variable {t[1]}")
        t[0] = None

def p_clear(t):
    'expression : clear'
    global variables
    variables = {"pi": 3.1415926535, "e": 2.718281828}

parser = yacc.yacc()

if __name__ == "__main__":
    print("\n### Welcome to the Charles Programming Langauge Shell ###\n")
    while True:
        inp = input("> ")
        lexer.input(inp)
        tokens = lexer.token()

        #for tok in lexer: print(tok)
        print(parser.parse(inp))
