import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

class JackAnalyzer:
    
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = input_file.replace('.jack', '.xml')

    
    def run(self):
        compileEngine = CompilationEngine(self.input_file, self.output_file)
        compileEngine.compileClass()
            


if __name__ == "__main__":

    input = sys.argv[1]
    main = JackAnalyzer(input)
    main.run()
    
    
    