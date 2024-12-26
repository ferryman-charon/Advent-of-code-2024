# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 15
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D15.txt', 'r') as f:
    input = f.read()

test = '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<'''

test2 = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^'''

MAZE = list[list[str]]
POS = tuple[int,int]

Directions = {'^':(-1, 0), '>':(0, 1), 'v':(1, 0), '<':(0, -1)}

def parse_input(input:str)->tuple[MAZE,str,POS]:
    maze, instr = input.split('\n\n')
    maze = maze.split()
    instr = ''.join(instr.split())
    newmaze = []
    pos = []
    for y in range(len(maze)):
        newline = []
        for x in range(len(maze[0])):
            if maze[y][x] == '@':
                pos.append((y,x))
                newline.append('.')
                continue
            newline.append(maze[y][x])
        newmaze.append(newline)
    return newmaze, instr, pos[0]

# Solving Part 1
# ------------------------------------------------------------

def move_robot(maze:MAZE, instr:str, pos:POS)->tuple[MAZE, POS]:
    y0, x0 = pos
    dy, dx = Directions[instr]
    y, x = y0 + dy, x0 + dx

    if maze[y][x] == '.': return maze, (y, x)
    if maze[y][x] == '#': return maze, pos

    i = 1
    while True:
        ny, nx = y0+i*dy, x0+i*dx
        if not (0 <= nx < len(maze[0]) and 0 <= ny < len(maze)):
            return maze, pos
        
        if maze[ny][nx] == '.':
            maze[ny][nx] = 'O'
            maze[y][x] = '.'
            return maze, (y,x)
        
        elif maze[ny][nx] == '#': return maze, pos
        else: i += 1

def get_GPS_value(maze:MAZE)->int:
    gps_val = 0
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'O' or maze[y][x] == '[':
                gps_val += (100*y + x)
    return gps_val

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

def calc_robot_behaviour(input:str)->MAZE:
    maze, instr, pos = parse_input(input)
    for move in instr:
        maze, pos = move_robot(maze, move, pos)

    #print_maze(maze)
    return get_GPS_value(maze)

print(f'Answer for Part 1: {calc_robot_behaviour(input)}')

# Solving Part 2
# ------------------------------------------------------------

test3 = '''#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^'''

import time

def strech_input(input:str)->tuple[MAZE, str, POS]:
    maze, instr = input.split('\n\n')
    maze = maze.split()
    instr = ''.join(instr.split())
    newmaze = []
    pos = []
    for line in maze:
        newline = []
        for c in line:
            if c == '@':
                newline.append('@')
                newline.append('.')
            elif c == 'O':
                newline.append('[')
                newline.append(']')
            else:    
                newline.append(c)
                newline.append(c)

        newmaze.append(newline)
    for y in range(len(newmaze)):
        for x in range(len(newmaze[0])):
            if newmaze[y][x] == '@':
                pos.append((y,x))
                newmaze[y][x] = '.'
                break 
    return newmaze, instr, pos[0]



def move_robot_double(maze:MAZE, instr:str, pos:POS)->tuple[MAZE, POS]:
    y0, x0 = pos
    dy, dx = Directions[instr]
    y, x = y0 + dy, x0 + dx

    if maze[y][x] == '.': return maze, (y, x)
    if maze[y][x] == '#': return maze, pos

    # consider 2 cases:
    # 1. moving horizontaly
    if dx != 0:
        i = 1
        while True:
            nx = x0 + i*dx
            if nx < 0 or nx >= len(maze[0]):
                return maze, pos
            
            if maze[y0][nx] == '.':
                # shift in dir
                if dx > 0:
                    left = maze[y0][:x0+1]
                    boxes = maze[y0][x0+1:nx]
                    right = maze[y0][nx+1:]
                    maze[y0] = left + ['.'] + boxes + right
                    return maze, (y0, x0+1)
                else:
                    left = maze[y0][:nx]
                    boxes = maze[y0][nx+1:x0]
                    right = maze[y0][x0:]
                    maze[y0] = left + boxes + ['.'] + right
                    return maze, (y0, x0-1)
            elif maze[y0][nx] == '#': return maze, pos
            else: i += 1

    # 2. move vertically
    else:
        def legal_move_vert(maze:MAZE, pos:POS, dy:int)->bool:
            y0, x0 = pos
            #print(pos)
            ny = y0 + dy
            if maze[y0][x0] == '.': return True
            elif maze[y0][x0] == '[':
                if legal_move_vert(maze,(y0+dy, x0),dy) and legal_move_vert(maze, (y0+dy, x0 + 1), dy): return True
            elif maze[y0][x0] == ']':
                if legal_move_vert(maze,(y0+dy, x0),dy) and legal_move_vert(maze, (y0+dy, x0 - 1), dy): return True
            
            else: return False
        
        def move_box_vert(maze:MAZE, pos:POS, dy:int)->None:
            y0, x0 = pos
            ny = y0 + dy

            if maze[y0][x0] == ']':
                if maze[ny][x0] == '.' and maze[ny][x0-1] == '.':
                    maze[ny][x0] = ']'
                    maze[ny][x0-1] = '['
                    maze[y0][x0] = '.'
                    maze[y0][x0-1] = '.'
                else:
                    move_box_vert(maze, (ny, x0), dy)
                    move_box_vert(maze, (ny, x0-1), dy)
                    move_box_vert(maze,pos,dy)

            if maze[y0][x0] == '[':
                if maze[ny][x0] == '.' and maze[ny][x0+1] == '.':
                    maze[ny][x0] = '['
                    maze[ny][x0+1] = ']'
                    maze[y0][x0] = '.'
                    maze[y0][x0+1] = '.'
                else:
                    move_box_vert(maze, (ny, x0), dy)
                    move_box_vert(maze, (ny, x0+1), dy)
                    move_box_vert(maze,pos,dy)

        #print('checking mov vert')
        if legal_move_vert(maze, (y0+dy,x0), dy):
            #print('yes')
            # find box attributes
            i = 1
            while True:
                ny = y0 + i*dy
                if maze[ny][x0] == '.': break
                else: i+=1
            
            move_box_vert(maze,(y0+dy,x0),dy)
            return maze, (y0+dy, x0)

        else:
            return maze, pos

def calc_robot2_behaviour(input:str)->MAZE:
    maze, instr, pos = strech_input(input)
    for move in instr:
        #print(f'\n {pos} mov to make {move}')
        #print_maze(maze, pos)
        
        maze, pos = move_robot_double(maze, move, pos)
    #print_maze(maze,pos)

    return get_GPS_value(maze)

print(f'Answer for Part 2: {calc_robot2_behaviour(input)}')