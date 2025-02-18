import sys

#################################################
#                     Stack                     #
#################################################

class Stack:
    def __init__(self, size=256):
        self.array = []
        self.size = size

    def push(self, number):                        # Stack push function
        if len(self.array) >= self.size:
            raise IndexError("Stack Overflow")     # Gracefully raise stack overflow error
        self.array.append(number)

    def pop(self):                                 # Stack pop function
        if not self.array:
            raise IndexError("Stack Underflow")    # Gracefully raise stack underflow error
        return self.array.pop()

    def top(self):                                 # Stack top function
        if not self.array:
            raise IndexError("Stack is Empty")     # Gracefully raise stack empty error
        return self.array[-1]

# The stack class was fixed by removing the sp variable keeping track of the pointer,
# instead, we are now using Python's built-in append() and pop() methods... I didn't know
# they were a thing...

##################################################
#                  Tokenization                  #
##################################################

def tokenize(program_lines):
    program = []
    label_tracker = {}

    for line in program_lines:
        line = line.split("#", 1)[0].strip()               # Remove comments and strip whitespace

        if not line:
            continue                                       # Skip empty lines

        parts = line.split()
        
        if parts[0].endswith(":"):                         # Store label positions
            label_tracker[parts[0][:-1]] = len(program)
        else:
            program.append(parts)                          # Store program tokens

    return program, label_tracker

# So, this changed up a lot. The tokenize function now returns the program array of arrays. An example of a 
# program array would be: [['PUSH', '5'], ['PUSH', '3'], ['ADD'], ['PRINT', 'Hello, World!'], ['HALT']]. This
# makes more sense as now each line is a new array and we can see where lines start and end. The label_tracker
# stayed the same.
#
# Hehe... by the way, I got rid of all the validation checks...

# TODO: Add validation checks for the program array

# TODO: ##################################################
# TODO: #                   Validation                   #
# TODO: ##################################################

##################################################
#                 Interpretation                 #
##################################################

def execute(program, label_tracker):
    stack = Stack()                                                  # Instantiate stack
    pc = 0                                                           # Program counter

    def op_push():                                                   # PUSH opcode: Push a number onto the stack
        stack.push(int(program[pc][1]))

    def op_pop():                                                    # POP opcode: Remove top value from stack
        stack.pop()
    
    def op_dup():
        a = stack.pop()
        stack.push(a)
        stack.push(a)
    
    def op_swap():
        a, b = stack.pop(), stack.pop()
        stack.push(a)
        stack.push(b)
    
    def op_rot():
        a, b, c = stack.pop(), stack.pop(), stack.pop()
        stack.push(a)
        stack.push(b)
        stack.push(c)

    def op_add():                                                    # ADD opcode: Add top two values on stack
        stack.push(stack.pop() + stack.pop())

    def op_sub():                                                    # SUB opcode: Subtract top value from second top value
        a, b = stack.pop(), stack.pop()
        stack.push(b - a)

    def op_mul():                                                    # MUL opcode: Multiply top two values on stack
        stack.push(stack.pop() * stack.pop())

    def op_div():                                                    # DIV opcode: Divide second top value by top value
        a, b = stack.pop(), stack.pop()
        stack.push(b // a)

    def op_print():                                                  # PRINT opcode: Print a string literal
        program[pc][1] = program[pc][1].replace('"', '')
        program[pc][-1] = program[pc][-1].replace('"', '')
        literal = " ".join(program[pc][1:])
        print(literal)

    def op_printtop():                                               # PRINT.TOP opcode: Print the top value of the stack
        print(stack.top())

    def op_goto():                                                   # GOTO opcode: Jump to a label
        nonlocal pc
        pc = label_tracker[program[pc][1]] - 1

    def op_halt():                                                   # HALT opcode: Stop execution
        return 16

    dispatch = {
        "PUSH": op_push,
        "POP": op_pop,
        "DUP": op_dup,
        "SWAP": op_swap,
        "ROT": op_rot,

        "ADD": op_add,
        "SUB": op_sub,
        "MUL": op_mul,
        "DIV": op_div,

        "PRINT": op_print,
        "PRINT.TOP": op_printtop,

        "GOTO": op_goto,

        "HALT": op_halt,
    }

    while pc < len(program):                                         # Execution loop
        opcode = program[pc][0]
        if opcode in dispatch:
            if dispatch[opcode]() == 16:
                break                                                # Stop execution if HALT is encountered
            else:
                pc += 1

##################################################
#                    Main                        #
##################################################

def main():
    program_filepath = sys.argv[1]                                   # Get program file path from command line argument
    with open(program_filepath, 'r') as program_file:
        program_lines = [line.strip() for line in program_file.readlines()]
    
    program, label_tracker = tokenize(program_lines)                 # Tokenize input file
    execute(program, label_tracker)                                  # Execute program

if __name__ == "__main__":
    main()                                                           # Run main function