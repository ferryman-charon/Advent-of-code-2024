# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 7
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D07.txt', 'r') as f:
   input = f.read().splitlines()

test = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20'''.splitlines()

# Solving Part 1
# ------------------------------------------------------------

def return_permutations(length:int)->list[str]:
    if length == 1:
        return ['0','1']
    newarr = []
    for i in return_permutations(length-1):
        newarr.append('0'+i)
        newarr.append('1'+i)
    return newarr

def return_binary(length:int)->list[str]:
    newarr = []
    for i in range(2**length):
        newarr.append(bin(i)[2:].zfill(length))
    return newarr

def calculate_operation(operators:str, values:list[int])->int:
    if len(operators)+1 != len(values):
        return -1
    
    temp = values[0]
    for i in range(len(operators)):
        if operators[i] == '0': temp += values[i+1]
        else: temp *= values[i+1]

    return temp

def operation_result(res:int, values:list[int])->bool:
    oplen = len(values)-1

    #for op in return_permutations(oplen):
    for op in return_binary(oplen):
        
        if calculate_operation(op,values) == res:
            return True
    
    return False
    
def validate_operations(text:list[str]):
    counter = 0
    for line in text:
        res, vals = line.split(': ')
        res = int(res)
        vals = [int(i) for i in vals.split()]
        
        if operation_result(res, vals):      
            counter += res
    return counter

print(f'Answer for Part 1: {validate_operations(input)}')


# Solving Part 2
# ------------------------------------------------------------
def return_permutation2(length:int)->list[str]:
    if length == 1:
        return ['0','1', '2']
    newarr = []
    for i in return_permutation2(length-1):
        newarr.append('0'+i)
        newarr.append('1'+i)
        newarr.append('2'+i)
    
    return newarr


def calculate_operation2(operators:str, values:list[int])->int:
    if len(operators)+1 != len(values):
        return -1
    
    result = values[0]
  
    for i in range(len(operators)):
        if operators[i] == '0': result += values[i+1]
        elif operators[i] == '1': result *= values[i+1]
        else:
            temp = int(str(result) + str(values[i+1]))
            result = temp

    return result


def operation_result2(res:int, values:list[int])->bool:
    oplen = len(values)-1

    #for op in return_permutations(oplen):
    for op in return_permutation2(oplen):
        
        if calculate_operation2(op,values) == res:
            return True
    
    return False
    
def validate_operations2(text:list[str]):
    counter = 0
    for line in text:
        res, vals = line.split(': ')
        res = int(res)
        vals = [int(i) for i in vals.split()]
        
        if operation_result2(res, vals):      
            counter += res
    return counter

print(f'Answer for Part 2: {validate_operations2(input)}')