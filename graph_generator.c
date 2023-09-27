#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>

// Include additional C libraries and headers as needed.

// Define your C function here.
PyObject* get_graphs(PyObject* self, PyObject* args) {
    int n, m;
    if (!PyArg_ParseTuple(args, "ii", &n, &m)) {
        return NULL;
    }

    
    //python code to port
    // Generate graphs.
    // all_possible_edges = list(itertools.combinations(range(n), 2))
    
    // edge_combinations = list(itertools.combinations(all_possible_edges, m))

    // graphLookOutTable = dict()
    // print_c = 0
    // for edges in edge_combinations:
    //     if print_c % 1000 == 0:
    //         print (print_c, "of", len(edge_combinations), str(100*print_c/len(edge_combinations))+"%", " time:" +str(time.time() - timer))
    //     print_c = print_c + 1
    //     G = nx.Graph()
    //     G.add_nodes_from(range(n))
    //     G.add_edges_from(edges)
    //     if not nx.is_connected(G):
    //         continue
    //     #transform the graph into a matrix
    //     matrix = nx.adjacency_matrix(G).todense()
    //     if graphLookOutTable.get(matrix_to_string(matrix)) is not None:
    //         continue
    //     graphs_output.append(G)

    //     #generate all possible permutations of the matrix
    //     index = list(itertools.permutations(range(n)))
    //     for i in range(len(index)):
    //         matrix = nx.adjacency_matrix(G, nodelist=index[i]).todense()
    //         if graphLookOutTable.get(matrix_to_string(matrix)) is not None:
    //             continue
    //         graphLookOutTable[matrix_to_string(matrix)] = G

    //c code

    //generate all possible edges
    int all_possible_edges[n*(n-1)/2][2];
    int edge_combinations[(int)pow(n*(n-1)/2, m)][m][2];
    int graphLookOutTable[(int)pow(n, n)][n][n];
    int print_c = 0;
    int edge_combinations_index = 0;
    int graphLookOutTable_index = 0;
    int all_possible_edges_index = 0;

    //generate all possible edges
    for(int i = 0; i < n; i++){
        for(int j = i+1; j < n; j++){
            all_possible_edges[all_possible_edges_index][0] = i;
            all_possible_edges[all_possible_edges_index][1] = j;
            all_possible_edges_index++;
        }
    }

    //generate all possible edge combinations
    for(int i = 0; i < pow(n*(n-1)/2, m); i++){
        for(int j = 0; j < m; j++){
            edge_combinations[i][j][0] = all_possible_edges[(i/(int)pow(n*(n-1)/2, j))%(n*(n-1)/2)][0];
            edge_combinations[i][j][1] = all_possible_edges[(i/(int)pow(n*(n-1)/2, j))%(n*(n-1)/2)][1];
        }
    }

    //generate all possible graphs
    int G[n][n];
    



    
    
    

    


}

// Define other C functions as needed.

// Define a list of Python methods that will be available from the Python wrapper.
static PyMethodDef module_methods[] = {
    {"get_graphs", get_graphs, METH_VARARGS, "Generate graphs."},
    // Add more methods if needed.
    {NULL, NULL, 0, NULL}
};

// Define the Python module initialization function.
static struct PyModuleDef module_definition = {
    PyModuleDef_HEAD_INIT,
    "graph_generator",
    "Graph Generation Module",
    -1,
    module_methods
};

// Create the Python extension module.
PyMODINIT_FUNC PyInit_graph_generator(void) {
    return PyModule_Create(&module_definition);
}