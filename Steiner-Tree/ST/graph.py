import networkx as nx
import matplotlib.pyplot as plt
import random
from itertools import combinations

def add_random_weights(graph: nx.Graph) -> nx.Graph:
    """
    Agrega pesos aleatorios a las aristas de un grafo.

    Args:
        graph (nx.Graph): El objeto grafo de NetworkX.

    Returns:
        nx.Graph: El grafo con pesos agregados a las aristas.
    """
    for u, v in graph.edges():
        graph[u][v]['weight'] = random.randint(1, 10)
    return graph

def build_custom_graph() -> nx.Graph:
    """
    Permite al usuario construir una gráfica personalizada y asignar pesos.

    Returns:
        nx.Graph: El grafo personalizado con pesos
    """
    G = nx.Graph()
    num_nodes = int(input("Ingresa el número de nodos para tu gráfica personalizada: "))
    G.add_nodes_from(range(num_nodes))

    while True:
        add_edge = input("¿Deseas agregar una arista? (s/n): ").lower()
        if add_edge == 's':
            try:
                u = int(input(f"Ingresa el nodo de origen (0 a {num_nodes - 1}): "))
                v = int(input(f"Ingresa el nodo de destino (0 a {num_nodes - 1}): "))
                if u < 0 or u >= num_nodes or v < 0 or v >= num_nodes:
                    print("Nodos fuera de rango. Inténtalo de nuevo.")
                    continue
                weight_input = input("Ingresa el peso para esta arista (deja en blanco para peso aleatorio): ")
                if weight_input:
                    weight = float(weight_input)
                else:
                    weight = random.randint(1, 10) # Peso aleatorio si no se especifica
                G.add_edge(u, v, weight=weight)
            except ValueError:
                print("Entrada inválida. Asegúrate de ingresar números para los nodos y el peso.")
        else:
            break
    return G

def generate_graph() -> nx.Graph:
    """
    Genera una gráfica de una lista de gráficas predefinidas con pesos en las aristas.

    Returns:
        nx.Graph: Un objeto NetworkX Graph con pesos.
    """
    
    menu = """
    Selecciona un tipo de gráfica:
        1. Gráfica Completa (K_n)
        2. Gráfica Camino (P_n)
        3. Gráfica Estrella (S_n)
        4. Gráfica Bipartita Completa (K_m,n)
        5. Gráfica Personalizada
        
    """
    print(menu)
    
    choice = input("Ingresa el número de la gráfica que deseas generar: ")
    
    if choice == '1':
        n = int(input("Ingresa el número de nodos (n): "))
        G = nx.complete_graph(n)
        G = add_random_weights(G) # Agrega pesos
        return G
    
    elif choice == '2':
        n = int(input("Ingresa el número de nodos (n): "))
        G = nx.path_graph(n)
        G = add_random_weights(G) # Agrega pesos
        return G
    
    elif choice == '3':
        n = int(input("Ingresa el número de hojas (n): "))
        G = nx.star_graph(n)
        G = add_random_weights(G) # Agrega pesos
        return G
    
    elif choice == '4':
        m = int(input("Ingresa el número de nodos en la primera partición (m): "))
        n = int(input("Ingresa el número de nodos en la segunda partición (n): "))
        G = nx.complete_bipartite_graph(m, n)
        G = add_random_weights(G) # Agrega pesos
        return G
    elif choice == '5':
        return build_custom_graph() # build_custom_graph() ya maneja los pesos
    
    else:
        print("Opción no válida.")
        return None


