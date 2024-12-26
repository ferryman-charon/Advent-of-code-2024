# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 4
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D04.txt', 'r') as f:
   input = f.read().splitlines()

test = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''.splitlines()


# Solving Part 1
# ------------------------------------------------------------
def xmas_search(text:list[str])->int:
    word_count = 0
    for y in range(len(text)):
        for x in range(len(text[0])):

            if text[y][x] == 'X':
                if text[y][x+1:x+4] == 'MAS':
                    word_count += 1

                if y + 3 < len(text):
                    if text[y+1][x] == 'M' and text[y+2][x] == 'A' and text[y+3][x] == 'S':
                        word_count += 1

                    if x+3 < len(text[0]):
                        if text[y+1][x+1] == 'M' and text[y+2][x+2] == 'A' and text[y+3][x+3] == 'S':
                            word_count += 1

                    if x-3 >= 0:
                        if text[y+1][x-1] == 'M' and text[y+2][x-2] == 'A' and text[y+3][x-3] == 'S':
                            word_count += 1
                
                if y - 3 >= 0:
                    if text[y-1][x] == 'M' and text[y-2][x] == 'A' and text[y-3][x] == 'S':
                        word_count += 1

                    if x+3 < len(text[0]):
                        if text[y-1][x+1] == 'M' and text[y-2][x+2] == 'A' and text[y-3][x+3] == 'S':
                            word_count += 1

                    if x-3 >= 0:
                        if text[y-1][x-1] == 'M' and text[y-2][x-2] == 'A' and text[y-3][x-3] == 'S':
                            word_count += 1
                    

            if text[y][x] == 'S':
                if text[y][x+1:x+4] == 'AMX':
                    word_count += 1

    return word_count
            

print(f'Answer for Part 1: {xmas_search(input)}')


# Solving Part 2
# ------------------------------------------------------------
XMAS = ['M', 'S', 'S', 'M']

def x_mas_search(text:list[str])->int:
    word_count = 0
    for y in range(len(text)):
        for x in range(len(text[0])):

            if text[y][x] == 'A':
                if y + 1 < len(text) and y-1 >= 0 and x+1 < len(text[0]) and x-1 >= 0:
                    for i in range(4):
                        expr = text[y+1][x+1] == XMAS[i%4] and text[y+1][x-1] == XMAS[(i+1)%4]  
                        expr = expr and text[y-1][x-1] == XMAS[(i+2)%4] and text[y-1][x+1] == XMAS[(i+3)%4]
                        if expr:word_count += 1

    return word_count

print(f'Answer for Part 2: {x_mas_search(input)}')