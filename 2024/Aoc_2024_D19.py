# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 19
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D19.txt', 'r') as f:
    input = f.read()

test = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb'''

# Solving Part 1
# ------------------------------------------------------------

def parse_input(input:str)->list[str, list[str]]:
    towels, combinations = input.split('\n\n')
    towels = towels.split(', ')
    combinations = combinations.split()
    return tuple(towels), combinations

from functools import cache, lru_cache

@cache
def pos_towel_arangement(combination:str, pos_towel:list[str])->bool:
    for towel in pos_towel:
        l = len(towel)
        if l == len(combination):
            if towel == combination: return True
            else : continue
        if combination[:l] == towel:
            if pos_towel_arangement(combination[l:], pos_towel): return True

    return False

def check_towel_sorting(input:str)->int:
    pos_towels, combinations = parse_input(input)
    result = 0
    for comb in combinations:
        result += pos_towel_arangement(comb, pos_towels)
    return result

print(f'Answer for Part 1: {check_towel_sorting(input)}')


# Solving Part 2
# ------------------------------------------------------------

@lru_cache(1000)
def towel_arangement(combination:str, pos_towel:list[str])->int:
    count = 0

    # try every towel
    for towel in pos_towel:
        l = len(towel)
        if l == len(combination):
            if towel == combination: count += 1
            else : continue

        # if towel found solve reduced problem
        if combination[:l] == towel:
            count += towel_arangement(combination[l:], pos_towel)
    return count

def count_towel_arr(input:str)->int:
    pos_towels, combinations = parse_input(input)
    result = 0
    for comb in combinations:
    #print(towel_arangement.cache_info())
        result += towel_arangement(comb, pos_towels)
    return result


print(f'Answer for Part 2: {count_towel_arr(input)}')