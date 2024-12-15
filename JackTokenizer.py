import re

class JackTokenizer:

    KeywordsCodes = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
    SymbolsCodes = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '<', '>', '=', '~']

    keyword_Pattern = '(?!\w)|'.join(KeywordsCodes) + '(?!\w)'
    symbol_pattern = '[' + re.escape('|'.join(SymbolsCodes)) + ']'
    int_pattern = r'\d+'
    str_pattern = r'"[^"\n]*"'
    identifier_pattern = r'[a-zA-Z_]\w*'
    token = re.compile(keyword_Pattern + '|' + symbol_pattern + '|' + int_pattern + '|' + str_pattern + '|' + identifier_pattern)
    

    def __init__(self, input_file: str):
        self.currentToken = ""

        self.data = ''
        if input_file:
            self.input_file = open(input_file, "r")
            self.data = self.input_file.read()

        self.data = re.sub(r'(//.*|/\*[\s\S]*?\*/)', '\n', self.data)   # remove all comments 
        self.data = self.data.strip()
        self.tokens = self.findAllTokens(self.data) # Find all tokens

        
        
    def tokenTypeAndValue(self, tokenValue):
        if re.match(self.keyword_Pattern, tokenValue) is not None:
            return ("keyword", tokenValue)
        elif re.match(self.symbol_pattern, tokenValue) is not None:
            return ("symbol", tokenValue)
        elif re.match(self.int_pattern, tokenValue) is not None:
            return ("int_const", tokenValue)
        elif re.match(self.str_pattern, tokenValue) is not None:
            return ("str_const", tokenValue)
        elif re.match(self.identifier_pattern, tokenValue) is not None:
            return ("identifier", tokenValue)
    

    def replaceSymbol(self, input_tuple):
        tokenType, tokenValue = input_tuple
        if tokenValue == '<': 
            return (tokenType, '&lt;')
        elif tokenValue == '>': 
            return (tokenType, '&gt;')
        elif tokenValue == '"': 
            return (tokenType, '&quot;')
        elif tokenValue == '&': 
            return (tokenType, '&amp;')
        else:              
            return (tokenType, tokenValue)
        

    def findAllTokens(self, data):
        return self.token.findall(data)


    def hasMoreTokens(self):
        return len(self.tokens) > 0


    def advance(self):
        if self.hasMoreTokens(): 
            self.currentToken = self.tokens.pop(0)
        else:
            self.currentToken = None
        return self.tokenTypeAndValue(self.currentToken) if self.currentToken else None


    def peek(self, index: int = 0):
        return self.tokens[index] if self.tokens else None
         
        




