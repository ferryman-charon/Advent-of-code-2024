# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 5
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D05.txt', 'r') as f:
   input = f.read()

test = '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47'''

# Solving Part 1
# ------------------------------------------------------------
def extract_rules(text:str)->tuple[dict,list]:
    rule_dict = {}
    rules, data = text.split('\n\n')
    data = [k.split(',') for k in data.split()]
    for first,second in [k.split('|') for k in rules.split()]:
        if first not in rule_dict.keys():
            rule_dict[first] = [second]
        else:
            vals = rule_dict[first]
            vals.append(second)
            rule_dict[first] = vals

    return rule_dict, data

def valid_seq(rules:dict, seq:list[str])->bool:
    leading = [seq[0]]
    for ind in range(1, len(seq)):
        if seq[ind] in rules.keys():
            nums = rules[seq[ind]]
            for obj in leading:
                if obj in nums:
                    return False
        leading.append(seq[ind])
    return True

def check_data(text:str)->int:
    result = 0
    rules, data = extract_rules(text=text)
    for line in data:
        if valid_seq(rules, line):
            result += int(line[len(line)//2])
    return result

print(f'Answer for Part 1: {check_data(input)}')


# Solving Part 2
# ------------------------------------------------------------

def sort_seq(rules:dict, seq:list[str])->list[str]:
    if len(seq) <= 1:
        return seq
    nseq = seq.copy()
    l = len(nseq)

    i = 0
    while True:
        a = nseq[i]
        newlist = []
        for obj in nseq[i:]:
            if obj in rules.keys():
                if a in rules[obj]:
                    newlist.append(obj)

        if not newlist:
            break

        for item in newlist:
            nseq.pop(nseq.index(item))
        nseq = newlist + nseq

    return [a] + sort_seq(rules, nseq[1:])


def correct_data(text:str)->int:
    result = 0
    rules, data = extract_rules(text=text)
    for line in data:
        if not valid_seq(rules, line):
            sline = sort_seq(rules, line)
            result += int(sline[len(line)//2])
    return result

print(f'Answer for Part 2: {correct_data(input)}')