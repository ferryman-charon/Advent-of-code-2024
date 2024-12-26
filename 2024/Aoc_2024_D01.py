# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 1
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/eudaemon/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D01.txt', 'r') as f:
   input = f.read().splitlines()

test = '''3   4
4   3
2   5
1   3
3   9
3   3'''.splitlines()

# Solving Part 1
# ------------------------------------------------------------

# quick implemantation of bubble sort
def sort_list(array:list)->list:
    iterable = array[:]
    n = len(iterable)

    # key concepts leaned:
    # bubble sort is 100% done after O(n²)
    # so we are just trying to save time

    for i in range(n-1):
        swapped = False 

        # bc the last (n-i) number is correct after 1. (i) iteration 
        # we can stop the loop one element (i) ahead

        for j in range(0,n-i-1):
            if iterable[j] > iterable[j+1]:
                temp = iterable[j+1]
                iterable[j+1] = iterable[j]
                iterable[j] = temp
                swapped = True
        
        # if after one iteration no swap was done the array is
        # sorted and we can stop
        if swapped == False:
            return iterable
    return iterable

def seperate_lists(text:list[str])->tuple[list]:
    left, right = [], []

    for line in text:
        l,r = line.split()
        left.append(l)
        right.append(r)

    return left, right

def calculate_dist(left, right)->int:
    total_dist = 0
    sleft = sort_list(left)
    sright = sort_list(right)

    for i in range(len(left)):
        total_dist += abs((int(sright[i])-int(sleft[i])))
    
    return total_dist

def part_one(text:list[str])->int:
    sleft, sright = seperate_lists(text)
    return calculate_dist(sleft,sright)

print(f'Answer for Part 1: {part_one(input)}')


# Solving Part 2
# ------------------------------------------------------------

# custom counter 
# from collections import Counter
def count(element, iterable:list)->int:
    c = 0
    for obj in iterable:
        if obj == element:
            c += 1
    return c

def Counter(iterable:list)->dict:
    counter_dict = {}
    for el in iterable:
        if el in counter_dict.keys(): continue
        counter_dict[el] = count(el,iterable)
    return counter_dict

def similarity_score(left:list, right:list)->int:
    sim_score = 0
    left_dict = Counter(left)
    for item in left_dict.keys():
        if item in right:
            sim_score += int(item) * left_dict[item] * count(item, right)
    return sim_score

def part_two(text:list[str])->int:
    left, right = seperate_lists(text=text)
    return similarity_score(left,right)


print(f'Answer for Part 2: {part_two(input)}')
