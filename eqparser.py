#from scipy.optimize import fsolve
#from math import *
from Lexer import Lexer
from Parser import Parser

class InvalidNameError(Exception):
    def __init__(self, word):
        self.word = word
 
    def __str__(self):
        return "Reserved word %s cannot be used as an identifier" % (self.word)

def main():
    var = []
    const = []
    eqn = []
    reserved = ['exp','log','log10','acos','asin','atan','cos','sin','tan','cosh','sinh','tanh']
    
    f = open(r'C:\Stuff\work\inputmv.txt', 'r')
    for line in f:
        if line[-1]=="\n":
            line = line[:-1]
        if line.find('var',0,3) == 0:
            var = line[line.find(' ')+1:].split(',')
        elif line.find('const',0,5) == 0:
            const = line[line.find(' ')+1:].split(',')
        elif len(line) > 0:
            eqn.append(line)
    f.close()

    # Make sure they are sorted by length
    if len(const) > 0:
        const.sort(lambda x, y: len(x)-len(y))
    if len(var) > 0:
        var.sort(lambda x, y: len(x)-len(y))
    for word in reserved:
        if word in var or word in const:
            raise InvalidNameError(word)
    
    rules = {
        "Function": r"(exp|log|log10|acos|asin|atan|cos|sin|tan|cosh|sinh|tanh)\(",
        "Number": r"\d+(\.\d+)?",
        "Operator": r"[-+()*^]", 
    }
 
    lex = Lexer(rules, False)
    out = ['[']
    for equation in eqn:
        tokens = [(group,value) for group, value in lex.scan(equation)]
        par = Parser(tokens, const, var)
        out.append(par.parseTokens())
        out.append(',')
    out.pop()
    out.append(']')
    ret = ''.join(out)
    print ret
    # Rewrite code including safe locals and globals dict
    #f = lambda x: eval(ret)
    #result = fsolve(f,[1,1])
    #print result
    pass

if __name__=="__main__": main()
