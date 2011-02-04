import re

class AmbiguousIdentifierError(Exception):
    def __init__(self, ident):
        self.ident = ident
 
    def __str__(self):
        return "Ambiguous Identifier: %s" % (self.ident)

class MalformedEquationError(Exception):
    def __init__(self, eqn):
        self.eqn = eqn
 
    def __str__(self):
        return "Malformed Equation: %s" % (self.eqn)

class Parser(object):
    def __init__(self, tokens, const, var):
        self.tokens = tokens
        self.const = const #Mapping of string to string, constant name to constant value in string
        self.var = var
        self.keys = const.keys()
        if len(self.keys) > 0:
            self.keys.sort(lambda x, y: len(x)-len(y))
        pass

    def parseIdentifier(self, ident):
        out = '' # Return String
        
        temp = [0 for i in range (len(ident))]

        # Find all the constants present
        for c in self.keys:
            if (len(c) <= len(ident)):
                t = ident.find(c) #Case-sensitive search
                if t != -1:
                    for j in range(t,t+len(c)):
                        temp[j]='C' + str(self.keys.index(c))
            else:
                break

        # Find all the variables present
        for v in self.var:
            if (len(v) <= len(ident)):
                t = ident.find(v) #Case-sensitive search
                if t != -1:
                    for j in range(t,t+len(v)):
                        temp[j]='V'+str(self.var.index(v))
            else:
                break

        # Look for any possible conflicts
        ch = temp[0]
        k = 1
        l = 1
        while k < len(temp):
            if temp[k] == ch:
                l += 1
                k += 1
                continue
            if ch[0] == 'C':
                if l == len(self.keys[int(ch[1:])]):
                    out += self.const[self.keys[int(ch[1:])]] + '*'
                else:
                    raise AmbiguousIdentifierError(ident)
            else:
                if l == len(self.var[int(ch[1:])]):
                    out += 'x[' + ch[1:] + ']*'
                else:
                    raise AmbiguousIdentifierError(ident)
            ch = temp[k]
            k += 1
            l = 1
        else:
            if ch[0] == 'C':
                if l == len(self.keys[int(ch[1:])]):
                    out += self.const[self.keys[int(ch[1:])]] + '*'
                else:
                    raise AmbiguousIdentifierError(ident)
            else:
                if l == len(self.var[int(ch[1:])]):
                    out += 'x[' + ch[1:] + ']*'
                else:
                    raise AmbiguousIdentifierError(ident)

        return out[:-1] # Don't return the trailing '*'

    def parseTokens(self):
        brackets = 0
        outStr = [] # Final Output
        
        ident='' # Identifier
        i=0
        for group, value in self.tokens:
            if group == "Unknown":
                ident += value
                i += 1
                continue
            
            # call group handler function
            if len(ident) > 0:
                if group != "Operator":
                    outStr.append(self.parseIdentifier(ident)+'*')
                else:
                    outStr.append(self.parseIdentifier(ident))
                ident=''
            if group == "Function":
                brackets += 1
                outStr.append(value)
            elif group == "Operator":
                if i > 0 and (self.tokens[i-1])[0] == "Operator":
                    if (value == '+' and (self.tokens[i-1])[1] == '-') or \
                       (value == '-' and (self.tokens[i-1])[1] == '+') or \
                       (value == '*' and (self.tokens[i-1])[1] != ')') or \
                       (value == '^' and (self.tokens[i-1])[1] != ')') or \
                       (value == ')' and (self.tokens[i-1])[1] != ')'):
                        eqnlist = [v for g,v in self.tokens]
                        eqn = ''.join(eqnlist)
                        raise MalformedEquationError(eqn)
                if i > 0 and (self.tokens[i-1])[0] == "Function":
                    if value == '*' or value == '^' or value == ')':
                        eqnlist = [v for g,v in self.tokens]
                        eqn = ''.join(eqnlist)
                        raise MalformedEquationError(eqn)
                if value == '^':
                    outStr.append('**')
                elif value == '(':
                    brackets += 1
                    outStr.append(value)
                elif value == ')':
                    brackets -= 1
                    if i+1 < len(self.tokens) and (self.tokens[i+1])[0] != "Operator":
                        outStr.append(value+'*')
                    else:
                        outStr.append(value)
                else:
                    outStr.append(value)
            else: #Number
                outStr.append(value)
                if i+1 < len(self.tokens):
                    if (self.tokens[i+1])[0] != "Operator":
                        outStr.append('*')
                    elif (self.tokens[i+1])[1] == "(":
                        outStr.append('*')
            i += 1
        
        if len(ident)>0:
            outStr.append(self.parseIdentifier(ident))
            
        if brackets != 0:
            eqnlist = [v for g,v in self.tokens]
            eqn = ''.join(eqnlist)
            raise MalformedEquationError(eqn)
            
        return ''.join(outStr)
    
    def parseLinearEquation(self):
        out = [] # Output: List of Tuples (coefficient, index)
        pattern = re.compile(r'x\[(\d+)\]')
        bracketCount = 0
        equation = []
        chunk = []
        for group, value in self.tokens:
            if (value == '+' or value == '-') and bracketCount == 0 and len(chunk) > 0:
                equation.append(chunk)
                chunk = []
            if value == '(':
                bracketCount += 1
            if value == ')':
                bracketCount -= 1
            chunk.append((group,value))
        equation.append(chunk)
        for chunk in equation:
            self.tokens = chunk
            temp = self.parseTokens()
            expr,cnt = pattern.subn('1',temp)
            if (cnt > 1):
                eqnlist = [v for g,v in self.tokens]
                eqn = ''.join(eqnlist)
                raise MalformedEquationError(eqn)
            out.append((eval(expr),int(pattern.search(temp).group(1))))
        return out