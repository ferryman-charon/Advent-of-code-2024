# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 25
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/eudaemon/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D25.txt', 'r') as f:
    input = f.read()

test = '''#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####'''

# Solving Part 1
# ------------------------------------------------------------

MAX_KEYSIZE = 5
def transpose(matrix:list[list[str]])->list[list[str]]:
    return [list(row) for row in zip(*matrix)]

def find_possible_keys(input:str)->int:
    def get_keys_and_locks(input:str)->tuple[list[int]]:
        keys, locks = [], []
        for schematic in input.split('\n\n'):
            schematic = schematic.splitlines()
            keyorlock = set(schematic[0])
            schematic = transpose(schematic[1:-1])
            s_values = []
            for row in schematic:
                s_values.append(row.count('#'))
            if keyorlock == {'#'}: locks.append(s_values)
            else: keys.append(s_values)

        return locks,keys

    def fit_lock(key:tuple[int], lock:tuple[int])->bool:
        if len(key) != len(lock): raise ValueError
        for i in range(len(key)):
            if key[i] > MAX_KEYSIZE - lock[i]: return False
        return True
    
    res_keys = 0
    locks, keys = get_keys_and_locks(input)
    for lock in locks:
        for key in keys:
            res_keys += fit_lock(key, lock)
    return res_keys


print(f'Answer for Part 1: {find_possible_keys(input)}')

# Solving Part 2
# ------------------------------------------------------------

print(f'Answer for Part 1: {0}')