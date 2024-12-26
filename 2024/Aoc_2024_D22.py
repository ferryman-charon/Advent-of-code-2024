# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 22
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/eudaemon/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D22.txt', 'r') as f:
    input = f.read().splitlines()

test = '''1
2
3
2024'''.splitlines()

PRUNE = 16777216

# Solving Part 1
# ------------------------------------------------------------
def prng_monkey(number:int, depth:int)->int:

    def update_secret(n:int)->int:
        num = n
        num1 = (num ^ (num*64))%PRUNE
        num2 = (num1 ^ int(num1/32))%PRUNE
        return (num2 ^ (num2*2048))%PRUNE

    to_update = number 
    for _ in range(depth):
        to_update = update_secret(to_update)
    return to_update

def part_one(input:list[str])->int:
    result = 0
    DEPTH = 2000
    for line in input:
        #print(prng_monkey(int(line), DEPTH))
        result += prng_monkey(int(line), DEPTH)
    return result


#print(f'Answer for Part 1: {part_one(input)}')


# Solving Part 2
# ------------------------------------------------------------
from functools import cache

@cache
def prng_list(number:int, depth:int)->int:

    def update_secret(n:int)->int:
        num = n
        num1 = (num ^ (num*64))%PRUNE
        num2 = (num1 ^ int(num1/32))%PRUNE
        return (num2 ^ (num2*2048))%PRUNE

    to_update = number 
    fdigits = [to_update%10]
    for _ in range(depth):
        to_update = update_secret(to_update)
        fdigits.append(to_update%10)
    return fdigits
import time

def number_sequences(input:list[str]):

    def diff_lists(banana_lists:list[list[int]], max_size:int)->list[list[int]]:
        banana_book = {}

        for blist in banana_lists:
            diff_dict = {}
            for i in range(max_size,len(blist)):
                diff_list = []
                for j in range(max_size-1, -1, -1):
                    diff_list.append(blist[i-j]-blist[i-j-1])

                key = tuple(diff_list)
                if key in diff_dict: continue
                else: diff_dict[key] = blist[i]

            for seq, val in diff_dict.items():
                if seq in banana_book.keys():
                    banana_book[seq] += val
                else: banana_book[seq] = val
    
        return max(banana_book.values())

    DEPTH = 2000
    all_list = []
    for line in input:
        all_list.append(prng_list(int(line), DEPTH))
    return diff_lists(all_list, 4)


print(f'Answer for Part 2: {number_sequences(input)}')