# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 8
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D08.txt', 'r') as f:
   input = f.read().splitlines()

test = '''............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............'''.splitlines()

# Solving Part 1
# ------------------------------------------------------------
def extract_antennas(text:list[str])->dict[str,list[tuple]]:
    antennas = {}
    for row in range(len(text)):
        for col in range(len(text[0])):
            char = text[row][col]
            if char != '.':
                if char in antennas.keys():
                    positions = antennas[char]
                    positions.append((row,col))
                    antennas[char] = positions
                else:
                    antennas[char] = [(row,col)]
    return antennas

def count_antinodes(text:list[str])->int:
    antennas = extract_antennas(text)
    antinodes = set()
    ymax, xmax = len(text), len(text[0])

    for antenna in antennas.keys():
        positions = antennas[antenna].copy()

        while positions:
            y0,x0 = positions.pop(0)
            for y,x in positions:
                dy = y - y0
                dx = x - x0

                for op in [2, -1]:
                    pos = (y0+op*dy, x0+op*dx)
                    if 0 <= pos[0] < ymax and 0 <= pos[1] < xmax:
                        antinodes.add(pos)
    return len(antinodes)

print(f'Answer for Part 1: {count_antinodes(input)}')
# Solving Part 2
# ------------------------------------------------------------
def count_resonant_antinodes(text:list[str])->int:
    antennas = extract_antennas(text)
    antinodes = set()
    ymax, xmax = len(text), len(text[0])

    for antenna in antennas.keys():
        positions = antennas[antenna].copy()

        while positions:
            y0,x0 = positions.pop(0)
            for y,x in positions:
                dy = y - y0
                dx = x - x0
                op = inc = 1
                
                while True:
                    pos = (y0+op*dy, x0+op*dx)
                    if 0 <= pos[0] < ymax and 0 <= pos[1] < xmax:
                        antinodes.add(pos)
                    else:
                        if op > 0: inc = -1
                        else: break
                    op += inc

    return len(antinodes)

print(f'Answer for Part 2: {count_resonant_antinodes(input)}')