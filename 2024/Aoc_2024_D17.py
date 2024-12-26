# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 17
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D17.txt', 'r') as f:
    input = f.read()

test = '''Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0'''

# Solving Part 1
# ------------------------------------------------------------

def initialize_program(input:str)->tuple[tuple[int],list[int]]:
    registers, program = input.split('\n\n')
    registers = tuple([int(reg.split()[-1]) for reg in registers.split('\n')])
    program = program.split()[-1].split(',')

    return registers, [int(i) for i in program]

def run_program(program:list[int], val:int, as_string=True)->str:
    RegA = val
    RegB = 0
    RegC = 0
    output = []

    def combo_op(operant:int)->int:
        if operant <= 3: return operant
        if operant==4: return RegA
        if operant==5: return RegB
        if operant==6: return RegC
        return False
    
    i = 0
    while i < len(program):
        opcode, operant = program[i], program[i+1]
        match opcode:
            case 0: RegA = int(RegA/(2**combo_op(operant)))
            case 1: RegB = RegB ^ operant
            case 2: RegB = combo_op(operant)%8
            case 3: 
                if RegA: 
                    i=operant
                    continue

            case 4: RegB = RegB ^ RegC
            case 5: output.append(str(combo_op(operant)%8))
            case 6: RegB = int(RegA/(2**combo_op(operant)))
            case 7: RegC = int(RegA/(2**combo_op(operant)))
        
        i+=2
    if as_string: return ','.join(output)
    else: return [int(i) for i in output]

def part_one(input:str)->str:
    (RegA,_, _), program = initialize_program(input)
    return run_program(program, RegA)

print(f'Answer for Part 1: {part_one(input)}')


# Solving Part 2
# ------------------------------------------------------------

# i just try the naive approch for now and look for some patterns
def naive_loop_val(input:str)->int:
    (RegA,_, _), program = initialize_program(input)

    value = 35184372088832
    while True:
        if value> 1_000_000: return False
        if len(program) < len(run_program(program, value, False)): return value
        value += 1
    return False

# the key concept here is to see that when a ending sequence in the program matches
# the Register is correct up to a certain digit in numeral base 8

def find_loop_val(input):
    _ , program = initialize_program(input)

    # so we start on the lowest number in base 8 with len(program) digits
    RegA = sum(7 * 8**i for i in range(len(program) - 1)) + 1

    #RegA = 35184372088832 # found this by brute force

    while True:
        result = run_program(program, RegA, False)

        if len(result) > len(program): return -1
        if result == program: return RegA

        # now we just increase the wrong digits in base 8 until they give the correct sequence
        for i in range(len(result) - 1, -1, -1):
            if result[i] != program[i]:
                RegA += 8**i
                break

print(f'Answer for Part 2: {find_loop_val(input)}')