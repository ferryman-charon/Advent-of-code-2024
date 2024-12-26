# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 3
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D03.txt', 'r') as f:
   input = f.read()

test = '''xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'''
test2 = '''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))'''
# Solving Part 1
# ------------------------------------------------------------

def digit_len(text:str, index:int, first:bool)-> int:
    j = 0
    while True:
        if index + j + 1 > len(text):
            return 0
        if text[index + j].isdigit():
            j += 1
        else:
            if first and text[index +j] == ',':
                return j + 1
            elif not first and text[index +j] == ')':
                return j + 1
            else:
                return 0

def cor_memory_ops(text:str)->int:
    result = 0
    i = 0
    while i < len(text):
        if text[i:i+4] == 'mul(':
            i += 4

            l1 = digit_len(text,i, True)
            if not l1: continue
            
            l2 = digit_len(text, i+l1, False)
            if not l2: continue
            result += int(text[i:i+l1-1])*int(text[i+l1:i+l1+l2-1])
            i += (l1+l2)
        else:
            i+=1
    
    return result

            

         

print(f'Answer for Part 1: {cor_memory_ops(input)}')


# Solving Part 2
# ------------------------------------------------------------
def ext_memory_ops(text:str)->int:
    result = 0
    i = 0
    operate = True  
    while i < len(text):
        if text[i:i+4] == 'mul(':
            i += 4

            l1 = digit_len(text,i, True)
            if not l1: continue
            
            l2 = digit_len(text, i+l1, False)
            if not l2: continue

            if operate:
                result += int(text[i:i+l1-1])*int(text[i+l1:i+l1+l2-1])
            i += (l1+l2)
        elif text[i:i+4] == 'do()': 
            operate = True
            i += 4
        elif text[i:i+7] == "don't()": 
            operate = False
            i += 7
        else:
            i+=1
    
    return result

print(f'Answer for Part 2: {ext_memory_ops(input)}')