import subprocess

def getOrder(graph):
    return len(graph)

def testOrder(graph1, graph2):
    print("\nCheck Order:")

    return getOrder(graph1) == getOrder(graph2)

def getSize(graph):
    size = 0

    for v in graph:
        size += len(graph[v])

    return size/2
    
def testSize(graph1, graph2):
    print("\nCheck Size:")

    return getSize(graph1) == getSize(graph2)

def getDegreeSequence(graph):
    degree_sequence = []

    for v1 in graph:
        degree_sequence.append(len(graph[v1]))
    
    return degree_sequence.sort()

def testDegreeSequence(graph1, graph2):
    print("\nCheck Degree Sequence:")

    return getDegreeSequence(graph1) == getDegreeSequence(graph2)

def DFS(k, visited, graph):
    visited[k] = True
    for p in graph[k]:
        if not(visited[p]):
            DFS(p, visited, graph)

def getNumberOfConnectedComponents(graph):
    visited = {}
    component_count = 0

    for k in graph:
        visited[k] = False

    for k in visited:
        if not(visited[k]):
            DFS(k, visited, graph)
            component_count += 1
    
    return component_count

def testNumberOfConnectedComponents(graph1, graph2):
    print("\nNumber of connected components:")

    return getNumberOfConnectedComponents(graph1) == getNumberOfConnectedComponents(graph2)

def compressLabels(labels):
    old_labels = labels.copy()
    for v in old_labels:
        labels[v] = hash(old_labels[v])
    
    return labels

def makeNewLabels(graph, labels):
    old_labels = labels.copy()
    for v1 in graph:
        adj_labels=[]
        for v2 in graph[v1]:
            adj_labels.append(old_labels[v2])
        labels[v1] = (old_labels[v1], tuple(sorted(adj_labels)))

    return compressLabels(labels)

def testWeisfeilerLehmanIsomorphism(graph1, graph2):
    print("\nWeisfeiler Lehman Isomorphism Test:")

    #Initalization
    labels_graph1 = {}
    for v in graph1:
        labels_graph1[v] = 1

    labels_graph2 = {}
    for v in graph2:
        labels_graph2[v] = 1

    count_graph1 = {}
    count_graph2 = {}
    i = 0
    
    while((not(count_graph1==count_graph2) or count_graph1=={} or i<3) and i<len(graph1)):
        i += 1

        labels_graph1 = makeNewLabels(graph1, labels_graph1)
        labels_graph2 = makeNewLabels(graph2, labels_graph2)

        for v in labels_graph1:
            label = labels_graph1[v]
            if label in count_graph1:
                count_graph1[label] += 1
            else:
                count_graph1[label] = 1

        for v in labels_graph2:
            label = labels_graph2[v]
            if label in count_graph2:
                count_graph2[label] += 1
            else:
                count_graph2[label] = 1

    return count_graph1 == count_graph2

    
def heuristicTestIsomorphic(graph1, graph2):

    if testOrder(graph1, graph2):
        print(" Same Order")

    else:
        print(" Not Same Order")
        return False

    if testSize(graph1, graph2):
        print(" Same Size")

    else:
        print(" Not Same Size")
        return False
    
    if testDegreeSequence(graph1, graph2):
        print(" Same Degree Sequence")
    
    else:
        print(" Not Same Degree Sequence")
        return False
    
    if testNumberOfConnectedComponents(graph1, graph2):
        print(" Same Component Count")
    
    else:
        print(" Not Same Component Count")
        return False

    if testWeisfeilerLehmanIsomorphism(graph1, graph2):
        print(" Passed Weisfeiler Lehman Isomorphism Test")
    
    else:
        print(" Not Passed Weisfeiler Lehman Isomorphism Test")
        return False
    
    return True

def glasgowTest(image_path):
    print("\ncompare Expected and Extracted: \n")
    result = subprocess.run(["glasgow-subgraph-solver/build/glasgow_subgraph_solver --format csv --induced graph.csv "+ image_path +".csv"], shell=True, text=True, stdout = subprocess.PIPE)

    lines = result.stdout.splitlines()
    for line in lines:
        if line.startswith("status"):
            print(line)

    print("\ncompare Extracted and Expected: \n")
    result = subprocess.run(["glasgow-subgraph-solver/build/glasgow_subgraph_solver --format csv --induced "+ image_path +".csv graph.csv"], shell=True, text=True, stdout = subprocess.PIPE)

    lines = result.stdout.splitlines()
    for line in lines:
        if line.startswith("status"):
            print(line)