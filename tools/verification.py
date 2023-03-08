# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

# Clase verification para evaluación de expresiones correctas
class Verification(object):
    def __init__(self, expression):
        self.expression = expression
    
    # Se retornan los resultados a diferentes pruebas
    def Comprobacion(self):
        ruleA = self.rule_parenthesis()
        ruleB = self.rule_unarios()
        ruleC = self.rule_symbols()
        ruleD = self.rule_kleenes()

        return ruleA, ruleB, ruleC, ruleD
        
    # Regla respecto a los paréntesis
    def rule_parenthesis(self):
        stack = []
        missing_parentheses = []
        for i, c in enumerate(self.expression):
            if c == '(':
                stack.append(i)
            elif c == ')':
                if not stack:
                    missing_parentheses.append(i)
                else:
                    stack.pop()
        missing_parentheses.extend(stack)
        if not missing_parentheses:
            return [True, 'Todo correcto', [], 'A']
        else:
            message = 'Falta uno o más paréntesis'
            return [False, message, missing_parentheses, 'A']
     
    # Regla respecto a los operadores unarios   
    def rule_unarios(self):
        message = ""
        indices = []
        
        for i in range(len(self.expression)):
            
            if (self.expression[-1] == '|' and self.expression[-2] != '|'):
                return [False, 'No se puede realizar este or', [len(self.expression)], 'B']
            
            if (i+1 < len(self.expression)):
                if (self.expression[i] == '|' and self.expression[i+1] == '|'):
                    message = "No pueden haber dos or's seguidos"
                    if(i not in indices and i+1 not in indices):
                        indices.append(i)
                        indices.append(i+1)   
                    
                if (i-1 >= 0):
                    if (self.expression[i] == '|'):
                        if (not (self.expression[i-1] not in '|' and self.expression[i+1] not in '?*+|')):
                            message = "No se puede realizar esta operación en el or"
                            return [False, message, self.expression, 'B']
        
        if(not indices):
            return [True, 'Todo correcto', [], 'B']
        else:
            return [False, message, indices, 'B']
    
    # Regla respecto al alfabeto    
    def rule_symbols(self):
        symbols = set("?*()+|")
        if all(c in symbols for c in self.expression):
            return [False, 'No hay símbolos del alfabeto', self.expression, 'C']
        else:
            return [True, 'Todo correcto', [], 'C']
    
    # Regla respecto a las cerraduras  
    def rule_kleenes(self):
        message = ""
        indices = []
        
        for i in range(len(self.expression)):
            if (i == 0):
                if (self.expression[i] in ')|*+.'):
                    message = "No se puede iniciar con este símbolo"
                    if(i not in indices):
                        indices.append(i)
            
            if (i-1 >= 0):
                if (self.expression[i-1] in '|(' and self.expression[i] in '*?+'):
                    message = "No se puede realizar esta operación"
                    if(i not in indices and i-1 not in indices):
                        indices.append(i-1)  
                        indices.append(i)
                
            if (i+1 < len(self.expression)):
                if (self.expression[i] in '+?*'):
                    posterior = self.expression[i+1]
                    if (posterior in '()' or posterior not in '().'):
                        continue
                    else:
                        message = "No se puede realizar esta operación"
                        if(i not in indices and i+1 not in indices):
                            indices.append(i)
                            indices.append(i+1)
                    
        if(not indices):
            return [True, 'Todo correcto', [], 'D']
        else:
            return [False, message, indices, 'D']
        