#Lex Yacc

import ply.lex as lex
import ply.yacc as yacc
import re

tokens = ('LPAREN', 'RPAREN', 'AND', 'NOT', 'OR', 'IMPLIES', 'PREDICATE')

t_ignore = ' \t'
t_AND = r'\&'
t_OR = r'\|'
t_IMPLIES = r'=>'
t_NOT = r'~'
# t_ID = r'[A-ZA-Za-z_][a-zA-Z0-9_]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PREDICATE = r"[A-Z][A-Za-z]* [(]([A-Za-z]*)([,] [A-Za-z]*)*[)]"

def p_NOT(p):
    """
    pred : LPAREN NOT pred RPAREN
    """
    p[0] = [p[2],p[3]]

def p_exp(p):
    """
    pred : LPAREN pred AND pred RPAREN
            | LPAREN pred OR pred RPAREN
            | LPAREN pred IMPLIES pred RPAREN
    """
    p[0] = [p[2],p[3],p[4]]

def p_terminal(p):
    """
    pred : PREDICATE
    """
    p[0] = p[1]

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

lexer = lex.lex()
parser = yacc.yacc()
# print(re.sub('\s+', '', "(Kills(Jack, Tuna) | Kills(Curiosity, Tuna))").strip())
# print(parser.parse(re.sub('\s+', '', "(Kills(Jack, Tuna) | Kills(Curiosity, Tuna))").strip()),lexer)

#read each line from file , replace trailing spaces with single/no space, then pass it through parser
