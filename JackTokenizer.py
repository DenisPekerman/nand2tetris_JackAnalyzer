import re

class JackTokenizer:

    KeywordsCodes = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                     "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
    SymbolsCodes = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '<', '>', '=', '~']

    keyword_Pattern = '(?!\w)|'.join(KeywordsCodes) + '(?!\w)'
    symbol_pattern = '[' + re.escape('|'.join(SymbolsCodes)) + ']'
    int_pattern = r'\d+'
    str_pattern = r'"[^"\n]*"'
    identifier_pattern = r'[a-zA-Z_]\w*'
    token = re.compile(keyword_Pattern + '|' + symbol_pattern + '|' + int_pattern + '|' + str_pattern + '|' + identifier_pattern)
    

    def __init__(self, input_file):
        self.input_file = open(input_file, "r")
        self.currentToken = ""

        self.data = self.input_file.read()
        self.data = re.sub(r'(//.*|/\*[\s\S]*?\*/)', '\n', self.data)   # remove all comments 
        self.data = self.data.strip()

        self.tokens = self.splitTokens(self.data)
        # replaces <,>,=,&
        for i, token in enumerate(self.tokens): 
            token_type, token_value = self.tokenTypeAndValue(token)
            if token_type == "SYMBOL":
                _, tValue = self.replaceSymbol((token_type, token_value))
                self.tokens[i] = tValue

        
        
    def tokenTypeAndValue(self, tokenValue):
        if re.match(self.keyword_Pattern, tokenValue) != None:
            return ("KEYWORD", tokenValue)
        elif re.match(self.symbol_pattern, tokenValue) != None:
            return ("SYMBOL", tokenValue)
        elif re.match(self.int_pattern, tokenValue) != None:
            return ("INT_CONST", tokenValue)
        elif re.match(self.str_pattern, tokenValue) != None:
            return ("STR_CONST", tokenValue)
        elif re.match(self.identifier_pattern, tokenValue) != None:
            return ("IDENTIFIER", tokenValue)
    

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


    def splitTokens(self, data):
        return self.token.findall(data)


    def hasMoreTokens(self):
        return len(self.tokens) > 0


    def advance(self):
        if self.hasMoreTokens(): 
            self.currentToken = self.tokens.pop(0)
        else:
            self.currentToken = None
        return self.currentToken





