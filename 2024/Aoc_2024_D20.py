# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 20
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D20.txt', 'r') as f:
    input = f.read().splitlines()

test = '''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############'''.splitlines()

# Solving Part 1
# ------------------------------------------------------------

import heapq
from collections import Counter

MAZE = list[list[str]]
POS = tuple[int,int]

Directions = [(-1,0), (0,1), (1,0), (0,-1)]

def parse_input(input:list[str])->tuple[MAZE, POS, POS]:
    maze = []
    start, end = 0 ,0
    for y in range(len(input)):
        line = []
        for x in range(len(input[0])):
            if input[y][x] == 'S': 
                start = (y,x)
                line.append('.')
            elif input[y][x] == 'E': 
                end = (y,x)
                line.append('.')
            else: line.append(input[y][x])
        maze.append(line)
    return maze, start, end

def node_costs(maze:MAZE, start:POS, end:POS)->dict[POS,int]:
    nodes = {}
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == '.': nodes[(y,x)] = None
    
    queue = [(start, 0)]
    while queue:
        (y0,x0), cost = heapq.heappop(queue)

        node_cost = nodes[(y0,x0)]
        if node_cost != None:
            if cost < node_cost: nodes[(y0,x0)] = cost
            else: continue
        else: nodes[(y0,x0)] = cost

        for dy,dx in Directions:
            ny, nx = y0+dy, x0+dx
            if maze[ny][nx] != '#': heapq.heappush(queue, ((ny,nx), cost+1))
            else: continue
    return nodes

def find_s_shorcuts(input:list[str])->tuple:
    def count_savetime(shortcuts:list[int], value:int)->int:
        result = 0
        for item in shortcuts:
            if item >= value: result += 1
        return result
    
    maze, start, end = parse_input(input)
    ymax, xmax = len(maze), len(maze[0])
    costs = node_costs(maze, start, end)
    shorcuts = []

    for y in range(1, ymax - 1):
        for x in range(1, xmax - 1):
            if maze[y][x] == '#':
                vertic = maze[y-1][x] == '.' and maze[y+1][x] == '.'
                horizont = maze[y][x-1] == '.' and maze[y][x+1] == '.'

                if vertic: shorcuts.append(abs(costs[(y-1, x)] - costs[(y+1, x)]) - 2)
                if horizont: shorcuts.append(abs(costs[(y, x-1)] - costs[(y, x+1)]) - 2)
    
    return count_savetime(shorcuts,100)

    
print(f'Answer for Part 1: {find_s_shorcuts(input)}')


# Solving Part 2
# ------------------------------------------------------------

CHEAT_TIME = 20

# ok keine Ahnung wo der Fehler ist
def v1_find_long_shortcuts(maze:MAZE, pos:POS, end:POS, costs:dict[POS,int], time_max:int)->int:
    ymax, xmax = len(maze), len(maze[0])
    start_cost = costs[pos]
    yf, xf = end
    queue = [(pos, set(), 20)]
    shortcuts = {}

    while queue:
        (y,x) , seen, cost = heapq.heappop(queue)
        print(len(queue))

        if cost<0: continue
        if y<0 or x<0 or y>=ymax or x>=xmax: continue
        if (y,x) in seen:continue

        newseen = seen.copy()
        newseen.add(((y,x)))

        for dy ,dx in Directions:
            ny, nx = y+dy, x+dx
            if (ny, nx) in seen: continue
            heapq.heappush(queue, ((ny,nx), newseen, cost-1))
        
        if not (y,x) in costs: continue

        save_value = costs[(y,x)] - start_cost - (20-cost)

        if save_value < time_max: continue

        if (y,x) in shortcuts.keys():
            short_values = shortcuts[(y,x)]
            if not save_value in short_values: 
                short_values.append(save_value)
                shortcuts[(y,x)] = short_values
        else:
            shortcuts[(y,x)] = [save_value]

    
    return sum([len(s) for s in shortcuts.values()])

def find_long_shortcuts(maze:MAZE, pos:POS, costs:dict[POS,int], time_max:int)->int:
    def out_of_bound(position, ymax=len(maze), xmax=len(maze[0])):
        y,x = position
        return y<0 or y>=ymax or x<0 or x>=xmax
    y0,x0 = pos
    start_cost = costs[pos]
    pos_cheats = 0

    for dy in range(-CHEAT_TIME, CHEAT_TIME + 1):
        for dx in range(-CHEAT_TIME, CHEAT_TIME + 1):
            if dy == 0 and dx == 0:
                continue

            cheat_cost = abs(dy) + abs(dx)
            if cheat_cost > CHEAT_TIME:
                continue 

            ny, nx = y0 + dy, x0 + dx

            if out_of_bound((ny,nx)):continue
            if maze[ny][nx] == '#': continue
          
            save_time = costs[(ny,nx)] - start_cost - cheat_cost
            if save_time >= time_max:
                pos_cheats += 1

    return pos_cheats


def count_l_shortcuts(input:list[str])->int:
    maze, start, end = parse_input(input)
    costs = node_costs(maze, start, end)
    count = 0

    # the idea ist to take every possible node and calculate the number of shortcuts from that node with more than 100 ps save time
    for node in costs.keys():
        #print(node, count)
        count += find_long_shortcuts(maze, node, costs, 100)

    return count

print(f'Answer for Part 2: {count_l_shortcuts(input)}')