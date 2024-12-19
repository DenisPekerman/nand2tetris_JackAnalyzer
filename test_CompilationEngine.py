import unittest
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
import xml.etree.cElementTree as ET
 


class TestJackTokenizer(unittest.TestCase):
    
    def setUp(self) -> None:
        self.compilationEngine = CompilationEngine('', "temp.xml")
    


    def checkXml(self, node, expected_str):
        ET.indent(node, space="", level=0)
        received_str = ET.tostring(node)

        expected_node = ET.fromstring(expected_str)
        ET.indent(expected_node, space="", level=0)
        expected_fmt_str = ET.tostring(expected_node)

        self.assertEqual(received_str, expected_fmt_str)



    def test_compileReturn(self):
        self.compilationEngine.tokenizer.tokens = ["return", "x", ";"]
        root = ET.Element("test") 
        self.compilationEngine.compileReturn(root)
        expected = """
            <test>
                <return>
                    <keyword>return</keyword>
                    <identifier>x</identifier>
                    <symbol>;</symbol>
                </return>
            </test>
        """

        self.checkXml(root, expected)



    def test_compileDo_empty(self):
        compilationEngine = CompilationEngine('', "temp.xml")
        compilationEngine.tokenizer.tokens = ["do", "someFunc", "(", ")"]
        root = ET.Element("test") 
        compilationEngine.compileDo(root)
        expected = """
            <test>
            <doStatement>
                <keyword>do</keyword>
                <identifier>someFunc</identifier>
                <symbol>(</symbol>
                <expressionList>\n</expressionList>
                <symbol>)</symbol>
                </doStatement>
            </test>
        """

        self.checkXml(root, expected)



    def test_compileDo_one_param(self):
        self.compilationEngine.tokenizer.tokens = ["do", "someFunc", "(", "x", ")"]
        root = ET.Element("test") 
        self.compilationEngine.compileDo(root)
        expected = """
            <test>
            <doStatement>
                <keyword>do</keyword>
                <identifier>someFunc</identifier>
                <symbol>(</symbol>
                <expressionList> 
            <expression>
              <term>
                    <identifier>x</identifier>   
              </term>
            </expression>            
                </expressionList>
                <symbol>)</symbol>
                </doStatement>
            </test>
        """

        self.checkXml(root, expected)



    def test_compileDo_multi_param(self):
        self.compilationEngine.tokenizer.tokens = ["do", "someFunc", "(", "x", ",", "y",
                                                    ",", "3", ")", '{', '}']
        root = ET.Element("test") 
        self.compilationEngine.compileDo(root)
        expected = """
            <test>
            <doStatement>
                <keyword>do</keyword>
                <identifier>someFunc</identifier>
                <symbol>(</symbol>
                <expressionList>
                    <identifier>x</identifier>
                    <symbol>,</symbol>
                    <identifier>y</identifier>
                    <symbol>,</symbol>
                    <int_const>3</int_const>
                </expressionList>
                <symbol>)</symbol>
                </doStatement>
            </test>
        """

        self.checkXml(root, expected)



    def test_compileParameterList(self):
        self.compilationEngine.tokenizer.tokens = ['int', 'y', ',', 'int', 'x', ')' ]
        root = ET.Element("test") 
        self.compilationEngine.compileParameterList(root)
        expected = """
            <test>
            <parameterList>
                <keyword>int</keyword>
                <identifier>y</identifier>
                <symbol>,</symbol>
                <keyword>int</keyword>
                <identifier>x</identifier>
            </parameterList>
            </test>
        """

        self.checkXml(root, expected)



    def test_compileIf_complex(self):
        # if ((x>4) & (y = 8))
        self.compilationEngine.tokenizer.tokens = ['if', '(', '(', 'x', '>', '4', ')', '&', 
                                                   '(', 'y', '=', '8', ')', ')', '{', '}' ]
        root = ET.Element("test") 
        self.compilationEngine.compileParameterList(root)
        expected = """
        <test>
            <ifStatement>
                <keyword>if</keyword>
                <symbol>(</symbol>
                <expression>
                    <term>
                        <symbol>(</symbol>
                        <expression>
                            <term>
                                <identifier>x</identifier>
                            </term>
                            <symbol>></symbol>
                            <term>
                                <integerConstant>4</integerConstant>
                            </term>
                        </expression>
                        <symbol>)</symbol>
                    </term>
                    <symbol>&</symbol>
                    <term>
                        <symbol>(</symbol>
                        <expression>
                            <term>
                                <identifier>y</identifier>
                            </term>
                            <symbol>=</symbol>
                            <term>
                                <integerConstant>8</integerConstant>
                            </term>
                        </expression>
                        <symbol>)</symbol>
                    </term>
                </expression>
                <symbol>)</symbol>
            </ifStatement>
            <symbol>{</symbol>
            <symbol>}</symbol>
        </test>

        """

        self.checkXml(root, expected)

    
    def test_compileIf_simple(self):
        # if (x>4)
        self.compilationEngine.tokenizer.tokens = ['if', '(', 'x', '>', '4', ')'
                                                   , '{', '}']
        root = ET.Element("test") 
        self.compilationEngine.compileIf(root)
        expected = """
        <test>
            <ifStatement>
                <keyword> if </keyword>
                <symbol> ( </symbol>
                <expression>
                    <term>
                        <identifier> x </identifier>
                    </term>
                    <symbol> > </symbol>
                    <term>
                        <integerConstant> 4 </integerConstant>
                    </term>
                </expression>
                <symbol> ) </symbol>
                <symbol> { </symbol>
            <symbol> } </symbol>
            </ifStatement>
        </test>
        """

        self.checkXml(root, expected)



    def test_compileTerm_varName(self):
        self.compilationEngine.tokenizer.tokens = ['x']
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <identifier>x</identifier>
            </term>
        </test>
        """

        self.checkXml(root, expected)


    def test_compileTerm_boolean(self):
        self.compilationEngine.tokenizer.tokens = ['false']
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <keyword>false</keyword>
            </term>
        </test>
        """

        self.checkXml(root, expected)



    def test_compileTerm_listItem(self):
        # x[1+2]
        self.compilationEngine.tokenizer.tokens = ['x', '[', '1', '+', '2', ']'], 
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <identifier>x</identifier>
                <symbol>[</symbol>
                <expression>
                    <term>
                        <integerConstant>1</integerConstant>
                    </term>
                    <symbol>+</symbol>
                    <term>
                        <integerConstant>2</integerConstant>
                    </term>
                </expression>
                <symbol>]</symbol>
            </term>
        </test>
        """

        self.checkXml(root, expected)



    def test_compileTerm_subroutineCall(self):
        # foo(1+2)
        self.compilationEngine.tokenizer.tokens = ['foo', '(', '1', '+', '2', ')'], 
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <identifier>foo</identifier>
                <symbol>(</symbol>
                <expression>
                    <term>
                        <integerConstant>1</integerConstant>
                    </term>
                    <symbol>+</symbol>
                    <term>
                        <integerConstant>2</integerConstant>
                    </term>
                </expression>
                <symbol>)</symbol>
            </term>
        </test>
        """

        self.checkXml(root, expected)



    def test_compileTerm_expression(self):
        self.compilationEngine.tokenizer.tokens = ['(', '1', '+', '2', ')'] 
                                                  
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <symbol>(</symbol>
                <expression>
                    <term>
                        <integerConstant>1</integerConstant>
                    </term>
                    <symbol>+</symbol>
                    <term>
                        <integerConstant>2</integerConstant>
                    </term>
                </expression>
                <symbol>)</symbol>
            </term>
        </test>
        """

        self.checkXml(root, expected)



    def test_compileTerm_unaryOp(self):
        # ~(x)
        self.compilationEngine.tokenizer.tokens = ['~', '(', 'x', ')']                                   
        root = ET.Element("test") 
        self.compilationEngine.compileTerm(root)
        expected = """
        <test>
            <term>
                <symbol>~</symbol>
                <term>
                    <symbol>(</symbol>
                    <expression>
                        <term>
                            <identifier>x</identifier>
                        </term>
                    </expression>
                    <symbol>)</symbol>
                </term>
            </term>
        </test>
        """

        self.checkXml(root, expected)

    
"""
x + 1
x - 1
x/y
x*y
x < y
x > y
x | y
x & y
(x + 3) > y
x[2] > 3
(x+2)*3
~(x)
"""