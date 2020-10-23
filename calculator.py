import io
import math
from tokenize import TokenError
from tokenizer import *
import statistics


class CalculatorException(Exception):
    def __init__(self, arg):
        self.arg = arg


class DivisionException(Exception):
    def __init__(self, arg):
        self.arg = arg


class PositionError(Exception):
    def __init__(self, arg):
        self.arg = arg


# dirctionary used to store constants and variables
vars = {'ans': 0, 'E': 2.718281828459045, 'PI': 3.141592653589793}
math_dic = {"sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log}
max_min = {"max": max, "min": min}
# helping funtion


def expression(wtok):
    result = term(wtok)
    while wtok.get_current() == '+' or wtok.get_current() == '-':

        if wtok.get_current() == '+':
            wtok.next()
            result = result + term(wtok)
        elif wtok.get_current() == '-':
            wtok.next()
            result = result-term(wtok)

    return result


def term(wtok):
    result = factor(wtok)
    while wtok.get_current() == '*' or wtok.get_current() == '/':
        if wtok.get_current() == '*':

            wtok.next()
            result = result*factor(wtok)

        elif wtok.get_current() == '/':
            try:
                wtok.next()
                result = result/factor(wtok)

            except:
                raise DivisionException(f"*** Error.Division by zero")

    return result


def factor(wtok):
    # check for right braces
    if wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok)
        if wtok.get_current() == ")":
            wtok.next()
        elif wtok.get_current() != ')':
            raise CalculatorException(
                f"***Expected  a left parentheses or number but found '{wtok.get_current()}'")

    # check a number
    elif wtok.is_number():                          # should be a number
        result = float(wtok.get_current())
        wtok.next()
    # check for negative opertion
    elif wtok.is_operation():
        if wtok.get_current() == "|":
            wtok.next()
            result = abs(assignment(wtok))
            if wtok.get_current() != "|":
                raise PositionError(
                    f"***Error:Expected '|' \n***The error occured at token '{wtok.get_current()}' just after token '{wtok.get_previous()}'")
            elif wtok.get_current() == "|":
                wtok.next()

        elif wtok.get_current() == '-':
            wtok.next()
            result = -(factor(wtok))
        elif wtok.get_current() in {'+', '*', '/'}:
            raise PositionError(
                f"***Error:Expected '-' or '|'  \n***The error occured at token '{wtok.get_current()}' just after token '{wtok.get_previous()}'")
    # check for a name
    elif wtok.is_name():
        if wtok.get_current() in {"PI", "ans"}:
            result = vars[wtok.get_current()]
            wtok.next()

        elif wtok.get_current() in ('abcdefghijklmnopqrstuvwxyz'):
            if wtok.get_current() in vars:
                x = wtok.get_current()
                result = vars[x]
                wtok.next()
            else:
                raise PositionError(
                    f"Error. Undefined variable: '{wtok.get_current()}'")

        elif wtok.get_current() in ("max", "min"):
            maxmin = max_min[wtok.get_current()]

            wtok.next()
            if wtok.get_current() == "(":
                wtok.next()
                result = assignment(wtok)

                while wtok.get_current() == ",":
                    wtok.next()

                    result = maxmin(result, assignment(wtok))
            elif wtok.get_current() != "(":
                raise PositionError(
                    f"***Error:Unbalanced parenthesses ')' \n ***The error occured at token '{wtok.get_current()}' just after token '{wtok.get_previous()}'")

            if wtok.get_current() == ")":
                wtok.next()
            else:
                raise PositionError(
                    f"***Error:Unbalanced parenthesses ')' \n ***The error occured at token '{wtok.get_current()}' just after token '{wtok.get_previous()}'")

        # funtion name
        elif wtok.get_current() in {'sin', 'cos', 'exp', 'log'}:

            result = math_dic[wtok.get_current()]
            wtok.next()
            if wtok.get_current() == '(':
                wtok.next()
                result = result(assignment(wtok))
            if wtok.get_current() == ")":
                wtok.next()
            elif wtok.get_current() != ')':
                raise PositionError(
                    f"***Error:Unbalanced parenthesses ')' \n ***The error occured at token '{wtok.get_current()}' just after token '{wtok.get_previous()}'")

        else:
            raise PositionError(
                f"***Error: Undefined variable:'{wtok.get_current()}'\n ***The error occured at token '{wtok.get_current()}' just after token '{wtok.get_previous()}'")

    elif wtok.is_at_end():
        raise CalculatorException(
            f"*** Error: Expected number, name or ’(’\n*** The error occurred at token ’*EOL*’ just after token '{wtok.get_previous()}'")

    else:
        raise CalculatorException(
            f"***Error: Expected a left parentheses or number but found '{wtok.get_current()}'")
    return result


def assignment(wtok):
    result = expression(wtok)

    current_value = wtok.get_current()

    if wtok.get_current() == '=':
        while wtok.get_current() == '=':
            pre_var = wtok.get_previous()
            wtok.next()

            if wtok.is_name():
                if wtok.get_current() in ('abcdefghijklmnopqrstuvwxyz'):

                    x = wtok.get_current()
                    vars[x] = result
                    wtok.next()

            else:
                raise PositionError(
                    f"***Error: Expected variable after ’=’\n ***The error occured at token '{wtok.get_current()}' just after token '{wtok.get_previous()}'")

    return result


def statement(wtok):
    if wtok.get_current() == 'quit':
        print('Bye!')
        exit()
    elif wtok.get_current() == 'vars':

        result = vars

    elif wtok.get_current() == 'NO MORE TOKENS':
        result = 'EOF'
    else:
        result = assignment(wtok)
    return result
# ____main_____


def main():
    print("Very simple calculator")
    while True:
        line = input('> ')
        try:
            wtok = TokenizeWrapper(line)
            result = statement(wtok)
            if result == vars:
                for x, y in vars.items():
                    print(str(x) + ':' + str(y)+'\n')
            else:
                vars['ans'] = result
                print(result)
        except TokenError:
            print('*** Error. Unbalanced parentheses')
        except CalculatorException as e:
            print(e)
        except DivisionException as e:
            print(e)
        except PositionError as e:
            print(e)


if __name__ == "__main__":
    main()
