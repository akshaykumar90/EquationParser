from Lexer import Lexer
import re

class TestLexer():
    rules = {
        "Function": r"(exp|log|log10|acos|asin|atan|cos|sin|tan|cosh|sinh|tanh)\(",
        "Number": r"\d+(\.\d+)?",
        "Operator": r"[-+()*^]", 
    }
    
    def TestSimpleEquations(self):
        """ Testing some simple equations:"""
        
        equations = [
            "2x+3y-5z-15",
            "PaintA^2 + PaintB^3 - 100",
            "x^2-y^2-6",
            "aexp(bx) - 10"
        ]
        expectedOutput = [
            [('Number', '2'), 
             ('Unknown', 'x'), 
             ('Operator', '+'), 
             ('Number', '3'), 
             ('Unknown', 'y'), 
             ('Operator', '-'), 
             ('Number', '5'), 
             ('Unknown', 'z'), 
             ('Operator', '-'), 
             ('Number', '15')],
            [('Unknown', 'P'), 
             ('Unknown', 'a'), 
             ('Unknown', 'i'), 
             ('Unknown', 'n'), 
             ('Unknown', 't'), 
             ('Unknown', 'A'), 
             ('Operator', '^'), 
             ('Number', '2'), 
             ('Operator', '+'), 
             ('Unknown', 'P'), 
             ('Unknown', 'a'), 
             ('Unknown', 'i'), 
             ('Unknown', 'n'), 
             ('Unknown', 't'), 
             ('Unknown', 'B'), 
             ('Operator', '^'), 
             ('Number', '3'), 
             ('Operator', '-'), 
             ('Number', '100')],
            [('Unknown', 'x'), 
             ('Operator', '^'), 
             ('Number', '2'), 
             ('Operator', '-'), 
             ('Unknown', 'y'), 
             ('Operator', '^'), 
             ('Number', '2'), 
             ('Operator', '-'), 
             ('Number', '6')],
            [('Unknown', 'a'), 
             ('Function', 'exp('), 
             ('Unknown', 'b'), 
             ('Unknown', 'x'), 
             ('Operator', ')'), 
             ('Operator', '-'), 
             ('Number', '10')]
        ]
        
        lex = Lexer(self.rules)
        for eqn in equations:
            out = [(g,v) for g,v in lex.scan(eqn)]
            assert out == expectedOutput.pop(0)
        pass
    
    def TestComplexEquations(self):
        """ Testing some complex equations """
        
        equations = [
            "expexp(exp)explog10(exp(log))",
            "10log10(10*10*log10(log*1o(log(10))))", #Notice the 6th 10 is actually 1 and 'o'
            "a*sin(bx+cy-xy+exp(uv))asin(a*sin(asin+asin(cy)))+tan(log10(10))",
            "pricexp(expensesexp(expenses))",
            "sin(x)^2 + (cos(x))^2 - 1"
        ]
        expectedOutput = [
            [('Unknown', 'e'), 
             ('Unknown', 'x'), 
             ('Unknown', 'p'), 
             ('Function', 'exp('), 
             ('Unknown', 'e'), 
             ('Unknown', 'x'), 
             ('Unknown', 'p'), 
             ('Operator', ')'), 
             ('Unknown', 'e'), 
             ('Unknown', 'x'), 
             ('Unknown', 'p'), 
             ('Function', 'log10('), 
             ('Function', 'exp('), 
             ('Unknown', 'l'), 
             ('Unknown', 'o'), 
             ('Unknown', 'g'), 
             ('Operator', ')'), 
             ('Operator', ')')],
            [('Number', '10'),
             ('Function', 'log10('),
             ('Number', '10'),
             ('Operator', '*'),
             ('Number', '10'),
             ('Operator', '*'),
             ('Function', 'log10('),
             ('Unknown', 'l'),
             ('Unknown', 'o'),
             ('Unknown', 'g'),
             ('Operator', '*'),
             ('Number', '1'),
             ('Unknown', 'o'),
             ('Operator', '('),
             ('Function', 'log('),
             ('Number', '10'),
             ('Operator', ')'),
             ('Operator', ')'),
             ('Operator', ')'),
             ('Operator', ')')],
            [('Unknown', 'a'),
             ('Operator', '*'),
             ('Function', 'sin('),
             ('Unknown', 'b'),
             ('Unknown', 'x'),
             ('Operator', '+'),
             ('Unknown', 'c'),
             ('Unknown', 'y'),
             ('Operator', '-'),
             ('Unknown', 'x'),
             ('Unknown', 'y'),
             ('Operator', '+'),
             ('Function', 'exp('),
             ('Unknown', 'u'),
             ('Unknown', 'v'),
             ('Operator', ')'),
             ('Operator', ')'),
             ('Function', 'asin('),
             ('Unknown', 'a'),
             ('Operator', '*'),
             ('Function', 'sin('),
             ('Unknown', 'a'),
             ('Unknown', 's'),
             ('Unknown', 'i'),
             ('Unknown', 'n'),
             ('Operator', '+'),
             ('Function', 'asin('),
             ('Unknown', 'c'),
             ('Unknown', 'y'),
             ('Operator', ')'),
             ('Operator', ')'),
             ('Operator', ')'),
             ('Operator', '+'),
             ('Function', 'tan('),
             ('Function', 'log10('),
             ('Number', '10'),
             ('Operator', ')'),
             ('Operator', ')')],
            [('Unknown', 'p'),
             ('Unknown', 'r'),
             ('Unknown', 'i'),
             ('Unknown', 'c'),
             ('Function', 'exp('),
             ('Unknown', 'e'),
             ('Unknown', 'x'),
             ('Unknown', 'p'),
             ('Unknown', 'e'),
             ('Unknown', 'n'),
             ('Unknown', 's'),
             ('Unknown', 'e'),
             ('Unknown', 's'),
             ('Function', 'exp('),
             ('Unknown', 'e'),
             ('Unknown', 'x'),
             ('Unknown', 'p'),
             ('Unknown', 'e'),
             ('Unknown', 'n'),
             ('Unknown', 's'),
             ('Unknown', 'e'),
             ('Unknown', 's'),
             ('Operator', ')'),
             ('Operator', ')')],
            [('Function', 'sin('),
             ('Unknown', 'x'),
             ('Operator', ')'),
             ('Operator', '^'),
             ('Number', '2'),
             ('Operator', '+'),
             ('Operator', '('),
             ('Function', 'cos('),
             ('Unknown', 'x'),
             ('Operator', ')'),
             ('Operator', ')'),
             ('Operator', '^'),
             ('Number', '2'),
             ('Operator', '-'),
             ('Number', '1')]
        ]
        lex = Lexer(self.rules)
        for eqn in equations:
            out = [(g,v) for g,v in lex.scan(eqn)]
            assert out == expectedOutput.pop(0)
        pass
    
    def TestFunctionPriority(self):
        """ Function names must be given top preference
            Equations snippets to check:
                exp(check)
                log10(tx)
                sin(ccos(y))
                eexp(22)
        """
        lex = Lexer(self.rules)
        assert [(g,v) for g,v in lex.scan("exp(check)")].pop(0) == ('Function', 'exp(')
        assert [(g,v) for g,v in lex.scan("log10(tx)")].pop(0) == ('Function', 'log10(')
        dualFunc = [(g,v) for g,v in lex.scan("sin(ccos(y))")]
        assert dualFunc[0] == ('Function', 'sin(')
        assert dualFunc[2] == ('Function', 'cos(')
        assert [(g,v) for g,v in lex.scan("eexp(22)")][1] == ('Function', 'exp(')
        pass
    
    def TestVariablesNaming(self):
        """ Numeric unknowns must be preceded by alphabetic unknowns
        can also be phrased as,
        variable names cannot begin with numerical digit.
        Equations to test:
        23x15sin(zy12*100u) + AF1atan(99c)
        """
        lex = Lexer(self.rules)
        test = []
        for g,v in lex.scan("23x15sin(zy12*100u) + AF1atan(99c)"):
            if g == 'Unknown' and re.match(r"\d+(\.\d+)?", v):
                assert test[-1][0] == 'Unknown' and re.match(r"^[_a-zA-Z]$",test[-1][1])
            test.append((g,v))
        pass
    
    def TestNumbersTokens(self):
        """ Numeric constants cannot appear immediately after unknowns.
        They must be seperated by either * or () or any other operator
        In other words:
        Numerical constants must not be preceded by unknowns.
        They can follow only after operator or functions.
        Equation to test:
        12xy2*15cz(2.54) + tan(23y)18c19(0.01)
        """
        lex = Lexer(self.rules)
        test = []
        for g,v in lex.scan("12xy2*15cz(2.54) + tan(23y)18c19(0.01)"):
            if g == 'Number':
                if len(test) > 0:
                    assert test[-1] != 'Unknown'
            test.append((g,v))
        pass
    
    def TestCaseInsensitivity(self):
        """ Function names should be case-insensitive
        exp() = Exp() = EXP()
        Equations to test:
        aExp(bX) + SIN(theta) + cos(z)
        dLog(LOG(x)) + hcosH(y)
        """
        lex = Lexer(self.rules, False)
        t1 = [(g,v) for g,v in lex.scan("aExp(bX) + SIN(theta) + cos(z)")]
        assert t1[1] == ('Function', 'Exp(')
        assert t1[6] == ('Function', 'SIN(')
        assert t1[14] == ('Function', 'cos(')
        t2 = [(g,v) for g,v in lex.scan("dLog(LOG(x)) + hcosH(y)")]
        assert t2[1] == ('Function', 'Log(')
        assert t2[2] == ('Function', 'LOG(')
        assert t2[8] == ('Function', 'cosH(')
        pass
        