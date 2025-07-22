from ST import graph as gph
from ST import steiner as st

if __name__ == "__main__":
    
    print("Árbol de Steiner: ")
    while True:
        g = gph.generate_graph()
        st.graph(g)
        opcion = input("\n¿Deseas generar otra gráfica? (s/n): ")
        if opcion.lower() != 's':
            break