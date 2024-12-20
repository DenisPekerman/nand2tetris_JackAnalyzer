from JackTokenizer import JackTokenizer
import xml.etree.cElementTree as ET

class CompilationEngine:

    def __init__(self, input: str, output: str):
        """
        Initializes a new compilation engine
        """
        
        self.tokenizer = JackTokenizer(input)
        self.output_file = open(output, 'wb')
        

    # current_token[0] = token type , current_token[1] = token value
    def _advance(self, node: ET.Element):
        current_token = self.tokenizer.advance()
        if current_token: 
            ET.SubElement(node, current_token[0]).text = current_token[1]
        else:
            raise Exception("EOF")

    
    def _flush(self):
        tree = ET.ElementTree(self.root)
        ET.indent(tree, space="\t", level=0)
        tree.write(self.output_file, short_empty_elements=False)

    
    def _doEmptyToken(self, parent_node: ET.Element):
        if len(parent_node) == 0:
            parent_node.text = '\n'
        return parent_node
    

    def _compileOneLine(self, parent_node: ET.Element, child_name: str):
        node = ET.SubElement(parent_node, child_name)
        while self.tokenizer.peek() != ";":
            self._advance(node) # line's body
        self._advance(node) # ;


    def _compileArrayIndex(self, parent_node: ET.Element):
        self._advance(parent_node) # [
        self.compileExpression(parent_node)
        self._advance(parent_node) # ]



    def compileClass(self):
        """
        Compiles a complete class.
        """
        self.root = ET.Element("class") 
        self._advance(self.root)  # class
        self._advance(self.root)  # class name
        self._advance(self.root)  # {

        # conmpiles class variables
        while self.tokenizer.peek() in ['static', 'field']:
            self.compileClassVarDec(self.root)

        # compiles subroutine 
        while self.tokenizer.peek() in ['function', 'constructor', 'method']:
            self.compileSubroutine(self.root)
              
        self._advance(self.root)  # } 
        self._flush() # writes everything to a file

        

    def compileClassVarDec(self, parent_node: ET.Element):
        """
        Compiles static variable declaration or a field declaration.
        """
        self._compileOneLine(parent_node, 'classVarDec')



    def compileSubroutine(self, parent_node: ET.Element):
        """
        Compiles a complete method, function, or constructor.
        """
        node = ET.SubElement(parent_node, "subroutineDec")
        self._advance(node) # method function or constructor
        self._advance(node) # subroutine type
        self._advance(node) # subroutine name
        self._advance(node) # (

        self.compileParameterList(node)

        self._advance(node) # )

        self.compileSubroutineBody(node)



    def compileParameterList(self, parent_node: ET.Element):
        """
        Compiles (possibly empty) parameter list.
        Does not handle the enclosing parentheses tokens ( ).
        """
        node = ET.SubElement(parent_node, "parameterList")
        if self.tokenizer.peek() == ')':
            self._doEmptyToken(node)
        else:
            while self.tokenizer.peek() in ['char', 'int', 'boolean']:
                while self.tokenizer.peek() != ')':
                    self._advance(node)
        


    def compileSubroutineBody(self, parent_node: ET.Element):
        """
        Compiles a subroutine's body.
        """
        node = ET.SubElement(parent_node, "subroutineBody")
        self._advance(node) # {
        self.compileVarDec(node)
        self.compileStatements(node)
        self._advance(node) # }



    def compileVarDec(self, parent_node: ET.Element):
        """
        Compiles a variable declaration.
        """
        node = ET.SubElement(parent_node, "varDec")
        if self.tokenizer.peek() != 'var':
            self._doEmptyToken(node)
        else:
            while self.tokenizer.peek() == 'var':
                while self.tokenizer.peek() != ';':     
                    self._advance(node)
                self._advance(node) # ;

        

    def compileStatements(self, parent_node: ET.Element):
        """
        Compiles a sequence of statements.
        Does not handle the enclosing curly bracket tokens { }.
        """
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
            
            else:
                break



    def compileLet(self, parent_node: ET.Element):
        """
        Compiles a let statement.
        """
        node = ET.SubElement(parent_node, "letStatement")
        self._advance(node) # let
        self._advance(node) # identifier
        self._advance(node) # =
        self.compileExpressionList(node)
        


    def compileIf(self, parent_node: ET.Element ):
        """
        Compiles an if statement, possibly with a trailing else clause.
        """
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
        node = ET.SubElement(parent_node, "doStatement")
        while self.tokenizer.peek() != '(':
            self._advance(node) # do someSubroutine
        self._advance(node) # (
        self.compileExpressionList(node)
        self._advance(node) # )
        


    def compileReturn(self, parent_node: ET.Element):
        """
        Compiles a return statement.
        """
        self._compileOneLine(parent_node, "return")

    

    def compileExpressionList(self, parent_node: ET.Element):
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        Returns the number of expressions in the list.
        """
        node = ET.SubElement(parent_node, "expressionList")
        if self.tokenizer.peek() == ')':
            self._doEmptyToken(node)
        else:
            while self.tokenizer.peek() != ')':
                self.compileExpression(node)
                if self.tokenizer.peek() == ',':
                    self._advance(node) # ,
                


    def compileExpression(self, parent_node: ET.Element):
        """
        Compiles an expression.
        """
        node = ET.SubElement(parent_node, "expression")
        self.compileTerm(node)
        while self.tokenizer.peek() in ['+', '-', '*', '/', '>', '<', '&', '|', '=']:
            self._advance(node)
            self.compileTerm(node)


            
    def compileTerm(self, parent_node: ET.Element):
        """
        Compiles a term. If the current token is an identifier, resolves its type:
        - A variable, array element, or subroutine call.
        - Handles symbols like [ ], ( ), or .
        """
        node = ET.SubElement(parent_node, "term")

        current_token = self.tokenizer.peek()
        current_token_type, _ = self.tokenizer.tokenTypeAndValue(current_token)

        next_token = self.tokenizer.peek(index=1)

        if current_token == '(':
            self._advance(node) # (
            self.compileExpression(node) # expression
            self._advance(node) # )

        elif (current_token_type in ['integerConstant', 'stringConstant'] or 
              current_token in ['true', 'false', 'null', 'this']):
            self._advance(node) 
        
        elif current_token in ['-', '~']:
            self._advance(node) # - or ~ 
            self.compileTerm(node)
        
        elif current_token_type == 'identifier':
            if next_token == '(':
                self._advance(node) # subroutine
                self._advance(node) # (
                self.compileExpressionList(node)
                self._advance(node) # )
            elif next_token == '.': 
                self._advance(node) # class
                self._advance(node) # .
                self._advance(node) # subroutine
                self._advance(node) # (
                self.compileExpressionList(node)
                self._advance(node) # )
            elif next_token == '[':
                self._advance(node)
                self._compileArrayIndex(node)
            else:
                self._advance(node)
            


    
         

