# ------------------------------------------------------------
# - Advent of code header
# 
# - Day 23
# - 2024 
# 
# ------------------------------------------------------------

WD = '/home/eudaemon/Workspace/Programming/Python/Projects/Advent_of_code/2024/data/'

with open(WD + 'data_D23.txt', 'r') as f:
    input = f.read().splitlines()

test = '''kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn'''.splitlines()

# Solving Part 1
# ------------------------------------------------------------
from collections import defaultdict
def _find_3_sets(input:list[str],n=3)->list[tuple]:     
    three_sets = set()
    computers = [i.split('-') for i in input]
    while computers:
        c1, c2 = computers.pop()
        pos_b = defaultdict()
        pos_b[c1] = []
        pos_b[c2] = []

        for a1, a2 in computers:
            if c1 == a1: 
                if a2 in pos_b[c2] and 't' in ''.join([c2[0],a1[0],a2[0]]): three_sets.add((c2, a1, a2))
                else: pos_b[c1].append(a2)
            elif c1 == a2: 
                if a1 in pos_b[c2] and 't' in ''.join([c2[0],a1[0],a2[0]]): three_sets.add((c2, a1, a2))
                else: pos_b[c1].append(a1)
            elif c2 == a1: 
                if a2 in pos_b[c1] and 't' in ''.join([c1[0],a1[0],a2[0]]): three_sets.add(tuple(sorted([c1, a1, a2])))
                else: pos_b[c2].append(a2)
            elif c2 == a2: 
                if a1 in pos_b[c1] and 't' in ''.join([c1[0],a1[0],a2[0]]): three_sets.add(tuple(sorted([c1, a1, a2])))
                else: pos_b[c2].append(a1)

    return len(three_sets)

def find_3_sets(input:list[str],n=3)->list[tuple]:     
    three_sets = set()
    computers = [i.split('-') for i in input]
    while computers:
        c1, c2 = computers.pop()
        pos_b = defaultdict()
        pos_b[c1] = []
        pos_b[c2] = []
        _mapc = [c1, c2]
        for a1, a2 in computers:
            _mapa = [a1, a2]
            for c in range(2):
                for a in range(2):
                    _c1, _c2 = _mapc[c%2], _mapc[(c+1)%2]
                    _a1, _a2 = _mapa[a%2], _mapa[(a+1)%2]

                    if _c1 == _a1: 
                        if _a2 in pos_b[_c2] and 't' in ''.join([_c2[0],_a1[0],_a2[0]]): 
                            three_sets.add((_c2, _a1, _a2))
                        else: pos_b[_c1].append(_a2)
    return len(three_sets)

#print(f'Answer for Part 1: {find_3_sets(input)}')


# Solving Part 2
# ------------------------------------------------------------

# is too slow!
def node_hmap(input:list[str])->dict[str,list[str]]:
    hmap = defaultdict()
    computers = [i.split('-') for i in input]
    for c1, c2 in computers:
        if c1 in hmap.keys(): hmap[c1].append(c2)
        else: hmap[c1] = [c2]
        if c2 in hmap.keys(): hmap[c2].append(c1)
        else: hmap[c2] = [c1]
    for key, value in hmap.items():
        hmap[key] = set(value)
    return hmap
def find_lagest_set(input:list[str])->str:

    def in_cluster(clusters: list[list[str]], node: str)->int:
        indexes = []
        for i in range(len(clusters)):
            if node in clusters[i]: indexes.append(i)
        return indexes
    
    def is_new_node(cluster:list[str], node:str):
        for bnode in cluster:
            if not node in nodes_map[bnode]: return False
        return True
    
    clusters = []
    nodes_map = node_hmap(input)
    nodes = list(nodes_map.keys())

    while nodes:
        print(len(nodes))
        node = nodes.pop()
        # ist this node already part of any custer?
        if in_cluster(clusters, node): continue
        # if not then add node to cluster
        new = True
        connections = nodes_map[node]
        for cnode in connections:
            pos = in_cluster(clusters, cnode)

            if not pos: continue
            new = False
            # case 2 node is part of any existing cluster
            for i in pos:
                if is_new_node(clusters[i], node):
                    clust = clusters[i]
                    clust.append(node)
                    clusters[i] = clust
                else: clusters.append([node, cnode])
        
        if new: clusters.append([node])

    #return [''.join(sorted(i)) for i in clusters]
    clenght = [len(i) for i in clusters]
    return ','.join(sorted(clusters[clenght.index(max(clenght))]))

# second try
# this was just a nice idea and it worked for the simple case, but 
# in the larger example there are cases left unconsidered.
def get_node_sets(input:list[str])->list[set[str]]:
    def remove_duplicates(array):
        copy = []
        for el in array:
            if el in copy: continue
            else: copy.append(el)
        return copy
    node_sets = []
    hmap = defaultdict()
    computers = [i.split('-') for i in input]
    for c1, c2 in computers:
        if c1 in hmap.keys(): hmap[c1].append(c2)
        else: hmap[c1] = [c2]
        if c2 in hmap.keys(): hmap[c2].append(c1)
        else: hmap[c2] = [c1]
    for key, value in hmap.items():
        value.append(key)
        node_sets.append(sorted(value))

    return remove_duplicates(node_sets)

def extract_lagest_set(input:list[str])->str:
    node_sets = get_node_sets(input)
    print(node_sets)
    clusters = [()]

    for i in range(len(node_sets)):
        cluster = []
        for j in range(len(node_sets)):
            if i == j: continue
            c = set.intersection(set(node_sets[i]), set(node_sets[j]))
            if c: cluster.append(c)
        lk = max([len(k) for k in cluster])
        if len(clusters[0]) < lk:
            clusters = [c for c in cluster if len(c) == lk]
    
    return ','.join(sorted(clusters[0]))
    #return ','.join(list(set(clusters))[0])

# it is a neat little algorythm
# and i hope i have the time to practise
# on this algorthm in the future
 
def bron_kerbosch(current_clique, potential_c, already_seen, graph, cliques)->None:
    if not potential_c and not already_seen:
        cliques.append(current_clique)
        return None

    while potential_c:
        v = potential_c.pop()
        neighbours = set(graph[v])
        bron_kerbosch(
            current_clique.union({v}),
            potential_c.intersection(neighbours),
            already_seen.intersection(neighbours),
            graph, cliques
        )
        already_seen.add(v)

def max_clique(input:list[str])->str:
    graph = node_hmap(input)
    all_cliques = []
    bron_kerbosch(set(), set(graph.keys()), set(), graph, all_cliques)
    len_key = [len(i) for i in all_cliques]
    return ','.join(sorted(all_cliques[len_key.index(max(len_key))]))

print(f'Answer for Part 2: {max_clique(input)}')