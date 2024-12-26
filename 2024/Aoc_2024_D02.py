# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 2
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/loki/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D02.txt', 'r') as f:
   input = f.read().splitlines()

test = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''.splitlines()

# Solving Part 1
# ------------------------------------------------------------
def check_report(report:list[int])->bool:

    slope = report[1] - report[0]
    if slope > 0:
        increasing = True
        decreasing = False
    elif slope < 0:
        increasing = False
        decreasing = True
    else:
        increasing = False
        decreasing = False
    
    for i in range(len(report)-1):
        step = (report[i+1]-report[i])
        if increasing and step > 0 and step <= 3:
            pass
        elif decreasing and step < 0 and step >= -3:
            pass
        else:
            return False
    return True

def control_reports(text:list[str])->int:
    contr_conter = 0
    for report in text:
        report = [int(i) for i in report.split()]
        #print(check_report(report))
        contr_conter += check_report(report)
    return contr_conter


print(f'Answer for Part 1: {control_reports(input)}')


# Solving Part 2
# ------------------------------------------------------------

def check_report(report:list[int])->bool:

    if report[1] - report[0] > 0: increasing = True
    else: increasing = False
    
    for i in range(len(report)-1):
        step = (report[i+1]-report[i])

        if increasing and step > 0 and step <= 3: pass
        elif not increasing and step < 0 and step >= -3: pass
        else: return False

    return True

def problem_dampener(report:list[int])->list[list[int]]:
    combinations = [report]
    
    for number in range(len(report)):
        reduced_rep = []
        for ind in range(len(report)):
            if ind != number:
                reduced_rep.append(report[ind])
        combinations.append(reduced_rep)
    return combinations

def cntr_damped_reports(text:list[str])->int:
    contr_conter = 0
    for report in text:
        reports = problem_dampener([int(i) for i in report.split()])
        if any([check_report(rep) for rep in reports]):
            contr_conter += 1
    return contr_conter

def cntr_damped_rep_v2(text:list[str])->int:
    contr_conter = 0
    for report in text:
        report = [int(i) for i in report.split()]
        for n in range(len(report)):
            newrep = report.copy()
            del(newrep[n])
            if check_report(newrep):
                contr_conter += 1
                break
    return contr_conter

print(f'Answer for Part 2: {cntr_damped_reports(input)}')
print(f'Answer for Part 2: {cntr_damped_rep_v2(input)}')