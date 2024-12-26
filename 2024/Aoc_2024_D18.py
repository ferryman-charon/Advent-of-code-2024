
# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 18
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D18.txt', 'r') as f:
    input = f.read().splitlines()

test = '''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0'''.splitlines()

GRID = (70, 70)
TEST_GRID = (6, 6)

# Solving Part 1
# ------------------------------------------------------------

import heapq
DIR = [(-1,0), (0, 1), (1, 0), (0, -1)]

def get_coordinates(input:list[str])->list[tuple]:
    return [tuple([int(j) for j in i.split(',')]) for i in input]

def print_maze(grid:tuple, corrupted:list[tuple])->None:
    xmax, ymax = grid
    maze = []
    for y in range(ymax+1):
        line = ''
        for x in range(xmax+1):
            if (x,y) in corrupted: line += '#'
            else: line += '.'
        maze.append(line)
    print('\n'.join(maze))


def solve_maze(grid:tuple, fallen_bytes:int, input:list[str]):
    corrupted = get_coordinates(input)[:fallen_bytes]
    # print_maze(grid, corrupted)
    xmax, ymax = grid
    visited = {}

    for y in range(ymax+1):
        for x in range(xmax+1):
            if (x,y) in corrupted:continue
            visited[(x,y)] = None

    queue = [((0,0), 0)]

    while queue:
        (x0, y0), dist = heapq.heappop(queue)
        #print(x0,y0)
        
        curlen = visited[(x0, y0)]
        if curlen != None:
            if curlen > dist: visited[(x0, y0)] = dist
            else: continue
        else: visited[(x0, y0)] = dist
        
        if (x0, y0) == (xmax, ymax): break

        for dx, dy in DIR:
            nx, ny = x0 + dx, y0 + dy 
            if nx < 0 or nx > xmax or ny < 0 or ny > ymax: continue

            if (nx, ny) in corrupted: continue
            heapq.heappush(queue, ((nx, ny), dist+1)) 

    return visited[(xmax, ymax)]

print(f'Answer for Part 1: {solve_maze(GRID, 1024, input)}')

# Solving Part 2
# ------------------------------------------------------------

def fsolve_maze(grid:tuple, corrupted):
    xmax, ymax = grid
    visited = {}

    for y in range(ymax+1):
        for x in range(xmax+1):
            if (x,y) in corrupted:continue
            visited[(x,y)] = None

    queue = [((0,0), 0)]

    while queue:
        (x0, y0), dist = heapq.heappop(queue)
        #print(x0,y0)
        
        curlen = visited[(x0, y0)]
        if curlen != None:
            if curlen > dist: visited[(x0, y0)] = dist
            else: continue
        else: visited[(x0, y0)] = dist
        
        if (x0, y0) == (xmax, ymax): break

        for dx, dy in DIR:
            nx, ny = x0 + dx, y0 + dy 
            if nx < 0 or nx > xmax or ny < 0 or ny > ymax: continue

            if (nx, ny) in corrupted: continue
            heapq.heappush(queue, ((nx, ny), dist+1)) 

    if visited[(xmax, ymax)] == None: return False
    else: return visited[(xmax, ymax)]

def exaust_find_byte(grid:tuple, input:list[str]):
    corrupted = get_coordinates(input)

    i = 2950
    while i < len(corrupted):
        v = fsolve_maze(grid, corrupted[:i])
        # print(f'for {i} maze is {v}' )
        if not v: return corrupted[i]
        i+=1
    return 0

print(f'Answer for Part 1: {exaust_find_byte(GRID, input)}')
