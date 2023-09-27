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
# Path: index.py
# Defining functions
TutteOrder = {}

def matrix_to_string(matrix):
    return "".join(np.concatenate(matrix).astype(str))
        
def get_graphs(n, m):
    graphs_output = []

    all_possible_edges = list(itertools.combinations(range(n), 2))
    
    edge_combinations = list(itertools.combinations(all_possible_edges, m))

    graphLookOutTable = dict()

    for edges in edge_combinations:
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
        if not os.path.exists("resultados/"+str(n) + '_' + str(m)+"/graph"):
            os.makedirs("resultados/"+str(n) + '_' + str(m)+"/graph")

        nx.draw(graphs_output[i], with_labels=True)
        plt.savefig("resultados/"+str(n) + '_' + str(m) + "/graph/graph_" + str(i) + ".png")
        plt.clf()



    print ("Done generating graphs for n = " + str(n) + " and m = " + str(m), len(graphs_output))
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
    R = R.expand()
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

    # save tutte_polynomial_map, directed_graph, and tutte_polynomials to a file, and the graph to a png
    # crete a folder
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)):
        os.makedirs('resultados/'+str(n) + '_' + str(m))
    np.save('resultados/'+str(n) + '_' + str(m)+'/tutte_polynomial_map_' + str(n) + '_' + str(m), tutte_polynomial_map)
    np.save('resultados/'+str(n) + '_' + str(m)+'/directed_graph_' + str(n) + '_' + str(m), directed_graph)
    np.save('resultados/'+str(n) + '_' + str(m)+'/tutte_polynomials_' + str(n) + '_' + str(m), tutte_polynomials)
    nx.draw(directed_graph, with_labels=True)
    plt.savefig('resultados/'+str(n) + '_' + str(m)+'/directed_graph_' + str(n) + '_' + str(m) + '.png')
    plt.clf()
    plt.close()
    # save it all as a string
    with open('resultados/'+str(n) + '_' + str(m)+'/tutte_polynomial_map_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        for key, value in tutte_polynomial_map.items():
            fp.write(str(key) + ' : ' + str(value) + '\n')
    with open('resultados/'+str(n) + '_' + str(m)+'/directed_graph_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(directed_graph))
    with open('resultados/'+str(n) + '_' + str(m)+'/tutte_polynomials_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(tutte_polynomials))
    # save it all as a json



def main():
    generate_diagrama_de_hasse(6, 8)


main()