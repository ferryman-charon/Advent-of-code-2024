# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 6
# - 2024 
# 
# ------------------------------------------------------------
import time
WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D06.txt', 'r') as f:
   input = f.read()

test = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''

# Solving Part 1
# ------------------------------------------------------------
DIR = ['n', 'e', 's', 'w']

LEFT_MAZE = 0
ROTATE_RIGHT = 1
CONT_WALKING = 2


def format_input(text:str):
    text = text.split()
    for line in range(len(text)):
        for row in range(len(text[0])):
            if text[line][row] == '^':
                return (line, row), text
    return False

def check_dir(maze:list[str], pos:tuple, direction:str, critpos=(None,None))->int:
    y,x = pos 
    match direction:
        case 'n':
            if y-1 >= 0:
                if maze[y-1][x] == '#' or (y-1,x) == critpos:
                    return ROTATE_RIGHT
                else:
                    return CONT_WALKING
            else:
                return LEFT_MAZE
        case 's':
            #print(len(maze),y)
            if y < len(maze)-1:
                if maze[y+1][x] == '#'or (y+1,x) == critpos:
                    return ROTATE_RIGHT
                else:
                    return CONT_WALKING
            else:
                return LEFT_MAZE
        case 'e':
            if x < len(maze[0])-1:
                if maze[y][x+1] == '#' or (y,x+1) == critpos:
                    return ROTATE_RIGHT
                else:
                    return CONT_WALKING
            else:
                return LEFT_MAZE
        case 'w':
            if x-1 >= 0:
                if maze[y][x-1] == '#' or (y,x-1) == critpos:
                    return ROTATE_RIGHT
                else:
                    return CONT_WALKING
            else:
                return LEFT_MAZE

def find_critical_pos(text:str):
    direction = DIR[0]
    (y0,x0), maze = format_input(text=text)
    visited = set()

    while True:
        #print(y0,x0)
        instr = check_dir(maze=maze, pos=(y0,x0), direction=direction)

        visited.add((y0,x0))

        if not instr:
            return len(visited)
        if instr == CONT_WALKING:
            match direction:
                case 'n': y0 -= 1
                case 's': y0 += 1
                case 'e': x0 += 1
                case 'w': x0 -= 1
        if instr == ROTATE_RIGHT:
            d = DIR.index(direction)
            direction = DIR[(d+1)%4]
  


print(f'Answer for Part 1: {find_critical_pos(input)}')


# Solving Part 2
# ------------------------------------------------------------
def return_critical_pos(text:str)->list[tuple]:
    direction = DIR[0]
    (y0,x0), maze = format_input(text=text)
    visited = set()

    while True:
        instr = check_dir(maze=maze, pos=(y0,x0), direction=direction)

        visited.add((y0,x0))

        if not instr:
            return list(visited)
        if instr == CONT_WALKING:
            match direction:
                case 'n': y0 -= 1
                case 's': y0 += 1
                case 'e': x0 += 1
                case 'w': x0 -= 1
        if instr == ROTATE_RIGHT:
            d = DIR.index(direction)
            direction = DIR[(d+1)%4]

def find_loop(maze, startpos, startdir, critpos):
    direction = startdir
    y0, x0 = startpos
    visited = []

    while True:
        for pos, direc in visited:
            if (y0,x0) == pos and direction == direc:
                return True

        instr = check_dir(maze=maze, pos=(y0,x0), direction=direction, critpos=critpos)

        if not instr:
            break
        if instr == CONT_WALKING:
            visited.append(((y0,x0),direction))
            match direction:
                case 'n': y0 -= 1
                case 's': y0 += 1
                case 'e': x0 += 1
                case 'w': x0 -= 1
        if instr == ROTATE_RIGHT:
            d = DIR.index(direction)
            direction = DIR[(d+1)%4]
        
    return False

def find_loop_pos(text:str):
    direction = DIR[0]
    result = 0
    it = 0
    (y0,x0), maze = format_input(text=text)
    critical = return_critical_pos(text=text)
    for position in critical:
        it += 1
        print(it)
        if find_loop(maze, (y0,x0),direction, position):
            result += 1
    return result

# Attemt 2
# ------------------------------------------------------------
def find_loop(maze:list[str], startpos:tuple, startdir:str, critpos:tuple, marked:list[tuple]):
    direction = startdir
    y0, x0 = startpos
    visited = [i for i in marked]

    while True:

        for pos, direc in visited:
            if (y0,x0) == pos and direction == direc:
                return True

        instr = check_dir(maze=maze, pos=(y0,x0), direction=direction, critpos=critpos)

        if not instr:
            break
        if instr == CONT_WALKING:
            visited.append(((y0,x0),direction))
            match direction:
                case 'n': y0 -= 1
                case 's': y0 += 1
                case 'e': x0 += 1
                case 'w': x0 -= 1
        if instr == ROTATE_RIGHT:
            d = DIR.index(direction)
            direction = DIR[(d+1)%4]
        
    return False

def find_loop_pos(text:str):
    result = 0
    direction = DIR[0]
    (y0,x0), maze = format_input(text=text)
    visited = []

    while True:
        print(result)
        instr = check_dir(maze=maze, pos=(y0,x0), direction=direction)

        if not instr:
            return result
        if instr == CONT_WALKING:
            match direction:
                case 'n':
                    if find_loop(maze, (y0,x0), direction, (y0-1,x0),visited[:-1]):
                        #print(f'found loop at {y0,x0}')
                        result += 1
                    y0 -= 1
                    visited.append(((y0,x0),direction))
                case 's': 
                    if find_loop(maze, (y0,x0), direction, (y0+1,x0),visited[:-1]):
                        #print(y0,x0)
                        result += 1
                    y0 += 1
                    visited.append(((y0,x0),direction))
                case 'e': 
                    if find_loop(maze, (y0,x0), direction, (y0,x0+1),visited[:-1]):
                        #print(y0,x0)
                        result += 1
                    x0 += 1
                    visited.append(((y0,x0),direction))
                case 'w': 
                    if find_loop(maze, (y0,x0), direction, (y0,x0-1),visited[:-1]):
                        #print(y0,x0)
                        result += 1
                    x0 -= 1
                    visited.append(((y0,x0),direction))

        if instr == ROTATE_RIGHT:
            d = DIR.index(direction)
            direction = DIR[(d+1)%4]
# ------------------------------------------------------------

# Both are slow as fuck 
print(f'Answer for Part 2: {find_loop_pos(input)}')