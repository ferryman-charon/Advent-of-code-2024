# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 12
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D12.txt', 'r') as f:
    input = f.read().splitlines()

test = '''EEEEE
EXXXX
EEEEE
EXXXX
EEEEE'''.splitlines()

test2 = '''RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE'''.splitlines()

test3 = '''AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA'''.splitlines()

# Solving Part 1
# ------------------------------------------------------------

DIRECTION = [(-1,0), (0, 1), (1, 0), (0, -1)]
def path_to_start(gmap:list[str], start:tuple, end:tuple, search:set, moveon:str)->bool:
    y0, x0 = start

    if start == end:
        return True
    if gmap[y0][x0] != moveon:
        return False
    
    search.add(start)

    for dy, dx in DIRECTION:
        if not 0 <= y0+dy < len(gmap) or not 0 <= x0+dx < len(gmap[0]):
            continue
        if (y0+dy, x0+dx) in search:
            continue
        
        if gmap[y0+dy][x0+dx] == moveon:
            if path_to_start(gmap, (y0+dy, x0 +dx), end, search, moveon): return True

    return False

GDICT =  dict[tuple,tuple[list[tuple],int,int]]

def find_garden_values(gmap:list[str])->GDICT:
    garden_dict = {}
    for y in range(len(gmap)):
        for x in range(len(gmap[0])):
            gtype = gmap[y][x]
            perim = 4
            for dy, dx in DIRECTION:
                if not 0 <= y+dy < len(gmap) or not 0 <= x+dx < len(gmap[0]):
                    continue
                if gmap[y+dy][x+dx] == gtype:
                    perim -= 1

            create = True
            for (y0, x0) in garden_dict.keys():

                if gtype != gmap[y0][x0]:
                    continue

                outside, area, diam = garden_dict[(y0,x0)]
                if path_to_start(gmap, (y,x), (y0,x0), set(), gtype):
                    if perim > 0:
                        outside.append((y,x))
                    area += 1
                    diam += perim
                    garden_dict[(y0,x0)] = (outside, area, diam)
                    create = False
                    break

            if create:
                garden_dict[(y,x)] = ([(y,x)], 1, perim)
 
    return garden_dict

def calculate_fence_cost(garden_map:list[str])->int:
    garden_vals = find_garden_values(gmap=garden_map)
    result = 0
    for (y0, x0), (_, area, perim) in garden_vals.items():

        result += area*perim

    return result

print(f'Answer for Part 1: {calculate_fence_cost(test2)}')


# Solving Part 2
# ------------------------------------------------------------
      
def find_sides(gmap:list[str],circum: list[tuple])->int:
    circum_dict = {}
    for (y,x) in circum:
        gtype = gmap[y][x]
        perim = []
        for dy, dx in DIRECTION:
            if 0 <= y+dy < len(gmap) and 0 <= x+dx < len(gmap[0]):
                if gmap[y+dy][x+dx] == gtype:
                    continue
            perim.append((dy, dx))
        circum_dict[(y,x)] = perim
    sides = 0

    for yi, xi in circum_dict.keys():
        neighbour_dir = set()
        pos_sides = []
        for dy, dx in DIRECTION:
            if not 0 <= yi+dy < len(gmap) or not 0 <= xi+dx < len(gmap[0]):
                pos_sides.append((dy,dx))
                continue

            if gmap[yi+dy][xi+dx] == gtype:
                if (yi+dy, xi+dx) in circum_dict.keys() and (dy < 0 or dx < 0):
                    for d in circum_dict[(yi+dy, xi+dx)]:
                        neighbour_dir.add(d)
            else:
                pos_sides.append((dy,dx))
        for direct in pos_sides:
            if not direct in neighbour_dir:
                sides += 1
                
    return sides

def calculate_bulk_price(garden_map:list[str])->int:
    garden_vals = find_garden_values(gmap=garden_map)
    result = 0
    print('garden_dict', len(garden_vals))
    for (circum, area, perim) in garden_vals.values():
        #print('circum', circum)
        sides = find_sides(garden_map, circum)
        #print('sides', sides)
        result += area*sides
    return result

print(f'Answer for Part 2: {calculate_bulk_price(input)}')