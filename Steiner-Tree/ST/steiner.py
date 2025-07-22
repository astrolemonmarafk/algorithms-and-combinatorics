# Steiner.py
import networkx as nx
import matplotlib.pyplot as plt
import itertools


def kmb(graph_nx_orig: nx.Graph, terminals_heur):
    """
    Resuelve el Problema del Árbol de Steiner aplicando el algoritmo de kmb

    Args:
        graph_nx_orig (nx.Graph): El grafo de entrada como objeto NetworkX.
        terminals_heur (list): La lista de nodos terminales.

    Returns:
        tuple: Una tupla (costo_total, aristas_seleccionadas).
               Retorna (None, []) si no se encuentra solución.
    """


    # Manejo de casos triviales: si hay menos de 2 terminales, el costo es 0.
    if not terminals_heur or len(terminals_heur) < 2:
        return 0, []

    # Asegurarse de que los terminales proporcionados existen en el grafo.
    valid_terminals = [t for t in terminals_heur if graph_nx_orig.has_node(t)]
    if len(valid_terminals) < 2:
        return 0, []
    
    terminals_to_use = valid_terminals

    # --- PASO 1: CONSTRUIR EL GRAFO MÉTRICO DE TERMINALES (H) ---
    # H contendrá solo los terminales. El peso de una arista (t1, t2) en H
    # será la distancia del camino más corto entre t1 y t2 en el grafo original.
    H = nx.Graph()
    # Diccionario para guardar el camino real en G que corresponde a cada arista de H.
    paths_in_G = {}
    for i in range(len(terminals_to_use)):
        for j in range(i + 1, len(terminals_to_use)):
            t1, t2 = terminals_to_use[i], terminals_to_use[j]
            try:
                # Calcular la distancia y el camino más corto en el grafo original G.
                length = nx.shortest_path_length(graph_nx_orig, source=t1, target=t2, weight='weight')
                path = nx.shortest_path(graph_nx_orig, source=t1, target=t2, weight='weight')
                
                # Añadir la arista "virtual" al grafo H.
                H.add_edge(t1, t2, weight=length)
                # Guardar el camino para usarlo después.
                paths_in_G[(min(t1,t2), max(t1,t2))] = path
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                # Si no hay camino entre dos terminales, el problema no tiene solución.
                return None, []
    
    # Comprobar si se pudo construir el grafo H.
    if H.number_of_nodes() == 0 or (H.number_of_edges() == 0 and len(terminals_to_use) > 1):
        return None, []

    # --- PASO 2: CALCULAR EL MST DEL GRAFO MÉTRICO ---
    # Esto nos da un esqueleto de bajo costo que conecta todos los terminales.
    mst_H = nx.minimum_spanning_tree(H, weight='weight')
    
    # --- PASO 3: RECONSTRUIR EL SUBGRAFO EN G ---
    # Se crea un subgrafo en G uniendo todos los caminos que formaron el mst_H.
    steiner_graph_edges_set = set()
    for u_h, v_h, _ in mst_H.edges(data=True):
        # Recuperar el camino original en G.
        path_uv = paths_in_G[(min(u_h,v_h), max(u_h,v_h))]
        # Añadir todas las aristas de ese camino al conjunto.
        for i_path in range(len(path_uv) - 1):
            node1, node2 = path_uv[i_path], path_uv[i_path+1]
            original_weight = graph_nx_orig[node1][node2]['weight']
            # Guardar la arista con su peso original. El set evita duplicados.
            edge_tuple = tuple(sorted((node1, node2))) + (original_weight,)
            steiner_graph_edges_set.add(edge_tuple)

    # Crear un grafo NetworkX a partir de la unión de los caminos.
    S_union = nx.Graph()
    S_union.add_weighted_edges_from(list(steiner_graph_edges_set))

    if not S_union.nodes:
        return (0, [])

    # --- PASO 4: LIMPIAR EL SUBGRAFO CON OTRO MST ---
    # S_union conecta los terminales, pero puede tener ciclos.
    # Calcular el MST de S_union elimina los ciclos de forma óptima.
    final_tree_candidate = nx.minimum_spanning_tree(S_union, weight='weight')
    
    # --- PASO 5: PODAR EL ÁRBOL ---
    # Eliminar iterativamente las hojas del árbol que NO son terminales.
    # Esto refina la solución eliminando ramas innecesarias.
    terminals_set = set(terminals_to_use)
    while True:
        # Encontrar todas las hojas (nodos con grado 1) que no son terminales.
        hojas_a_podar = [
            node for node, degree in final_tree_candidate.degree()
            if degree == 1 and node not in terminals_set
        ]
        if not hojas_a_podar:
            # Si no hay más hojas que podar, el proceso termina.
            break
        # Eliminar las hojas encontradas.
        final_tree_candidate.remove_nodes_from(hojas_a_podar)

    # --- CÁLCULO FINAL ---
    # Calcular el costo total y la lista de aristas del árbol podado final.
    aristas_finales = []
    costo_final = 0
    for u, v, data in final_tree_candidate.edges(data=True):
        aristas_finales.append((u, v, data['weight']))
        costo_final += data['weight']
    
    
    return costo_final, aristas_finales


