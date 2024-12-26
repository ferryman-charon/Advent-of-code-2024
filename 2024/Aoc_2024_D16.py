# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 16
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D16.txt', 'r') as f:
    input = f.read().splitlines()

test = '''###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############'''.splitlines()

test2 = '''#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################'''.splitlines()


MAZE = list[list[str]]
POS = tuple[int, int]
Dir = [(-1,0), (0,1), (1,0), (0,-1)]

def print_maze(maze:MAZE, pos=None)->None:
    if pos:
        toprint = []
        for y in range(len(maze)):
            nstr = ''
            for x in range(len(maze[0])):
                if (y,x) == pos:
                    nstr += '@'
                else:
                    nstr += maze[y][x]
            toprint.append(nstr)
        print('\n'.join(toprint))
    else:
        print('\n'.join([''.join(i) for i in maze]))
# Solving Part 1
# ------------------------------------------------------------

def parse_maze(input:list[str])->tuple[MAZE, POS, POS, set[POS]]:
    maze = []
    start, end = (), ()
    nodes = set()
    for y in range(len(input)):
        line = []
        for x in range(len(input[0])):
            if input[y][x] == 'E':
                end = (y,x)
                line.append('.')
                nodes.add((y,x))
            elif input[y][x] == 'S':
                start = (y,x)
                line.append('.')
                nodes.add((y,x))
            else:
                if input[y][x] == '.': nodes.add((y,x))
                line.append(input[y][x])
        maze.append(line)
    return maze, start, end, nodes

# meiner meinung nach sollte dieser Weg gehen!
def try1_solve_maze(maze:MAZE, d:POS, start:POS, end:POS, seen:list[POS])->int:
    y0, x0 = start
    dindex = Dir.index(d)

    if start == end: return 0
    if maze[y0][x0] == '#' or start in seen: return -1

    seen.append(start)

    dy, dx = d
    ly, lx = Dir[(dindex -1)%4]
    ry, rx = Dir[(dindex +1)%4]
    val_forward = try1_solve_maze(maze, d, (y0+dy,x0+dx), end, seen)
    val_rot_left = try1_solve_maze(maze, (ly, lx), (y0+ly, x0+lx), end, seen)
    val_rot_right = try1_solve_maze(maze, (ry, rx), (y0+ry, x0+rx), end, seen)

    vals = []
    if val_forward >= 0: vals.append(1+val_forward)
    for val in [val_rot_left, val_rot_right]:
        if val >= 0: vals.append(1001 + val)
    #print(vals)
    #print(seen)
    if not vals: return -1
    else: return min(vals) 

import heapq

def solve_maze(maze:MAZE, d, start:POS, end:POS, nodes:set[POS]):
    visited = {pos:None for pos in nodes}
    queue = [(start,d, 0)]

    while queue:
        (y0, x0), (dy ,dx), dist = heapq.heappop(queue)

        dindex = Dir.index((dy,dx))
        ly, lx = Dir[(dindex -1)%4]
        ry, rx = Dir[(dindex +1)%4]
        
        #print(f'Pos: {y0,x0} going in dir {dy,dx} and at len {dist}')
        #if (y0,x0) == end: return dist
        
        curlen = visited[(y0, x0)]
        if curlen != None:
            if curlen > dist:
                visited[(y0, x0)] = dist
            else:
                continue
        else: visited[(y0, x0)] = dist
        
        if maze[y0+dy][x0+dx] != '#':
            heapq.heappush(queue, ((y0+dy, x0+dx), (dy, dx), dist+1))
        if maze[y0+ly][x0+lx] != '#':
            heapq.heappush(queue, ((y0+ly, x0+lx), (ly,lx), dist+1001))
        if maze[y0+ry][x0+rx] != '#':
            heapq.heappush(queue, ((y0+ry, x0+rx), (ry,rx), dist+1001))

    return visited[end]

def part_one(input:list[str])->int:
    maze, start, end, nodes = parse_maze(input)
    #print_maze(maze)
    return solve_maze(maze, (0, 1), start, end, nodes)

print(f'Answer for Part 1: {part_one(input)}')


# Solving Part 2
# ------------------------------------------------------------

def find_good_seats(maze:MAZE, d, start:POS, end:POS, shortes_path:int):
    good_seats = set()
    queue = [(start,d, 0, {start})]
    visited = {}

    while queue:
        (y0, x0), (dy ,dx), dist, path = heapq.heappop(queue)
        if dist > shortes_path: continue

        dindex = Dir.index((dy,dx))
        ly, lx = Dir[(dindex -1)%4]
        ry, rx = Dir[(dindex +1)%4]

        # now it is possilbe to visit pos more than once, but differnet directions 
        pos = (y0, x0, (dy,dx))
        if pos in visited.keys() and visited[pos] < dist:
            continue
        visited[pos] = dist

        if (y0,x0) == end and dist == shortes_path: 
            good_seats.update(path)
            continue

        if maze[y0+dy][x0+dx] != '#':
            new_path = path | {(y0+dy, x0+dx)}
            heapq.heappush(queue, ((y0+dy, x0+dx), (dy, dx), dist+1, new_path))
        if maze[y0+ly][x0+lx] != '#':
            new_path = path | {(y0+ly, x0+lx)}
            heapq.heappush(queue, ((y0+ly, x0+lx), (ly,lx), dist+1001, new_path))
        if maze[y0+ry][x0+rx] != '#':
            new_path = path | {(y0+ry, x0+rx)}
            heapq.heappush(queue, ((y0+ry, x0+rx), (ry,rx), dist+1001, new_path))

    return len(good_seats)

def part_two(input:list[str])->int:
    maze, start, end, _ = parse_maze(input)
    shortest = part_one(input)
    return find_good_seats(maze, (0, 1), start, end, shortest)

print(f'Answer for Part 2: {part_two(input)}')