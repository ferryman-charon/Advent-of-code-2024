# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 13
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D13.txt', 'r') as f:
    input = f.read()

test = '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279'''

HUGE = 10_000_000_000_000

def parse_input(input:str, adjust=False)->list[tuple]:

    def strip_numers(instructions:list[str], seperator:str='+'):
        if len(instructions) != 2: return False
        tl, tr = instructions
    
        tl = int(tl.strip(',').split(seperator)[1])
        tr = int(tr.split(seperator)[1])
        return tl, tr
    
    arcades = []
    for machine in input.split('\n\n'):
        a, b, price = machine.splitlines()
 
        xa, ya = strip_numers(a.split()[-2:])
        xb, yb = strip_numers(b.split()[-2:])
        px, py = strip_numers(price.split()[-2:], '=')

        if adjust:
            arcades.append(((xa,ya), (xb, yb), (px+HUGE, py+HUGE)))
            continue
        arcades.append(((xa,ya), (xb, yb), (px, py)))

    return arcades

# Solving Part 1
# ------------------------------------------------------------

def solve_machine_exaust(ainstr:tuple, binstr:tuple, price:tuple)->int:
    for i in range(1,101):
        for j in range(1, 101):
            ares = ainstr[0]*j + binstr[0]*i == price[0]
            bres = ainstr[1]*j + binstr[1]*i == price[1]
            if ares and bres:
                return j*3 + i
    return 0

def calculate_result(input:str)->int:
    result = 0
    arcade = parse_input(input)
    for macine in arcade:
        ains, bins, price = macine
        result += solve_machine_exaust(ains, bins, price)

    return result

print(f'Answer for Part 1: {calculate_result(input)}')


# Solving Part 2
# ------------------------------------------------------------
def solve_machine_fast(ainst:tuple, binst:tuple, price:tuple)->int:
    acount, isint = divmod((price[1]*binst[0] - binst[1]*price[0]), (binst[0]*ainst[1] - binst[1]*ainst[0]))
    if isint != 0: return 0
    bcount, isint = divmod((price[0]-ainst[0]*acount), binst[0])
    if isint != 0: return 0
    return acount*3 + bcount

def calculate_adj_result(input:str)->int:
    result = 0
    arcade = parse_input(input, True)
    for macine in arcade:
        #print(macine)
        ains, bins, price = macine
        #print(solve_machine_fast(ains, bins, price))
        result += solve_machine_fast(ains, bins, price)

    return result

print(f'Answer for Part 2: {calculate_adj_result(input)}')