def graph(graph_nx: nx.Graph):
    """
    Solicita al usuario los nodos terminales para generar un árbol de Steiner
    Grafica el grafo original y el Árbol de Steiner resultante,
    resaltando los nodos terminales y las aristas del árbol.
   .

    Args:
        graph_nx (nx.Graph): El grafo original.
    """
    # Mostrar los nodos existentes para que el usuario pueda elegirlos
    print(f"\nNodos disponibles en el grafo: {list(graph_nx.nodes())}")

    # Solicitar al usuario los nodos terminales
    while True:
        terminals_input = input("Ingresa los nodos terminales separados por comas (e.g., 0,2,4): ")
        try:
            # Convertir la entrada a una lista de enteros
            terminals = [int(t.strip()) for t in terminals_input.split(',')]
            
            # Verificar que los terminales ingresados existan en el grafo
            if all(node in graph_nx.nodes() for node in terminals):
                break
            else:
                print("Alguno de los nodos terminales ingresados no existe en el grafo. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar números separados por comas.")
        except Exception as e:
            print(f"Ocurrió un error: {e}. Intenta de nuevo.")

    costo, steiner_edges_data = kmb(graph_nx, terminals)

    if costo is None:
        print("No se pudo encontrar una solución para el Árbol de Steiner con los terminales dados.")
        return

    steiner_edges = [(u, v) for u, v, _ in steiner_edges_data]
    steiner_nodes = set()
    for u, v, _ in steiner_edges_data:
        steiner_nodes.add(u)
        steiner_nodes.add(v)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph_nx, seed=42)  

    # 1. Dibujar todas las aristas del grafo original (en gris claro)
    nx.draw_networkx_edges(graph_nx, pos, edge_color="lightgray", width=1, alpha=0.7)

    # 2. Dibujar todas los nodos del grafo original (en gris claro)
    nx.draw_networkx_nodes(graph_nx, pos, node_color="lightgray", node_size=300, alpha=0.7)

    # 3. Dibujar las aristas del Árbol de Steiner (en azul)
    nx.draw_networkx_edges(graph_nx, pos, edgelist=steiner_edges, edge_color="blue", width=2.5)

    # 4. Dibujar los nodos del Árbol de Steiner (en azul, más grandes)
    nx.draw_networkx_nodes(graph_nx, pos, nodelist=list(steiner_nodes), node_color="skyblue", node_size=500)

    # 5. Dibujar los nodos terminales (en rojo, más grandes aún)
    nx.draw_networkx_nodes(graph_nx, pos, nodelist=terminals, node_color="red", node_size=700)

    # 6. Etiquetas de los nodos
    nx.draw_networkx_labels(graph_nx, pos, font_size=10, font_weight="bold")

    # 7. Etiquetas de los pesos de las aristas del grafo original
    edge_labels = nx.get_edge_attributes(graph_nx, 'weight')
    nx.draw_networkx_edge_labels(graph_nx, pos, edge_labels=edge_labels, font_size=8, alpha=0.8)

    plt.axis("off")
    plt.title(f"Árbol de Steiner (KMB) - Costo Total: {costo:.2f}", size=15)
    plt.show()
