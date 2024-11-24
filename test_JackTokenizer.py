import unittest
from JackTokenizer import JackTokenizer


class TestJackTokenizer(unittest.TestCase):
    
    def setUp(self) -> None:
        self.jackTokenizer = JackTokenizer("/Users/denispek/Projects/coursera/nand2tetris/part_2/JackAnalyzer/test.jack")
        # return super().setUp()
    

    def test_tokenTypeAndValue_keyword(self):
        token = "class"
        result = self.jackTokenizer.tokenTypeAndValue(token)
        self.assertEqual(result, ("KEYWORD", "class"))


    def test_tokenTypeAndValue_symbol(self):
        token = '>'
        result = self.jackTokenizer.tokenTypeAndValue(token)
        self.assertEqual(result, ("SYMBOL", '>'))

    
    def test_tokenTypeAndValue_intConst(self):
        token = '5543'
        result = self.jackTokenizer.tokenTypeAndValue(token)
        self.assertEqual(result, ("INT_CONST", '5543'))

    
    def test_tokenTypeAndValue_strConst(self):
        token = '"yabadabadu"'
        result = self.jackTokenizer.tokenTypeAndValue(token)
        self.assertEqual(result, ("STR_CONST", '"yabadabadu"'))


    def test_tokenTypeAndValue_identifier(self):
        token = 'yaba_dabadu5'
        result = self.jackTokenizer.tokenTypeAndValue(token)
        self.assertEqual(result, ("IDENTIFIER", 'yaba_dabadu5'))


    def test_init(self):
        expected_tokens = [
            "class", "Main", "{",
            "static", "boolean", "test", ";",
            "function", "void", "func", "(", "int", "y", ")", "{",
            "var", "SquareGame", "game", ";",
            "var", "int", "x", ";",
            "if", "(", "x", "&gt;", "1", ")", "{",
            "let", "y", "=", "0", ";",
            "}",
            "do", "game", ".", "dispose", "(", ")", ";",
            "return", ";",
            "}",
            "}"
        ]
        actual_tokens = self.jackTokenizer.tokens
        self.assertEqual(actual_tokens, expected_tokens)

    
    def test_hasMoreTokens_true(self):
        has_more_tokens = self.jackTokenizer.hasMoreTokens()
        self.assertEqual(has_more_tokens, True)
    

    def test_hasMoreTokens_false(self):
        self.jackTokenizer.tokens = []
        has_more_tokens = self.jackTokenizer.hasMoreTokens()
        self.assertEqual(has_more_tokens, False)


    def test_advance(self):
        x = self.jackTokenizer.advance()
        self.assertEqual(x, 'class')
        x = self.jackTokenizer.advance()
        self.assertEqual(x, 'Main')
        x = self.jackTokenizer.advance()
        self.assertEqual(x, '{')
        self.jackTokenizer.tokens = []
        x = self.jackTokenizer.advance()
        self.assertEqual(x, None)
        
        