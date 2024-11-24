import sys
from JackTokenizer import JackTokenizer



class JackAnalizer:
    
    def __init__(self, input_file):
        self.input_file = input_file

    
    def run(self):
        tokenizer = JackTokenizer(self.input_file)
        while tokenizer.hasMoreTokens():
            token = tokenizer.advance()
            print(token)
            










if __name__ == "__main__":

    input = sys.argv[1]
    main = JackAnalizer(input)
    main.run()
    
    
    