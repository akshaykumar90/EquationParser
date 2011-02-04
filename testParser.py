from Lexer import Lexer
from Parser import Parser, AmbiguousIdentifierError, MalformedEquationError
import nose.tools
from math import *

class TestParser():
    @classmethod
    def setupClass(self):
        rules = {
            "Function": r"(exp|log|log10|acos|asin|atan|cos|sin|tan|cosh|sinh|tanh)\(",
            "Number": r"\d+(\.\d+)?",
            "Operator": r"[-+()*^]", 
        }
        self.lex = Lexer(rules)
        pass
    def TestKnownValues(self):
        """ Tests some equations by comparing output to known results """
        v = ['log']
        c = {'exp':'1'}
        tokens = [(group,value) for group, value in self.lex.scan('expexp(exp)explog10(exp(log))')]
        par = Parser(tokens, c, v)
        assert par.parseTokens() == '1*exp(1)*1*log10(exp(x[0]))'
        
        v = ['x']
        c = {}
        tokens = [(group,value) for group, value in self.lex.scan('sin(x)^-2+(cos(x))^2-1')]
        par = Parser(tokens, c, v)
        assert par.parseTokens() == 'sin(x[0])**-2+(cos(x[0]))**2-1'
        
        v = ['x','y','z']
        c = {'a':'1.67e-5','b':'8'}
        tokens = [(group,value) for group, value in self.lex.scan('aexp(bx+xy) + sin(z)log(by)*5')]
        par = Parser(tokens, c, v)
        assert par.parseTokens() == '1.67e-5*exp(8*x[0]+x[0]*x[1])+sin(x[2])*log(8*x[1])*5'
    
    def TestEvalExpressions(self):
        """ Tests that the expressions are evaluated successfully by eval() without
        raising any exceptions 
        """
        var = ['x','y','u','v']
        const = {'a':'0.25','b':'1','c':'2.6','asinc':'8'}
        tokens = [(group,value) for group, value in self.lex.scan('a*sin(bx+cy-xy+exp(uv))asin(a*sin(asinc+asin(0.01cy)))+tan(log10(10))')]
        par = Parser(tokens, const, var)
        x = [1,1,1,1]
        eval(par.parseTokens())
        
        var = ['t','theta']
        const = {'a':'1.8','k':'16','c':'1','azm':'1'}
        tokens = [(group,value) for group, value in self.lex.scan('atan(aexp(-kt))+cktsin(azm*theta)')]
        par = Parser(tokens, const, var)
        x = [1,1]
        eval(par.parseTokens())
        
    @nose.tools.raises(MalformedEquationError)
    def TestUnbalancedBrackets(self):
        """ Tests that an equation with unbalanced brackets is flagged as Malformed Equation """
        test_eqn = [
            "21a*sin(bx+(cy+dz)",
            "100log(ccos(xy+yz))+23(34)tan(exp(2x)",
            "sin(x)^(-2x+3y+aexp(-kt)"
        ]
        var = ['x','y','z','t']
        const = {'a':'1','b':'1','c':'1','d':'1','k':'1'}
        for eqn in test_eqn:
            tokens = [(group,value) for group, value in self.lex.scan(eqn)]
            par = Parser(tokens, const, var)
            par.parseTokens()
            
    def TestOperatorArrangement(self):
        """ Tests that an equation with illegal operator arrangement is flagged as Malformed Equation """
        test_eqn = [
            "2x^-4*sin(exp())", #Zero arguments to exp()
            "sin(ax+-by+cz)",
            "dlog(x)*23sin(y*)",
            "12x(y^3)+23(^0.5)tan(y)"
        ]
        var = ['x','y','z']
        const = {'a':'1','b':'1','c':'1','d':'1'}
        for eqn in test_eqn:
            tokens = [(group,value) for group, value in self.lex.scan(eqn)]
            par = Parser(tokens, const, var)
            nose.tools.assert_raises(MalformedEquationError, par.parseTokens)
            
    def TestIdentifier(self):
        """ Tests that the identifiers are properly parsed and ambiguous identifiers raise error """
        const = {'b':'1','bat':'2'}
        var = ['attr']
        tokens = [(group,value) for group, value in self.lex.scan('battrexp(x)+log(bat^x)')]
        par = Parser(tokens, const, var)
        nose.tools.assert_raises(AmbiguousIdentifierError, par.parseTokens)
        
        const = {'p':'3'}
        var = ['rice','price']
        tokens = [(group,value) for group, value in self.lex.scan('plog(rice)+price*rice')]
        par = Parser(tokens, const, var)
        par.parseTokens()
        
        const = {'b':'1','a':'2', 'bet':'3'}
        var = ['x','eta']
        tokens = [(group,value) for group, value in self.lex.scan('2betalog(x)+bet*a+b*etaexp(eta)')]
        par = Parser(tokens, const, var)
        nose.tools.assert_raises(AmbiguousIdentifierError, par.parseTokens)
        
class TestLinearEquation():
    @classmethod
    def setupClass(self):
        rules = {
        "Number": r"\d+(\.\d+)?",
        "Operator": r"[-+()*]", 
        }
        self.lex = Lexer(rules, False)
        pass
    def TestKnownValues(self):
        """ Tests some linear equation by testing against known output """
        var = ['Cost','PaintA','PaintB','PaintC','Quantity']
        
        tokens = [(group,value) for group, value in self.lex.scan("2PaintA+3PaintB-0.5Cost")]
        par = Parser(tokens, {}, var)
        assert par.parseLinearEquation() == [(2, 1), (3, 2), (-0.5, 0)]
        
        tokens = [(group,value) for group, value in self.lex.scan("5Cost*3.1+(-2)8*Quantity-(-8)PaintA")]
        par = Parser(tokens, {}, var)
        assert par.parseLinearEquation() == [(15.5, 0), (-16, 4), (8, 1)]
        
        tokens = [(group,value) for group, value in self.lex.scan("2(1+0.5)PaintA+33*Quantity-13Cost*(2.5+1)")]
        par = Parser(tokens, {}, var)
        assert par.parseLinearEquation() == [(3.0, 1), (33, 4), (-45.5, 0)]
        
    def TestNonLinearEquations(self):
        """ Tests that non-linear equations are flagged as Malformed Equation """
        var = ['x','y','z']
        test_eqn = [
            "2xy+y-3z",
            "2x+3xyz-8z",
            "x-y-xy+2z"
        ]
        for eqn in test_eqn:
            tokens = [(group,value) for group, value in self.lex.scan(eqn)]
            par = Parser(tokens, {}, var)
            nose.tools.assert_raises(MalformedEquationError, par.parseLinearEquation)
            
    def TestImproperBrackets(self):
        """ Tests that improperly placed brackets in the equation raises MalformedEquationError 
        Though mathematically correct, for the function to work, brackets must be properly placed
        and should not envelop more than one variable"""
        var = ['x','y','z']
        test_eqn = [
            "(2x+y)-3z",
            "(2*4x-(-3)y)-8z",
        ]
        for eqn in test_eqn:
            tokens = [(group,value) for group, value in self.lex.scan(eqn)]
            par = Parser(tokens, {}, var)
            nose.tools.assert_raises(MalformedEquationError, par.parseLinearEquation)
        