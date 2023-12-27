import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import os
import time
import subprocess
import sys
#from tutte import tutte_poly tutte is on tutte_bhkk-master/tutte.py
from tutte_algorithm.tutte import tutte_poly

x, y = sp.symbols('x y')


def convert_to_file_name(file_name):
    return file_name.replace(' ', '').replace('**', '^').replace('*', '')

def create_required_directories(n, m):
    if not os.path.exists('resultados'):
        os.makedirs('resultados')
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)):
        os.makedirs('resultados/'+str(n) + '_' + str(m))
    if not os.path.exists('resultados/'+str(n) + '_' + str(m)+'/graph_image'):
        os.makedirs('resultados/'+str(n) + '_' + str(m)+'/graph_image')


def get_maximal_node_in_graph(graph):
    #for each node if do nt have out edges then it is maximal
    return_node = []
    for node in graph.nodes:
        if len(graph.edges(node)) == 0:
            return_node.append(node)

    return return_node

def matrix_to_string(matrix):
    return "".join(np.concatenate(matrix).astype(str))

def get_graph(n, m):
    '''
    only bipartite graphs can be maximal

    '''
    command = 'nauty2_8_6/geng -c ' + str(n) + ' ' + str(m)
    graphs = []
    try:
        # Execute the command and wait for it to finish
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            # Output is a list of graph6 rows
            output = stdout.decode('utf-8').split('\n')
            # Remove the last element of the list
            output.pop()
            # Convert the graph6 to a networkx graph
            for i in range(len(output)):
                graph = nx.from_graph6_bytes(output[i].encode('utf-8'))
                graphs.append(graph)
        else:
            print("Error: The command returned a non-zero exit code.")
            print("stderr:", stderr.decode('utf-8'))

    except Exception as e:
        print("Error:", e)

    # print ("Done generating graphs for n = " + str(n) + " and m = " + str(m), len(graphs))
    return graphs

def get_graphs(n, m, print_status = True):
    command = 'nauty2_8_6/geng -c ' + str(n) + ' ' + str(m)
    graphs = []
    try:
        # Execute the command and wait for it to finish
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            # Output is a list of graph6 rows
            output = stdout.decode('utf-8').split('\n')
            # Remove the last element of the list
            output.pop()
            # Convert the graph6 to a networkx graph
            for i in range(len(output)):
                graph = nx.from_graph6_bytes(output[i].encode('utf-8'))
                graphs.append(graph)
        else:
            print("Error: The command returned a non-zero exit code.")
            print("stderr:", stderr.decode('utf-8'))

    except Exception as e:
        print("Error:", e)
    if print_status:
        print ("Done generating graphs for n = " + str(n) + " and m = " + str(m), len(graphs))
    return graphs

def tutte_polynomial_algorithm(graphs):
    timer = time.time()
    tutte_polynomials = []
    for i in range(len(graphs)):
        # if i % 10 == 0:
            # print (i, "of", len(graphs), str(100*i/len(graphs))+"%", " time:" +str(time.time() - timer))

        lol_tuttepoly = tutte_poly(graphs[i])
        sympy_tuttepoly = sp.Poly(lol_tuttepoly, x, y)
        tutte_polynomials.append([graphs[i], sympy_tuttepoly])
    return tutte_polynomials

TutteResult = {}

def is_h_greater_than_g(H, G):
    R = 0
    if  TutteResult.get(str(H) + str(G)) is not None:
        R = TutteResult[str(H) + str(G)]
    elif TutteResult.get(str(G) + str(H)) is not None:
        R = TutteResult[str(G) + str(H)]
        for r_key, r_value in R.items():
            if r_value > 0:
                return 0
        return 1
    else:
        R = (H - G)/ sp.Poly(x+y-(x*y))
        R = sp.simplify(R)
        R = sp.expand(R)
        R = R.as_coefficients_dict()
        TutteResult[str(H) + str(G)] = R

    for r_key, r_value in R.items():
        if r_value < 0:
            return 0
    
    return 1

