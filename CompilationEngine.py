from JackTokenizer import JackTokenizer
import xml.etree.cElementTree as ET

class CompilationEngine:
    def __init__(self, input, output):
        """Initializes a new compilation engine."""
        self.tokenizer = JackTokenizer(input)
        self.output_file = open(output, 'w')
        


        # while tokenizer.hasMoreTokens():
        #     token = tokenizer.advance()
        #     print(token)

    def compileClass(self):
        """
        Compiles a complete class.
        """
        class_token = self.tokenizer.advance()
        class_token = self.tokenizer.tokenTypeAndValue(class_token)
        class_name = self.tokenizer.advance()
        class_name = self.tokenizer.tokenTypeAndValue(class_token)
        braket = self.tokenizer.advance()
        braket = self.tokenizer.tokenTypeAndValue(class_token)
        # TODO: verify
        self.root = ET.Element("class") 
        ET.SubElement(self.root, class_token[0]).text = class_token[1]
        ET.SubElement(self.root, class_name[0]).text = class_name[1]
        ET.SubElement(self.root, braket[0]).text = braket[1]


        pass

    def compileClassVarDec(self):
        """
        Compiles static variable declaration or a field declaration.
        """
        # Handles variable declarations at the class level.
        pass

    def compileSubroutine(self):
        """
        Compiles a complete method, function, or constructor.
        """
        # Creates methods, functions, or constructors.
        pass

    def compileParameterList(self):
        """
        Compiles (possibly empty) parameter list.
        Does not handle the enclosing parentheses tokens ( ).
        """
        # Parses a list of parameters for a subroutine.
        pass

    def compileSubroutineBody(self):
        """
        Compiles a subroutine's body.
        """
        # Processes the subroutine body including statements.
        pass

    def compileVarDec(self):
        """
        Compiles a variable declaration.
        """
        # Handles local variable declarations inside subroutines.
        pass

    def compileStatements(self):
        """
        Compiles a sequence of statements.
        Does not handle the enclosing curly bracket tokens { }.
        """
        # Processes statements inside subroutine or block bodies.
        pass

    def compileLet(self):
        """
        Compiles a let statement.
        """
        # Handles assignment statements in Jack.
        pass

    def compileIf(self):
        """
        Compiles an if statement, possibly with a trailing else clause.
        """
        # Handles conditional branching logic.
        pass

    def compileWhile(self):
        """
        Compiles a while statement.
        """
        # Handles while loops in Jack.
        pass

    def compileDo(self):
        """
        Compiles a do statement.
        """
        # Processes do statements for subroutine calls.
        pass

    def compileReturn(self):
        """
        Compiles a return statement.
        """
        # Handles return statements for subroutines.
        pass

    def compileExpression(self):
        """
        Compiles an expression.
        """
        # Processes arithmetic, logical, or constant expressions.
        pass

    def compileTerm(self):
        """
        Compiles a term. If the current token is an identifier, resolves its type:
        - A variable, array element, or subroutine call.
        - Handles symbols like [ ], ( ), or .
        """
        # Processes individual terms within expressions.
        pass

    def compileExpressionList(self):
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        Returns the number of expressions in the list.
        """
        # Processes lists of expressions, often in argument lists.
        pass
