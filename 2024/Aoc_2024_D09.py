# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 9
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D09.txt', 'r') as f:
    input = f.read()

test = '''2333133121414131402'''

# Solving Part 1
# ------------------------------------------------------------

def disk_map(input:str)->list[str]:
    id_number = 0
    dmap = []

    for i in range(len(input)):
        if not i%2:
            for _ in range(int(input[i])):
                dmap.append(str(id_number))
            id_number += 1
        else:
            for _ in range(int(input[i])):
                dmap.append('.')
    return dmap

def format_disk(disk_map:list[str])->list[str]:
    dmap = disk_map.copy()
    rindex = len(dmap)-1

    for i in range(len(dmap)):
        if dmap[i] == '.':
            while True:
                if dmap[rindex] != '.':
                    break
                rindex -= 1
            
            if rindex < i:

                return dmap
            
            dmap[i] = dmap[rindex]
            dmap[rindex] = '.'
    return -1

def calculate_checksum(disk:list[str])->int:
    checksum = 0
    for i in range(len(disk)):
        if disk[i] == '.':
            break
        checksum += (i*int(disk[i]))
    return checksum

def solve_part_one(input:str)->int:
    fdisk = format_disk(disk_map=disk_map(input))
    return calculate_checksum(disk=fdisk)


print(f'Answer for Part 1: {solve_part_one(input)}')

# Solving Part 2
# ------------------------------------------------------------
HASH_DMAP = list[tuple[int,str]]
DMAP = list[str]
import time
def hash_disk_map(input:str)->HASH_DMAP:
    id_number = 0
    dmap = []

    for i in range(len(input)):
        if not i%2:
            dmap.append((int(input[i]), str(id_number)))
            id_number += 1
        else:
            dmap.append((int(input[i]),'.'))
    return dmap

def fastformat_disk(disk_map:HASH_DMAP)->HASH_DMAP:
    disk = disk_map.copy()
    rindex = len(disk)-1
    start_index = 0

    while rindex > 0:
        rval, robj = disk[rindex]
        if robj != '.':
            found = False
            for i in range(start_index,rindex):
                val, obj = disk[i]
                if obj == '.':
                    if not found:
                        start_index = i
                        found = True
                    if val >= rval:
                        tempval, tempobj = disk[i]
                        disk[i] = (tempval- rval, tempobj)
                        disk[rindex] = (rval, '.')
                        disk.insert(i, (rval, robj))
                        break
            
        rindex -= 1
    return disk


def unhash_dmap(hdisk_map:HASH_DMAP)->DMAP:
    dmap = []
    for cnt, obj in hdisk_map:
        for _ in range(cnt):
            dmap.append(obj)
    return dmap

def calcu_checksum_2(disk:list[str])->int:
    checksum = 0
    for i in range(len(disk)):
        if disk[i] == '.':
            continue
        checksum += (i*int(disk[i]))
    return checksum

def solve_part_two(text:str)->int:
    hfdisk = fastformat_disk(disk_map=hash_disk_map(text))
    return calcu_checksum_2(unhash_dmap(hfdisk))

print(f'Answer for Part 2: {solve_part_two(input)}')