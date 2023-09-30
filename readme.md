# Prototipo en python del proyecto de investigación.

En el siguiente prototipo se implementa el algoritmo no optimizado en python para la generación de diagramas de hasse.

Al ejecutarlo se creará una carpeta 'resultados' en la cual se guardara el resultado de la ejecución.

Esta carpeta tendrá los siguientes archivos y carpetas

## Carpetas y archivos

Graph/: se guardarán todos los grafos generados para su posterior utilización.

Graph-image/: se guardarán todas las imágenes de todos los grafos.

directed_graph_Hasse$n$_$m$.png: diagrama de hasse

directed_graph_Hasse$n$_$m$.txt: diagrama de hasse pero solo los edges

maximal_node_$n$_$m$: el polinomio de tutte máximo

tutte_polynomial_map_$n$_$m$: un mapeo entre los nodos del diagrama de hasse, los grafos y los polinomios de tutte. La liña n es el nodo n-1 es decir, si el polinomio de tutte está en la liña 10 este será el nodo 9 del diagrama de hasse.

tutte_polynomials_$n$_$m$: todos los polinomios de tutte encontrados.

## cómo ejecutar el programa

**python index.py** ejecutará el programa desde i=5 hasta i=8 vértices y desde i hasta i+5 aristas.

**python index.py n1 m1 n2 m2 n3 m3...** ejecutará el programa para n1 vértices y m1 aristas, n2 vértices y m2 aristas, n3 vértices y m3 aristas, ...

**ejemplo: python index.py 5 5 6 6 7 7** ejecutará el programa para 5 vértices y 5 aristas, 6 vértices y 6 aristas, 7 vértices y 7 aristas.

recordar que el programa puede tardar tiempo en ejecutar, ya que es computacionalmente intensivo y no está optimizado.


## cómo compilar a cython 

**python setup.py build_ext --inplace**

**python main.py**

