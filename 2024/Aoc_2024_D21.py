# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 21
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/eudaemon/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D21.txt', 'r') as f:
    input = f.read().splitlines()

test = '''029A
980A
179A
456A
379A'''.splitlines()

NUMPAD = {
'7':(0,0), '8':(0,1), '9':(0,2), 
'4':(1,0), '5':(1,1), '6':(1,2),
'1':(2,0), '2':(2,1), '3':(2,2),
'0':(3,1), 'A':(3,2)}

CONTROLPAD = {
    '<':{'v':['>A'],'>':['>>A'], '^':['>^A'], 'A':['>>^A', '>^>A']},
    'v':{'<':['<A'], '>':['>A'], '^':['^A'], 'A':['>^A', '^>A']},
    '>':{'<':['<<A'],'v':['<A'], '^':['<^A', '^<A'], 'A':['^A']},
    '^':{'<':['v<A'], 'v':['vA'], '>':['>vA', 'v>A'], 'A':['>A']},
    'A':{'<':['v<<A', '<v<A'], 'v':['v<A', '<vA'], '^':['<A'], '>':['vA']}
}


DIR = {(-1,0):'^',(0,1):'>',(1,0):'v',(0,-1):'<'}
# Solving Part 1
# ------------------------------------------------------------
from functools import cache

@cache
def find_instr(start:str, end:str)->list[str]:
    y0, x0 = NUMPAD[start]
    yf, xf = NUMPAD[end]
    dist = abs(y0-yf)+abs(x0-xf)
    paths = []
    queue = [((y0, x0),'', 0)]
    while queue:
        (y,x), path, cost = queue.pop()
        if cost < dist:
            for dy, dx in DIR.keys():
                ny, nx = y+dy, x+dx
                if (ny,nx) not in NUMPAD.values(): continue
                p = path + DIR[(dy,dx)]
                #print(p)
                queue.append(((ny,nx),p, cost+1))
        if cost > dist or (y,x) != (yf,xf): continue
        else: paths.append(path+'A')

    return paths

@cache
def v0_controlpad_instr(code:str, sdiff:str)->list[str]:
    if not code: return []
    out_sequences = []

    current = code[0]
    rem_seq = code[1:]
    if sdiff == current: instr = ['A']
    else: instr = CONTROLPAD[sdiff][current]
    for seq in instr:
        sequences = v0_controlpad_instr(rem_seq, current)
        if not sequences: return instr
        for remain_seq in sequences:
            out_sequences.append(seq+remain_seq)
    return out_sequences

@cache
def v1_controlpad_instr(start_code:str, sdiff:str, r_chain_len:int)->str:
    diff = sdiff
    code = start_code
    for j in range(r_chain_len):
        print(j)
        out = ''
        for i in range(len(code)):
            current = code[i]
            if diff == current: out += 'A'
            else: out += CONTROLPAD[diff][current]
            diff = current
        code = out
      
    return len(code)

def numpad_instr(code:str, sdiff)->list[str]:
    if not code: return []
    out_sequences = []

    current = code[0]
    rem_seq = code[1:]

    if sdiff == current: instr = ['A']
    else: instr = find_instr(sdiff, current)
    for seq in instr:
        sequences = numpad_instr(rem_seq, current)
        if not sequences: return instr
        for remain_seq in sequences:
            out_sequences.append(seq+remain_seq)
    return out_sequences

def v1_final_instr(code:str, robot_chain_len:int)->str:
    numpad = numpad_instr(code, 'A')
    print(numpad)
    outer = []
    for seq in numpad:

        start = 'A' 
        outer.append(v1_controlpad_instr(seq, start, robot_chain_len))
    
    return min(outer)

def str_to_int(line:str)->int:
    i = 0
    res = ''
    start = False
    while i < len(line):
        if line[i] == '0':
            if not start: 
                i+=1 
                continue
        if line[i].isdigit():
            res += line[i]
            start = True
        i += 1
    return int(res)

@cache
def translate(code, depth):
    if code[0].isnumeric():
        moves = numpad_instr(code)
    else:
        #moves = controlpad_instr(code,'A')
        moves = translate_keypad(code)

    if depth == 0:
        return min([sum(map(len, move)) for move in moves])
    else:
        return min([sum(translate(curr_code, depth - 1) for curr_code in move) for move in moves])
    
def build_combinations(arrays, current=[], index=0):
    if index == len(arrays):
        return [current]
    results = []
    for value in arrays[index]:
        new_results = build_combinations(arrays, current + [value], index + 1)
        results.extend(new_results)
    return results

def numpad_instr(code):
    code = "A" + code
    moves = [find_instr(a, b) for a, b in zip(code, code[1:])]
    moves = build_combinations(moves)
    return moves

def translate_keypad(code):
    code = "A" + code
    moves = [CONTROLPAD[a][b] if a != b else ["A"] for a, b in zip(code, code[1:])]
    moves = build_combinations(moves)
    return moves

def part_one(data):
    complexities = 0
    for code in data:
        min_len = translate(code, 2)
        complexities += min_len * int(code[:-1])
    return complexities

print(f'Answer for Part 1: {part_one(input)}')

# Solving Part 2
# ------------------------------------------------------------
def build_combinations(arrays, current=[], index=0):
    if index == len(arrays):
        return [current]
    results = []
    for value in arrays[index]:
        new_results = build_combinations(arrays, current + [value], index + 1)
        results.extend(new_results)
    return results

@cache
def translate(code, depth):
    if code[0].isnumeric():
        moves = numpad_instr(code)
    else:
        #moves = controlpad_instr(code,'A')
        moves = translate_keypad(code)

    if depth == 0:
        return min([sum(map(len, move)) for move in moves])
    else:
        return min([sum(translate(curr_code, depth - 1) for curr_code in move) for move in moves])


def numpad_instr(code):
    code = "A" + code
    moves = [find_instr(a, b) for a, b in zip(code, code[1:])]
    moves = build_combinations(moves)
    return moves

def translate_keypad(code):
    code = "A" + code
    moves = [CONTROLPAD[a][b] if a != b else ["A"] for a, b in zip(code, code[1:])]
    moves = build_combinations(moves)
    return moves

def part_two(data):
    complexities = 0
    for code in data:
        min_len = translate(code, 25)
        complexities += min_len * int(code[:-1])
    return complexities
print(f'Answer for Part 2: {part_two(input)}')