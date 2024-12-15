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
                    <identifier>x</identifier>                
                </expressionList>
                <symbol>)</symbol>
                </doStatement>
            </test>
        """

        self.checkXml(root, expected)

    def test_compileDo_multi_param(self):
        self.compilationEngine.tokenizer.tokens = ["do", "someFunc", "(", "x", ",", "y", ",", "3", ")"]
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
