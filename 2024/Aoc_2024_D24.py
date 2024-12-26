# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 24
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/eudaemon/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D24.txt', 'r') as f:
    input = f.read()

test = '''x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj'''

INSTR_VAL = dict[str,int]
OPERATONS = list[tuple[str]]

def parse_input(input:str)->tuple[INSTR_VAL,OPERATONS]:
    initial, operations = input.split('\n\n')
    start_vals = {}
    for line in initial.splitlines():
        name, num = line.split(':')
        start_vals[name] = int(num)
    
    wire_operations = []
    for op in operations.splitlines():
        inp1, instr, inp2, _, out =  op.split()
        wire_operations.append((inp1, inp2, instr, out))
    return start_vals, wire_operations

# Solving Part 1
# ------------------------------------------------------------

def bool_instr(a:int,b:int, instr:str)->int:
    match instr:
        case 'OR':  return int(a | b) 
        case 'AND': return int(a & b)
        case 'XOR': return int(a ^ b)
        case _ : return -1

def operate_wires(input:str)->int:
    start_vals, wire_operations = parse_input(input)
    i = 0
    while True:
        if not wire_operations: break
        if i >= len(wire_operations):i=0

        inp1, inp2, instr, out = wire_operations[i]

        if inp1 in start_vals.keys() and inp2 in start_vals.keys():
            start_vals[out] = bool_instr(start_vals[inp1],start_vals[inp2], instr)
            wire_operations.pop(i)
        else: i+=1
    
    result = sorted([v for v in start_vals.keys() if 'z' in v])
    
    num = ''
    for val in result[::-1]:
        num += str(start_vals[val])
    return int(num,2)

print(f'Answer for Part 1: {operate_wires(input)}')


# Solving Part 2
# ------------------------------------------------------------

def f_operate_wires(start_vals:INSTR_VAL, operations:OPERATONS)->str:
    wire_operations = operations.copy()
    i = 0
    while True:
        if not wire_operations: break
        if i >= len(wire_operations):i=0

        inp1, inp2, instr, out = wire_operations[i]

        if inp1 in start_vals.keys() and inp2 in start_vals.keys():
            start_vals[out] = bool_instr(start_vals[inp1],start_vals[inp2], instr)
            wire_operations.pop(i)
        else: i+=1
    
    result = sorted([v for v in start_vals.keys() if 'z' in v], reverse=True)
    return ''.join([str(start_vals[i]) for i in result])

def expected_sum(start_vals:INSTR_VAL)->tuple[int]:
    x = sorted([i for i in start_vals.keys() if 'x' in i], reverse=True)
    y = sorted([i for i in start_vals.keys() if 'y' in i], reverse=True)

    xv = ''.join([str(start_vals[i]) for i in x])
    yv = ''.join([str(start_vals[i]) for i in y])
    z = bin(int(xv,2)+int(yv,2))[2:]
    return z

# ist nicht die Lösung
def follow_zs(wrong_z:list[str], wire_operations:OPERATONS)->list[str]:
    to_permute_nodes = []
    check_fields = [] 
    operations = wire_operations.copy()

    for znode in wrong_z:
        for i in range(len(operations)):
            if znode in operations[i]: 
                to_permute_nodes.append(operations[i])
                check_fields.extend(operations[i][0:2])
                operations.pop(i)
                break
    while check_fields:
        if not operations: return -1

        node = check_fields.pop()
        i = 0
        while i < len(operations):
            a, b , ins, out = operations[i]
            if out == node: 
                check_fields.extend([a,b])
                to_permute_nodes.append(operations[i])
                operations.pop(i)
            else: i += 1
    return to_permute_nodes

def visualize(input):
    def print_gate_connections(gate_relation, key, depth=0):
        if depth == 3 or key[0] in ("x", "y"):
            return key
        input1, gate, input2 = gate_relation[key]
        return f"({key}=[{print_gate_connections(gate_relation, input1, depth + 1)} {gate} {print_gate_connections(gate_relation, input2, depth + 1)}])"

    start_vals, wire_operations = parse_input(input)
    gate_relations = {}
    for a,b,ins,out in wire_operations:
        gate_relations[out] = (a, ins, b)
    for i in range(46):
        print(print_gate_connections(gate_relations, f"z{i:02}"))

from collections import defaultdict

def find_swap_gates(input:str)->str:
    start_vals, wire_operations = parse_input(input)
    expected_z = expected_sum(start_vals)[::-1]

    # I needed some hint on this one
    # https://www.reddit.com/r/adventofcode/comments/1hla5ql/2024_day_24_part_2_a_guide_on_the_idea_behind_the/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1
    '''
    ok so the idea is that the values from z are a ripple carry bit adder.
    I looked at some solutions and found that:
    1. An XOR must lead to a z value or when the input is a xy lead to an AND or XOR but not an OR
    2. Any AND can only lead to one OR
    3. An OR must lead to one AND and one XOR
    '''

    # output operations of a node
    op_used_as = defaultdict(list)
    for in1, in2, op, out in wire_operations:
        op_used_as[in1].append(op)
        op_used_as[in2].append(op)
    print(op_used_as)
    wrong_ops = []
    for i in range(len(wire_operations)):
        in1, in2, op, out = wire_operations[i]

        # manualy checked out of x00 to be true and z45 has no output to be chaged
        if out == 'z45' or in1 == 'x00' or in2 == 'x00':continue

        if op == 'XOR':
            # XOR from starting values must be used as exactly one AND and one XOR
            if in1[0] in 'xy': 
                if out != 'z00' and sorted(op_used_as[out]) != ['AND', 'XOR']:
                    wrong_ops.append(wire_operations[i])
            # or XOR must lead to a z value
            else: 
                if out[0] != 'z': 
                    wrong_ops.append(wire_operations[i])

        # OR can only lead to one AND and one XOR
        if op == 'OR' and sorted(op_used_as[out]) != ['AND', 'XOR']:
            wrong_ops.append(wire_operations[i])

        # AND can oly lead to one single OR 
        if op == 'AND' and op_used_as[out] != ['OR']:
            wrong_ops.append(wire_operations[i])
    
    to_swap = set()
    for _,_,_, v_out in wrong_ops:
        to_swap.add(v_out)
    return ','.join(sorted(to_swap))
    
print(f'Answer for Part 2: {find_swap_gates(input)}')