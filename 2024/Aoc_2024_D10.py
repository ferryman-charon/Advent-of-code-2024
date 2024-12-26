# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 10
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D10.txt', 'r') as f:
   input = f.read().splitlines()

test = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732'''.splitlines()

# Solving Part 1
# ------------------------------------------------------------
DIRECTIONS = [(-1,0), (0, 1), (1, 0), (0, -1)]

def conv_to_intmap(textmap:list[str])->list[list[int]]:
    return [[int(i) for i in line] for line in textmap]

def follow_trail(tmap:list[list[int]], pos:tuple[int], visited:set[tuple])->int:
    '''recursively follow the trail to find the number of trails that lead to 
    the different possible end positions. Moving on visited tiles is prohibited'''

    ys, xs = pos
    if tmap[ys][xs] == 9:
        return 1
    
    trailnum = 0
    visited.add(pos)
    for dy, dx in DIRECTIONS:
        if ys+dy < 0 or ys+dy>=len(tmap) or xs+dx < 0 or xs+dx>=len(tmap[0]):
            continue

        if tmap[ys+dy][xs+dx] - tmap[ys][xs] == 1:
            if (ys+dy, xs+dx) in visited:
                continue
            visited.add((ys+dy, xs+dx))
            trailnum += follow_trail(tmap=tmap, pos=(ys+dy, xs+dx), visited=visited)
    return trailnum


def find_trailheads(textmap:list[str])->int:
    topmap = conv_to_intmap(textmap=textmap)
    trailheads = 0
    for y in range(len(topmap)):
        for x in range(len(topmap[0])):
            if topmap[y][x] == 0:
                trailheads += follow_trail(tmap=topmap, pos=(y,x), visited=set())
    return trailheads


print(f'Answer for Part 1: {find_trailheads(input)}')


# Solving Part 2
# ------------------------------------------------------------

def find_paths(tmap:list[list[int]], pos:tuple[int])->int:
    '''recursively follow the trail to find the number of different trails that 
    lead to all different end positions. Moving on visited tiles is now allowed'''
    
    ys, xs = pos
    if tmap[ys][xs] == 9:
        return 1
    
    trailnum = 0
    for dy, dx in DIRECTIONS:
        if ys+dy < 0 or ys+dy>=len(tmap) or xs+dx < 0 or xs+dx>=len(tmap[0]):
            continue

        if tmap[ys+dy][xs+dx] - tmap[ys][xs] == 1:
            trailnum += find_paths(tmap=tmap, pos=(ys+dy, xs+dx))
    return trailnum


def trailhead_ratings(textmap:list[str])->int:
    topmap = conv_to_intmap(textmap=textmap)
    trailheads = 0
    for y in range(len(topmap)):
        for x in range(len(topmap[0])):
            if topmap[y][x] == 0:
                trailheads += find_paths(tmap=topmap, pos=(y,x))
    return trailheads

print(f'Answer for Part 2: {trailhead_ratings(input)}')