# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 14
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D14.txt', 'r') as f:
    input = f.read().splitlines()

test = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3'''.splitlines()

def parse_input(input:list[str])->list[tuple]:
    robots = []
    for line in input:
        pos, vel = [tuple([int(i) for i in l[2:].split(',')]) for l in line.split()]
        robots.append((pos, vel))
    return robots

TESTSPACE = (11,7)
SPACE = (101, 103) 

# Solving Part 1
# ------------------------------------------------------------
def move_robots(robots_instr:list[tuple], space:tuple)->list[tuple]:
    positions = []
    xspace , yspace = space
    for instr in robots_instr:
        (x,y), (vx ,vy) = instr
        xf = (x + 100*vx)%xspace
        yf = (y + 100*vy)%yspace
        positions.append((xf, yf))
    return positions

def safety_factor(input:list[str], space:tuple):
    robots = parse_input(input)
    robot_pos = move_robots(robots_instr=robots, space=space)
    q1, q2, q3, q4 = 0, 0, 0, 0
    xmid = space[0]//2
    ymid = space[1]//2

    for x,y in robot_pos:
        if x < xmid and y < ymid: q1 += 1
        elif x > xmid and y < ymid: q2 += 1
        elif x < xmid and y > ymid: q3 += 1
        elif x > xmid and y > ymid: q4 += 1
        else: pass
    return q1*q2*q3*q4

#print(f'Answer for Part 1: {safety_factor(input, SPACE)}')


# Solving Part 2
# ------------------------------------------------------------
import time
def parse_input(input:list[str])->list[tuple]:
    robot_pos, robot_vel = [],[]
    for line in input:
        pos, vel = [tuple([int(i) for i in l[2:].split(',')]) for l in line.split()]
        robot_pos.append(pos)
        robot_vel.append(vel)
    return robot_pos, robot_vel

def move_robots_once(robot_pos:list[tuple], robot_vel:list[tuple], space:tuple):
    positions = []
    xspace , yspace = space
    for i in range(len(robot_pos)):
        (x,y) = robot_pos[i]
        (vx ,vy) = robot_vel[i]

        xf = (x + vx)%xspace
        yf = (y + vy)%yspace
        positions.append((xf, yf))
    return positions

def draw_robots(robot_pos:list[tuple], space:tuple, stepnumber)->None:
    filename = 'Projects/Advent_of_code/2024/picture_day14.txt'
    open(filename, 'w').close()
    lines = []
    lines.append('\n')
    lines.append(f'Stepnumber {stepnumber}\n')
    for y in range(space[1]):
        line = ''
        for x in range(space[0]):
            if (x,y) in robot_pos: line += '#'
            else: line += '.'
        line += '\n'
        lines.append(line)

    with open(filename, 'w') as f:
        f.writelines(lines)

def check_tree(robot_pos:list[tuple]):
    for i in range(len(robot_pos)):
        x,y = robot_pos[i]
        for j in range(1, 6):
            xn = x+j
            if not (xn, y) in robot_pos:
                break
        else:
            return True   
    return False


def loop_robots(input:list[str], space:tuple):
    filename = 'Projects/Advent_of_code/2024/data/picture_day14.txt'
    robot_pos, robot_vel = parse_input(input)
    counter = 0
    lines = []

    def append_to_lines(lines:list[str])->None:
        lines.append('\n')
        lines.append(f'Stepnumber {counter}\n')
        for y in range(space[1]):
            line = ''
            for x in range(space[0]):
                if (x,y) in robot_pos: line += '#'
                else: line += '.'
            line += '\n'
            lines.append(line)   

    while counter <= 10404:
        counter += 1

        robot_pos = move_robots_once(robot_pos, robot_vel, space)
        if check_tree(robot_pos):
            print(counter)
            append_to_lines(lines)
    
    with open(filename, 'w') as f:
        f.writelines(lines)


print(loop_robots(input, SPACE))

#from pynput.keyboard import Key, Listener
#
#def on_press(key):
#    global positions, robot_pos, counter
#    positions.append(robot_pos)
#    counter += 1
#
#    robot_pos = move_robots_once(robot_pos, robot_vel, SPACE)
#    if robot_pos in positions:
#        return counter
#    draw_robots(robot_pos, SPACE)
#
#
#def on_release(key):
#    if key == Key.esc:
#        return False	
#
#if __name__=='__main__':
#	with Listener(on_press=on_press, on_release=on_release) as listener:
#		listener.join()  
