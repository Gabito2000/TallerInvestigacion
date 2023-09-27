'''
The objetive of this project is to create a program that
1. gets all the graphs with n vertices and m edges
2. calculates the tutte polynomial of each graph
3. adds the tutte polynomial of each graph to a list
4. use the folowing algorithm to generate a directed graph
'''

# Path: index.py
# Importing libraries
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import itertools
import numpy as np
import os
import time
# Path: index.py
# Defining functions
TutteOrder = {}

def get_maximal_node_in_graph(graph):
    #for each node if do nt have out edges then it is maximal
    for node in graph.nodes:
        if len(graph.edges(node)) == 0:
            return node
    
    return -1

def load_graphs(n, m):
    graphs = []
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)):
        return graphs
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)+'/graph'):
        return graphs
    for i in range(len(os.listdir('resultados/'+str(n) + '_' + str(m)+'/graph'))):
        graphs.append(nx.read_gexf('resultados/'+str(n) + '_' + str(m)+'/graph/graph_' + str(i) + '.gexf'))
    return graphs

def save_graphs(graphs, n, m):
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)):
        os.makedirs('resultados/'+str(n) + '_' + str(m))
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)+'/graph'):
        os.makedirs('resultados/'+str(n) + '_' + str(m)+'/graph')
    
    for i in range(len(graphs)):
        nx.write_gexf(graphs[i], 'resultados/'+str(n) + '_' + str(m)+'/graph/graph_' + str(i) + '.gexf')


def matrix_to_string(matrix):
    return "".join(np.concatenate(matrix).astype(str))
        
def get_graphs(n, m):
    graphs_output = load_graphs(n, m)
    if len(graphs_output) > 0:
        return graphs_output
    
    timer = time.time()
    all_possible_edges = list(itertools.combinations(range(n), 2))
    
    edge_combinations = list(itertools.combinations(all_possible_edges, m))

    graphLookOutTable = dict()

    print_c = 0
    for edges in edge_combinations:
        if print_c % 10000 == 0:
            print (print_c, "of", len(edge_combinations), str(100*print_c/len(edge_combinations))+"%", " time:" +str(time.time() - timer))
        print_c = print_c + 1
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(edges)
        if not nx.is_connected(G):
            continue
        #transform the graph into a matrix
        matrix = nx.adjacency_matrix(G).todense()
        if graphLookOutTable.get(matrix_to_string(matrix)) is not None:
            continue
        graphs_output.append(G)

        #generate all possible permutations of the matrix
        index = list(itertools.permutations(range(n)))
        for i in range(len(index)):
            matrix = nx.adjacency_matrix(G, nodelist=index[i]).todense()
            if graphLookOutTable.get(matrix_to_string(matrix)) is not None:
                continue
            graphLookOutTable[matrix_to_string(matrix)] = G
            

    #plot the graphs
    for i in range(len(graphs_output)):
        if not os.path.exists("resultados/"+str(n) + '_' + str(m)):
            os.makedirs("resultados/"+str(n) + '_' + str(m))
        if not os.path.exists("resultados/"+str(n) + '_' + str(m)+"/graph_image"):
            os.makedirs("resultados/"+str(n) + '_' + str(m)+"/graph_image")

        nx.draw(graphs_output[i], with_labels=True)
        plt.savefig("resultados/"+str(n) + '_' + str(m) + "/graph_image/graph_" + str(i) + ".png")
        plt.clf()



    print ("Done generating graphs for n = " + str(n) + " and m = " + str(m), len(graphs_output))

    save_graphs(graphs_output, n, m)

    return graphs_output

def tutte_polynomial(graphs):
    tutte_polynomials = []
    for i in range(len(graphs)):
        tutte_polynomials.append([graphs, nx.tutte_polynomial(graphs[i]).expand()])
    return tutte_polynomials


def is_h_greater_than_g(G, H):
    if TutteOrder.get((G, H)) is not None:
        return TutteOrder.get((G, H))

    R = (H - G)/ (sp.symbols('x') + sp.symbols('y') - sp.symbols('x') * sp.symbols('y'))
    R = sp.simplify(R)
    R_dict = R.as_coefficients_dict()
    for r_key, r_value in R_dict.items():
        if r_value < 0:
            return 0
        
    TutteOrder[(G, H)] = 1
    return 1

def generate_diagrama_de_hasse(n,m):
    print ("Generating diagrama de hasse for n = " + str(n) + " and m = " + str(m))
    graphs = get_graphs(n, m)
    print ("Done generating graphs for n = " + str(n) + " and m = " + str(m))
    tutte_polynomials = tutte_polynomial(graphs)
    print ("Done generating tutte polynomials for n = " + str(n) + " and m = " + str(m))
    

    # create a map of tutte polynomials to their graphs
    tutte_polynomial_map = {}
    for i in range(len(tutte_polynomials)):
        if tutte_polynomial_map.get(tutte_polynomials[i][1]) is None:
            tutte_polynomial_map[tutte_polynomials[i][1]] = []
        tutte_polynomial_map[tutte_polynomials[i][1]].append(tutte_polynomials[i][0])

    tutte_polynomials = list(tutte_polynomial_map.keys())

    directed_graph = nx.DiGraph()
    directed_graph.add_nodes_from(range(len(tutte_polynomials)))

    for i in range(len(tutte_polynomials)):
        for j in range(len(tutte_polynomials)):
            if i != j:
                if is_h_greater_than_g(tutte_polynomials[i], tutte_polynomials[j]):
                    directed_graph.add_edge(i, j)

    print(directed_graph.nodes)         
    print(directed_graph.edges)

    # check if the graph has a maximum
    max_node= get_maximal_node_in_graph(directed_graph)
    if max_node != -1:
        max_node = tutte_polynomials[max_node]
    else:
        max_node = "NO MAXIMUM NODE EXISTS"
    print("the max node is:",max_node)

    # save the maximum node
    with open('resultados/'+str(n) + '_' + str(m)+'/maximal_node_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(max_node))

    # save tutte_polynomial_map, directed_graph, and tutte_polynomials to a file, and the graph to a png
    # crete a folder
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)):
        os.makedirs('resultados/'+str(n) + '_' + str(m))
    plt.savefig('resultados/'+str(n) + '_' + str(m)+'/directed_graph_Hasse' + str(n) + '_' + str(m) + '.png')
    plt.clf()
    plt.close()
    # save it all as a string
    with open('resultados/'+str(n) + '_' + str(m)+'/tutte_polynomial_map_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        for key, value in tutte_polynomial_map.items():
            fp.write(str(key) + ' : ')
            for i in range(len(value)):
                for j in range(len(value[i])):
                    fp.write(str(value[i][j].edges))
                    fp.write(' ')
            fp.write('\n')
    with open('resultados/'+str(n) + '_' + str(m)+'/directed_graph_Hasse' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(directed_graph.edges))
    with open('resultados/'+str(n) + '_' + str(m)+'/tutte_polynomials_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(tutte_polynomials))



def main():
    for n in range(5, 10):
        for m in range(n, 2*n):
            generate_diagrama_de_hasse(n,m)
main()