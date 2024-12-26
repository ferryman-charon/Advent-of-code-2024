# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 11
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D11.txt', 'r') as f:
    input = f.read().split()

test = '125 17'.split()

# Solving Part 1
# ------------------------------------------------------------
def remove_leading_zero(number:str):
    for c in range(len(number)):
        if number[c] != '0':
            return number[c:]
    return '0'


def arrange_stones(stone_array:list[str])->list[str]:
    stones = stone_array.copy()
    index = 0
    while index < len(stones):
        if stones[index] == '0':
            stones[index] = '1'
            index += 1
        elif len(stones[index])%2:
            num = int(stones[index])
            stones[index] = str(num*2024)
            index += 1
        else:
            mid = int(len(stones[index]) / 2)
            left = remove_leading_zero(stones[index][:mid])
            right = remove_leading_zero(stones[index][mid:])

            stones.pop(index)
            stones.insert(index, left)
            stones.insert(index + 1, right)
            index += 2

    return stones

def arange_n_times(stone_array:list[str], n:int=25)->int:
    stones = stone_array.copy()
    for _ in range(n):
        stones = arrange_stones(stones)
    return len(stones)


print(f'Answer for Part 1: {arange_n_times(input, 25)}')


# Solving Part 2
# ------------------------------------------------------------

# ok the idea was to group the stones and so reduce the len of the array and 
# complexity of the problem

def get_stones_value(stones:dict[str,int])->dict[str,int]:
    new_stones = {}

    for stone, val in stones.items():

        if stone == '0': 
            if '1' in new_stones.keys():new_stones['1'] += val
            else: new_stones['1'] = val
                
        elif len(stone)%2:
            num = (str(int(stone)*2024))
            if num in new_stones.keys(): new_stones[num] += val
            else: new_stones[num] = val
        else:
            mid = int(len(stone)/2)
            left = remove_leading_zero(stone[:mid])
            right = remove_leading_zero(stone[mid:])

            if left in new_stones.keys(): new_stones[left] += val
            else: new_stones[left] = val

            if right in new_stones.keys(): new_stones[right] += val
            else: new_stones[right] = val
            
    return new_stones

def Counter(iterable:list)->dict:
    counter_dict = {}
    for el in iterable:
        if el in counter_dict.keys(): 
            counter_dict[el] += 1
        else:
            counter_dict[el] = 1
    return counter_dict

def arange_dict(stone_array:list[str], n:int=25)->int:
    stones = Counter(stone_array)
    for _ in range(n):
        stones = get_stones_value(stones)

    return sum(stones.values())


def arange_rec_n_times(stone_array:list[str], n:int)->int:
    if n == 0:
        return 1
    result = 0
    for stone in get_stones_value(stone_array):
        result += arange_rec_n_times([stone], n-1)

    return result

print(f'Answer for Part 2: {arange_dict(input, 75)}')