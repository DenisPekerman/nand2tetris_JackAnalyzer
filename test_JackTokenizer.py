import unittest
from JackTokenizer import JackTokenizer


class TestJackTokenizer(unittest.TestCase):
    
    def setUp(self) -> None:
        self.jackTokenizer = JackTokenizer('')
        # return super().setUp()
    

    def test_tokenTypeAndValue_keyword(self):
        token = "class"
        result = self.jackTokenizer.tokenTypeAndValue(token)
        self.assertEqual(result, ("keyword", "class"))


    def test_tokenTypeAndValue_symbol(self):
        token = '>'
        result = self.jackTokenizer.tokenTypeAndValue(token)
        self.assertEqual(result, ("symbol", '>'))

    
    def test_tokenTypeAndValue_intConst(self):
        token = '5543'
        result = self.jackTokenizer.tokenTypeAndValue(token)
        self.assertEqual(result, ("int_const", '5543'))

    
    def test_tokenTypeAndValue_strConst(self):
        token = '"yabadabadu"'
        result = self.jackTokenizer.tokenTypeAndValue(token)
        self.assertEqual(result, ("str_const", '"yabadabadu"'))


    def test_tokenTypeAndValue_identifier(self):
        token = 'yaba_dabadu5'
        result = self.jackTokenizer.tokenTypeAndValue(token)
        self.assertEqual(result, ("identifier", 'yaba_dabadu5'))

    def test_init_empty(self):
        actual_tokens = self.jackTokenizer.tokens
        self.assertEqual(actual_tokens, [])


    # def test_init(self):
    #     expected_tokens = [
    #         "class", "Main", "{",
    #         "static", "boolean", "test", ";",
    #         "function", "void", "func", "(", "int", "y", ")", "{",
    #         "var", "SquareGame", "game", ";",
    #         "var", "int", "x", ";",
    #         "if", "(", "x", ">", "1", ")", "{",
    #         "let", "y", "=", "0", ";",
    #         "}",
    #         "do", "game", ".", "dispose", "(", ")", ";",
    #         "return", ";",
    #         "}",
    #         "}"
    #     ]
    #     actual_tokens = self.jackTokenizer.tokens
    #     self.assertEqual(actual_tokens, expected_tokens)

    
    def test_hasMoreTokens_true(self):
        self.jackTokenizer.tokens = ['class', 'Main', '{']
        has_more_tokens = self.jackTokenizer.hasMoreTokens()
        self.assertEqual(has_more_tokens, True)
    

    def test_hasMoreTokens_false(self):
        self.jackTokenizer.tokens = []
        has_more_tokens = self.jackTokenizer.hasMoreTokens()
        self.assertEqual(has_more_tokens, False)


    def test_advance(self):
        self.jackTokenizer.tokens = ['class', 'Main', '{']
        x = self.jackTokenizer.advance()
        self.assertEqual(x[1], 'class')
        x = self.jackTokenizer.advance()
        self.assertEqual(x[1], 'Main')
        x = self.jackTokenizer.advance()
        self.assertEqual(x[1], '{')
        self.jackTokenizer.tokens = []
        x = self.jackTokenizer.advance()
        self.assertEqual(x, None)
        
    def test_peek(self):
        self.jackTokenizer.tokens = ['class', 'Main', '{']
        self.assertEqual(self.jackTokenizer.peek(), 'class')
        self.assertEqual(self.jackTokenizer.peek(), 'class')

    def test_peek_empty(self):
        self.jackTokenizer.tokens = []
        self.assertEqual(self.jackTokenizer.peek(), None)
