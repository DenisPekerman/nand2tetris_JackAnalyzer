from JackTokenizer import JackTokenizer
import xml.etree.cElementTree as ET

class CompilationEngine:

    def __init__(self, input: str, output: str):
        """Initializes a new compilation engine."""
        
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
        self._compileOneLine(self.root, 'classVarDec')



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
        # Processes the subroutine body including statements.
        node = ET.SubElement(parent_node, "subroutineBody")
        self._advance(node) # {
        self.compileVarDec(node)
        self.compileStatements(node)
        self._advance(node) # }



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
                self._advance(node) # ;

        

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



    def compileLet(self, parent_node: ET.Element):
        """
        Compiles a let statement.
        """
        self._compileOneLine(parent_node, "letStatement")
        

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



    def compileExpression(self, parent_node: ET.Element):
        """
        Compiles an expression.
        """
        node = ET.SubElement(parent_node, "expression")
        token = self.tokenizer.peek()
        type, value = self.tokenizer.tokenTypeAndValue(token)
        
        if type == 'symbol':
            pass

        # while self.tokenizer.peek() != ')':
        #     token = self.tokenizer.peek()
        #     token_type, token_value = self.tokenizer.replaceSymbol(token)

        #     if token_type == 'symbol' and token_value in ["<", '>', '"','&']:
        #         _, replaced_value = self.tokenizer.replaceSymbol((token_type, token_value))

        #         elem = ET.SubElement(node, token_type)
        #         elem.text = replaced_value

        #         self.tokenizer.advance()
        #     else: 
        #         self._advance(node)
        # pass


            
    def compileTerm(self, parent_node: ET.Element):
        """
        Compiles a term. If the current token is an identifier, resolves its type:
        - A variable, array element, or subroutine call.
        - Handles symbols like [ ], ( ), or .
        """
        # Processes individual terms within expressions.
        node = ET.SubElement(parent_node, "term")
        next_token = self.tokenizer.peek(index=1)

        if next_token == '[':
            pass
            #do compile array on the current token
        elif next_token == '.':
            #do compile subroutine-call
            pass
        

    def compileExpressionList(self, parent_node: ET.Element):
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        Returns the number of expressions in the list.
        """
        # Processes lists of expressions, often in argument lists.
        node = ET.SubElement(parent_node, "expressionList")
        if self.tokenizer.peek() == ')':
            self._doEmptyToken(node)
        else:
            # do sub(1,2,3)
            while self.tokenizer.peek() != ')':
                self._advance(node) # 1, 2, 3
                
         

