from JackTokenizer import JackTokenizer
import xml.etree.cElementTree as ET

class CompilationEngine:
    def __init__(self, input, output):
        """Initializes a new compilation engine."""
        self.tokenizer = JackTokenizer(input)
        self.output_file = open(output, 'wb')

    # current_token[0] = token type , current_token[1] = token value
    def _advance(self, node: ET.Element):
        current_token = self.tokenizer.advance()
        ET.SubElement(node, current_token[0]).text = current_token[1]

    
    def _flush(self):
        tree = ET.ElementTree(self.root)
        ET.indent(tree, space="\t", level=0)
        tree.write(self.output_file, short_empty_elements=False)

    
    def _doEmptyToken(self, parent_node: ET.Element):
        if len(parent_node) == 0:
            parent_node.text = '\n'
        return parent_node
    

    def _compileSimpleStatement(self, parent_node: ET.Element, child_name: str):
        node = ET.SubElement(parent_node, child_name)
        while self.tokenizer.peek() != ";":
            self._advance(node)
        self._advance(node) # semicolon


    def compileClass(self):
        """
        Compiles a complete class.
        """
        self.root = ET.Element("class") 
        self._advance(self.root)  # class
        self._advance(self.root)  # class name
        self._advance(self.root)  # braket  

        # conmpile class variables
        # keep compiling variables as long as next token is field or static
        while self.tokenizer.peek() in ['static', 'field']:
            self.compileClassVarDec(self.root)

        # compile functions 
        while self.tokenizer.peek() in ['function', 'constructor', 'method']:
            self.compileSubroutine(self.root)
              

        self._advance(self.root)  # closing braket  
        self._flush()

        

    def compileClassVarDec(self, parent_node: ET.Element):
        """
        Compiles static variable declaration or a field declaration.
        """
        # read 2 tokens: first is declration type
        # second is primitive type
        # and then advance to get variables names untill reached ';'
        # write it to xml  
        node = ET.SubElement(parent_node, "classVarDec")
        while self.tokenizer.peek() != ';':          
            self._advance(node) # var value/comma
        self._advance(node) # semicolon



    def compileSubroutine(self, parent_node: ET.Element):
        """
        Compiles a complete method, function, or constructor.
        """
        node = ET.SubElement(parent_node, "subroutineDec")
        self._advance(node) # method function or constructor
        self._advance(node) # subroutine type
        self._advance(node) # subroutine name
        self._advance(node) # opening parentheses

        self.compileParameterList(node)

        self.compileSubroutineBody(node)



    def compileParameterList(self, parent_node: ET.Element):
        """
        Compiles (possibly empty) parameter list.
        Does not handle the enclosing parentheses tokens ( ).
        """
        # Parses a list of parameters for a subroutine.
        node = ET.SubElement(parent_node, "parameterList")
        if self.tokenizer.peek() == ')':
            self._doEmptyToken(node)
        else:
            while self.tokenizer.peek() in ['char', 'int', 'boolean']:
                while self.tokenizer.peek() != ')':
                    self._advance(node)
        self._advance(node) # )



    def compileSubroutineBody(self, parent_node: ET.Element):
        """
        Compiles a subroutine's body.
        """
        # Processes the subroutine body including statements.
        node = ET.SubElement(parent_node, "subroutineBody")
        self._advance(node) # right curley braket
        self.compileVarDec(node)
        self.compileStatements(node)
        self._advance(node) # left curley braket

        

    def compileStatements(self, parent_node: ET.Element):
        """
        Compiles a sequence of statements.
        Does not handle the enclosing curly bracket tokens { }.
        """
        # Processes statements inside subroutine or block bodies.
        node = ET.SubElement(parent_node, "statements")

        while self.tokenizer.peek() != '}':
            
            if self.tokenizer.peek() == 'let':
                self.compileLet(node)

            elif self.tokenizer.peek() == 'do':
                 self.compileDo(node)

            elif self.tokenizer.peek() == 'while':
                self.compileWhile(node)

            elif self.tokenizer.peek() == 'if':
                self.compileIf(node)
                
            elif self.tokenizer.peek() == 'return':
                self.compileReturn(node)



    def compileVarDec(self, parent_node: ET.Element):
        """
        Compiles a variable declaration.
        """
        # Handles local variable declarations inside subroutines.
        node = ET.SubElement(parent_node, "varDec")
        if self.tokenizer.peek() != 'var':
            varDec = ET.SubElement(node, "varDec")
            self._doEmptyToken(varDec)
        else:
            while self.tokenizer.peek() == 'var':
                while self.tokenizer.peek() != ';':     
                    self._advance(node)
                self._advance(node)
    
    
    
    def compileLet(self, parent_node: ET.Element):
        """
        Compiles a let statement.
        """
        self.compileSimpleStatement(parent_node, "letStatement")
        

    def compileIf(self, parent_node: ET.Element ):
        """
        Compiles an if statement, possibly with a trailing else clause.
        """
        # Handles conditional branching logic.
        node = ET.SubElement(parent_node, "ifStatement")
        self._advance(node) #  if
        self._advance(node) #  (
        self.compileExpression(node)
        self._advance(node) #  )
        self._advance(node) #  {
        self.compileStatements(node)
        self._advance(node) # }

        if self.tokenizer.peek() == 'else':
            self._advance(node) # else
            self._advance(node) #  {
            self.compileStatements(node)
            self._advance(node) # }


    def compileWhile(self, parent_node: ET.Element):
        """
        Compiles a while statement.
        """
        # Handles while loops in Jack.
        node = ET.SubElement(parent_node, "whileStatement")
        self._advance(node) # while
        self._advance(node) # (
        self.compileExpression(node)
        self._advance(node) # )
        self._advance(node) # {
        self.compileStatements(node)
        self._advance(node) # }
        

    def compileDo(self, parent_node: ET.Element):
        """
        Compiles a do statement.
        """
        self.compileSimpleStatement(parent_node, "doStatement")
        


    def compileReturn(self, parent_node: ET.Element):
        """
        Compiles a return statement.
        """
        self.compileSimpleStatement(parent_node, "return")



    def compileExpression(self, parent_node: ET.Element):
        """
        Compiles an expression.
        """
        # Processes arithmetic, logical, or constant expressions.
        pass

    def compileTerm(self, parent_node: ET.Element):
        """
        Compiles a term. If the current token is an identifier, resolves its type:
        - A variable, array element, or subroutine call.
        - Handles symbols like [ ], ( ), or .
        """
        # Processes individual terms within expressions.
        pass

    def compileExpressionList(self, parent_node: ET.Element):
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        Returns the number of expressions in the list.
        """
        # Processes lists of expressions, often in argument lists.
        pass