def tutte_polynomial_map_generate(n, m, tutte_polynomials, save_graphs):
    # print("creating a map of tutte polynomials to their graphs")
    tutte_polynomial_map = {}
    for i in range(len(tutte_polynomials)):
        if tutte_polynomial_map.get(tutte_polynomials[i][1]) is None:
            tutte_polynomial_map[tutte_polynomials[i][1]] = []
        tutte_polynomial_map[tutte_polynomials[i][1]].append(tutte_polynomials[i][0])
    if save_graphs:
        # print("saving the graph asociated with the tutte polynomial")
        with open('resultados/'+str(n) + '_' + str(m)+'/graph_image/map_graph_tuttepol ' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
            for key, value, c in zip(tutte_polynomial_map.keys(), tutte_polynomial_map.values(), range(len(tutte_polynomial_map))):
                for i in range(len(value)):
                    fp.write(str(c) + '_' + str(i) + ' : ' + convert_to_file_name(str(key)) + ' : ' + str(value[i].edges)+ '\n')
                    nx.draw(value[i], with_labels=True)
                    plt.savefig('resultados/'+str(n) + '_' + str(m)+'/graph_image/' + str(c)+ '_' + str(i) + '.png')
                    plt.clf()
                    plt.close()
    return tutte_polynomial_map

def get_tutte_polynomials(n, m, graphs, save_graphs, print_status = True):
    tutte_polynomials = tutte_polynomial_algorithm(graphs)
    if print_status:
        print ("Done generating tutte polynomials for n = " + str(n) + " and m = " + str(m))
    # create a map of tutte polynomials to their graphs
    tutte_polynomial_map = tutte_polynomial_map_generate(n, m, tutte_polynomials, save_graphs)
    tutte_polynomials = list(tutte_polynomial_map.keys())

    with open('resultados/'+str(n) + '_' + str(m)+'/tutte_polynomials_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(tutte_polynomials))
    # save the graph asociated with the tutte polynomial

    # save it all as a string
    with open('resultados/'+str(n) + '_' + str(m)+'/tutte_polynomial_map_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        for key, value in tutte_polynomial_map.items():
            fp.write(str(key) + ' : ')
            for i in range(len(value)):
                fp.write(str(value[i].edges))
            fp.write('\n')
    return tutte_polynomials

def get_tutte_max(tutte_polynomials, n, m, timer):
    max_node = []
    
    #for h in range(len(tutte_polynomials)):}
    h = 0
    initial_length = len(tutte_polynomials)
    while h < len(tutte_polynomials):
        progres = h + initial_length - len(tutte_polynomials)
        # print (progres, "of", initial_length, str(100*progres/initial_length)+"%", " time:" +str(time.time() - timer))
        g = 0
        while g < len(tutte_polynomials):
            if g != h:
                if is_h_greater_than_g(tutte_polynomials[g], tutte_polynomials[h]) == 1:
                    #remove h from the list
                    tutte_polynomials.pop(h)
                    h -= 1
                    break
                if is_h_greater_than_g(tutte_polynomials[h], tutte_polynomials[g]) == 1:
                    #remove g from the list
                    tutte_polynomials.pop(g)
                    g -= 1
                    if h > g:
                        h -= 1

            g += 1
        h += 1
        

    max_node = tutte_polynomials
    if len(max_node) == 1:
        max_node = max_node[0]
        print("the max node is:",max_node, convert_to_file_name(str(max_node)))
    elif len(max_node) > 1:
        print("NO MAX NODE EXISTS, THE MAXIMUMS ARE:",max_node, convert_to_file_name(str(max_node)))
    else:
        print("NO MAX NODE EXISTS")

    with open('resultados/'+str(n) + '_' + str(m)+'/maximal_node_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(max_node)+ " with the filename "+ convert_to_file_name(str(max_node)))

    return max_node

def get_girth_max(n, m, graphs, print_status = True):
    # print("getting the girth max")
    girth_max = 0
    girth_max_graph = []
    for i in range(len(graphs)):
        if nx.is_connected(graphs[i]):
            girth = nx.girth(graphs[i])
            if girth > girth_max:
                girth_max = girth
                girth_max_graph = [graphs[i]]
            elif girth == girth_max:
                girth_max_graph.append(graphs[i])
                
    calculate_tutte_polynomial = tutte_polynomial_algorithm(girth_max_graph)

    calculate_tutte_polynomial = map(lambda x: x[1], calculate_tutte_polynomial)
    calculate_tutte_polynomial = list(calculate_tutte_polynomial)

    if print_status:
        print ("Done generating girth max for n = " + str(n) + " and m = " + str(m))
    with open('resultados/'+str(n) + '_' + str(m)+'/girth_max_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(girth_max) + ':')
        fp.write(str(calculate_tutte_polynomial))

    return calculate_tutte_polynomial

def ejecutar_algoritmo(n,m, getOnlyMax = False, save_graphs = False, print_status = True):
    timer = time.time()
    if print_status:
        if getOnlyMax == False:
            print ("Generating diagrama de hasse for n = " + str(n) + " and m = " + str(m))
        else:
            print ("Generating max node for n = " + str(n) + " and m = " + str(m))

    graphs = get_graphs(n, m, print_status)
    tutte_polynomials = get_tutte_polynomials(n, m, graphs, save_graphs, print_status)

    if getOnlyMax:
        max_tutte_polynomial = get_tutte_max(tutte_polynomials, n, m, timer)
        girth_experiment(n, m, print_status, graphs, max_tutte_polynomial)

    else:
        generate_hasse_diagram(n, m, timer, tutte_polynomials)


    if print_status:
        if getOnlyMax == False:
            print("Done generating diagrama de hasse for n = " + str(n) + " and m = " + str(m), len(graphs), " time:" +str(time.time() - timer))
        else:
            print("Done generating max node for n = " + str(n) + " and m = " + str(m), len(graphs), " time:" +str(time.time() - timer))

def girth_experiment(n, m, print_status, graphs, max_tutte_polynomial):
    max_girth_tutte_polynomial = get_girth_max(n, m, graphs, print_status)
    max_node_with_max_girth = []
    if type(max_tutte_polynomial) is not list:
        max_tutte_polynomial = [max_tutte_polynomial]
        
    if type(max_girth_tutte_polynomial) is not list:
        max_girth_tutte_polynomial = [max_girth_tutte_polynomial]

    for i in range(len(max_girth_tutte_polynomial)):
        for j in range(len(max_tutte_polynomial)):
            if max_girth_tutte_polynomial[i] == max_tutte_polynomial[j]:
                max_node_with_max_girth.append(max_girth_tutte_polynomial[i])
                break
    if len(max_node_with_max_girth) == 0:
        print('THE MAX NODE WITH MAX GIRTH IS NOT IN THE MAX NODES')
    else:
        print("THE MAX NODE WITH MAX GIRTH IS:",max_node_with_max_girth, convert_to_file_name(str(max_node_with_max_girth)))
        
    with open('resultados/'+str(n) + '_' + str(m)+'/maximal_node_with_max_girth_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(max_node_with_max_girth)+ " with the filename "+ convert_to_file_name(str(max_node_with_max_girth)))

def generate_hasse_diagram(n, m, timer, tutte_polynomials):
    directed_graph = nx.DiGraph()
    directed_graph.add_nodes_from(range(len(tutte_polynomials)))

    # print("creating the directed graph")
    for i in range(len(tutte_polynomials)):
        print (i, "of", len(tutte_polynomials), str(100*i/len(tutte_polynomials))+"%", " time:" +str(time.time() - timer))
        for j in range(i, len(tutte_polynomials)):
                if i != j :
                    if is_h_greater_than_g(tutte_polynomials[j], tutte_polynomials[i]) == 1:
                        directed_graph.add_edge(i, j)
                    elif is_h_greater_than_g(tutte_polynomials[i], tutte_polynomials[j]) == 1:
                        directed_graph.add_edge(j, i)

    # print(directed_graph.nodes)
    # print(directed_graph.edges)

    #asign the tutte_polynomials to the nodes
    for i in range(len(tutte_polynomials)):
        directed_graph.nodes[i]['tutte_polynomial'] = tutte_polynomials[i]

    # check if the graph has a maximum
    max_node = get_maximal_node_in_graph(directed_graph)
    if len(max_node) == 1:
        max_node = tutte_polynomials[max_node[0]]
        print("the max node is:",max_node, convert_to_file_name(str(max_node)))
    elif len(max_node) > 1:
        for i in range(len(max_node)):
            max_node[i] = tutte_polynomials[max_node[i]]
        print("NO MAX NODE EXISTS, THE MAXIMUMS ARE:",max_node, convert_to_file_name(str(max_node)))
    else:
        print("NO MAX NODE EXISTS")

    with open('resultados/'+str(n) + '_' + str(m)+'/maximal_node_' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(max_node)+ " with the filename "+ convert_to_file_name(str(max_node)))

    directed_graph = nx.relabel_nodes(directed_graph, lambda x: convert_to_file_name(str(directed_graph.nodes[x]['tutte_polynomial'])))

    # save tutte_polynomial_map, directed_graph, and tutte_polynomials to a file, and the graph to a png
    nx.draw(directed_graph, with_labels=True)
    plt.savefig('resultados/'+str(n) + '_' + str(m)+'/graph_image/' + 'directed_graph_Hasse_' + str(n) + '_' + str(m) + '.png')
    plt.clf()
    plt.close()
    with open('resultados/'+str(n) + '_' + str(m)+'/directed_graph_Hasse' + str(n) + '_' + str(m) + '.txt', 'w') as fp:
        fp.write(str(directed_graph.edges))

    return directed_graph

def main():
    array_entada = []
    if len(sys.argv) < 3:
        print("Usage: python index.py n m for more especific execution")
        # array_entada.append([6,7])
        # array_entada.append([6,9])
        # array_entada.append([7,11])
        # array_entada.append([8,16])
        
        for i in range(6, 9):
            for j in range(i, i*2):
                array_entada.append([i,j])
    else:
        if len(sys.argv) % 2 != 1:
            print("error, odd number of enties read the readme file for more information")
            exit()
        for i in range(1, len(sys.argv), 2):
            if int(sys.argv[i]) < 0 or int(sys.argv[i+1]) < 0:
                print("read the readme file for more information")
                exit()
            array_entada.append([int(sys.argv[i]), int(sys.argv[i+1])])

    for i in range(len(array_entada)):
        create_required_directories(array_entada[i][0], array_entada[i][1])
        ejecutar_algoritmo(array_entada[i][0], array_entada[i][1], True, True, False)

if __name__ == "__main__":
    main()