import io
import tokenize


class TokenizeWrapper:
    def __init__(self, line):
        self.line = line
        self.tokens = tokenize.generate_tokens(io.StringIO(line).readline)
        
        self.current = next(self.tokens)
        self.previous = 'START'

    def __str__(self):
        
        return self.current[1]

    def get_current(self):
        if self.current[0] > 0:
            return self.current[1]
        else:
            return 'NO MORE TOKENS'

    def get_previous(self):
        return self.previous

    def next(self):
        # The return value is mainly intended for debugging purposes
        if self.has_next():
            self.previous = self.current[1]
            self.current = next(self.tokens)
            
            return self.current
        else:
            return (0, 'EOS')

    def is_number(self):
       
        return self.current[0] == 2

    def is_name(self):
        return self.current[0] == 1
    def is_operation(self):
        return self.current[0]==54

    def is_newline(self):
        return self.current[0] == 4

    def is_at_end(self):        
        return self.current[0] == 0 or self.current[0] == 4

    def has_next(self):
        return self.current[0] != 0 and self.current[0] != 4


def main():
    line = '1,| max 2'
    w = TokenizeWrapper(line)
    # y=w.next()
    # if not w.is_at_end():
    #     print('True')
    # print(y)
    # print(w.next())
    # print(w.next())
    # print(w.next())
    try:
        while w.has_next():
            
            print(w.get_current(), end=' \t')
            if w.is_name():
                print('NAME')
            elif w.is_number():
                print('NUMBER')
            elif w.is_operation():
                print('opertion') 
            elif w.is_at_end():
                print('end')       
                
            else:
                print()
            w.next()
    except tokenize.TokenError:  # For handling unbalanced parentheses
        print('*** Unbalanced parentheses')
    print('Bye')


if __name__ == '__main__':
    main()