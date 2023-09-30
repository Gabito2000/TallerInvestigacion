import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import itertools
import os
import time
import sys

TutteOrder = {}

def convert_to_file_name(file_name):
    return file_name.replace(' ', '').replace('**', '^').replace('*', '')

def create_required_directories(n, m):
    if not os.path.exists('resultados'):
        os.makedirs('resultados')
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)):
        os.makedirs('resultados/'+str(n) + '_' + str(m))
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)+'/graph'):
        os.makedirs('resultados/'+str(n) + '_' + str(m)+'/graph')
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)+'/graph_image'):
        os.makedirs('resultados/'+str(n) + '_' + str(m)+'/graph_image')

def get_maximal_node_in_graph(graph):
    # for each node if do not have out edges then it is maximal
    for node in graph.nodes:
        if len(graph.edges(node)) == 0:
            return node
    return -1

def load_graphs(n, m):
    graphs = []
    for i in range(len(os.listdir('resultados/'+str(n) + '_' + str(m)+'/graph'))):
        graphs.append(nx.read_gexf('resultados/'+str(n) + '_' + str(m)+'/graph/graph_' + str(i) + '.gexf'))
    return graphs

def save_graphs(graphs, n, m):
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
        # transform the graph into a matrix
        matrix = nx.adjacency_matrix(G).todense()
        if graphLookOutTable.get(matrix_to_string(matrix)) is not None:
            continue
        graphs_output.append(G)

        # generate all possible permutations of the matrix
        index = list(itertools.permutations(range(n)))
        for i in range(len(index)):
            matrix = nx.adjacency_matrix(G, nodelist=index[i]).todense()
            if graphLookOutTable.get(matrix_to_string(matrix)) is not None:
                continue
            graphLookOutTable[matrix_to_string(matrix)] = G

    save_graphs(graphs_output, n, m)

    return graphs_output

def tutte_polynomial(graphs):
    timer = time.time()
    tutte_polynomials = []
    for i in range(len(graphs)):
        if i % 10 == 0:
            print (i, "of", len(graphs), str(100*i/len(graphs))+"%", " time:" +str(time.time() - timer))
        tutte_polynomials.append([graphs[i], nx.tutte_polynomial(graphs[i]).expand()])
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

def generate_diagrama_de_hasse(n, m):
    timer = time.time()
    print ("Generating diagrama de hasse for n = " + str(n) + " and m = " + str(m))
    graphs = get_graphs(n, m)
    print ("Done generating graphs for n = " + str(n) + " and m = " + str(m), len(graphs))
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

    # asin the tutte_polynomials to the nodes
    for i in range(len(tutte_polynomials)):
        directed_graph.nodes[i]['tutte_polynomial'] = tutte_polynomials[i]

    # check if the graph has a maximum
    max_node= get_maximal_node_in_graph(directed_graph)
    if max_node != -1:
        max_node = tutte_polynomials[max_node]
    else:
        max_node = "NO MAXIMUM NODE EXISTS"
    print("the max node is:",max_node, convert_to_file_name(str(max_node)))

    # save the maximum node
    with open('resultados/'+str(n) + '_' + str(m)+'/maximal_node_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(max_node)+ " with the filename "+ convert_to_file_name(str(max_node)))

    # save tutte_polynomial_map, directed_graph, and tutte_polynomials to a file, and the graph to a png
    nx.draw(directed_graph, with_labels=True)
    plt.savefig('resultados/'+str(n) + '_' + str(m)+'/directed_graph_Hasse' + str(n) + '_' + str(m) + '.png')
    plt.clf()
    plt.close()

    # save the graph asociated with the tutte polynomial
    for key, value in tutte_polynomial_map.items():
        for i in range(len(value)):
            nx.draw(value[i], with_labels=True)
            plt.savefig('resultados/'+str(n) + '_' + str(m)+'/graph_image/' + convert_to_file_name(str(key))+ '_' + str(i) + '.png')
            plt.clf()
            plt.close()

    # save it all as a string
    with open('resultados/'+str(n) + '_' + str(m)+'/tutte_polynomial_map_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        for key, value in tutte_polynomial_map.items():
            fp.write(str(key) + ' : ')
            for i in range(len(value)):
                fp.write(str(value[i].edges))
            fp.write('\n')
    with open('resultados/'+str(n) + '_' + str(m)+'/directed_graph_Hasse' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(directed_graph.edges))
    with open('resultados/'+str(n) + '_' + str(m)+'/tutte_polynomials_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(tutte_polynomials))

    print ("Done generating diagrama de hasse for n = " + str(n) + " and m = " + str(m), len(graphs), " time:" +str(time.time() - timer))

def main():
    array_entada = []
    if len(sys.argv) < 3:
        print("Usage: python index.py n m for more specific execution")
        for i in range(5, 8):
            for j in range(i, i+5):
                array_entada.append([i, j])
    else:
        if len(sys.argv) % 2 != 1:
            print("error, odd number of entries read the readme file for more information")
            exit()
        for i in range(1, len(sys.argv), 2):
            if int(sys.argv[i]) < 0 or int(sys.argv[i+1]) < 0:
                print("read the readme file for more information")
                exit()
            array_entada.append([int(sys.argv[i]), int(sys.argv[i+1])])

    for i in range(len(array_entada)):
        create_required_directories(array_entada[i][0], array_entada[i][1])
        generate_diagrama_de_hasse(array_entada[i][0], array_entada[i][1])

main()