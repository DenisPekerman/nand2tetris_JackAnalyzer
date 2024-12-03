import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine



class JackAnalizer:
    
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = ""

    
    def run(self):
        compileEngine = CompilationEngine(self.input_file, self.output_file)
        compileEngine.compileClass()
            


if __name__ == "__main__":

    input = sys.argv[1]
    main = JackAnalizer(input)
    main.run()
    
    
    