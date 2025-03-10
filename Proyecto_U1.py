import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

class SocialNetWorkGraph:
    def __init__(self, users):
        self.adj = {}
    
    @property
    def V(self):
        return len(self.adj)

    def add_following(self, u, v):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)

    def dfs(self, v, visitante, stack):
        visitante.add(v)
        for vecino in self.adj.get(v, []):
            if vecino not in visitante:
                self.dfs(vecino, visitante, stack)
        stack.append(v)

    def transpose(self):
        Gt = SocialNetWorkGraph(len(self.adj))
        for v in self.adj:
            for vecino in self.adj[v]:
                Gt.add_following(vecino, v)
        return Gt

    def dfs_scc(self, v, visitante, componente):
        visitante.add(v)
        componente.append(v)
        for vecino in self.adj.get(v, []):
            if vecino not in visitante:
                self.dfs_scc(vecino, visitante, componente)

    def kosaraju(self):
        stack = []
        visitante = set()
        for nodo in self.adj:
            if nodo not in visitante:
                self.dfs(nodo, visitante, stack)
        
        transpose_graph = self.transpose()
        visitante.clear()
        sccs = []
        while stack:
            v = stack.pop()
            if v not in visitante:
                componente = []
                transpose_graph.dfs_scc(v, visitante, componente)
                sccs.append(componente)
        return sccs

    def tarjan_dfs(self, u, ids, low, on_stack, stack, sccs, index):
        ids[u] = low[u] = index[0]
        index[0] += 1
        stack.append(u)
        on_stack.add(u)

        for v in self.adj.get(u, []):
            if ids.get(v, -1) == -1:
                self.tarjan_dfs(v, ids, low, on_stack, stack, sccs, index)    
                low[u] = min(low[u], low[v])
            elif v in on_stack:
                low[u] = min(low[u], ids[v])

        if ids[u] == low[u]:
            scc = []
            while True:
                v = stack.pop()
                on_stack.remove(v)
                scc.append(v)
                if v == u:
                    break
            sccs.append(scc)

    def tarjan(self):
        ids = {}
        low = {}
        on_stack = set()
        stack = []
        sccs = []
        index = [0]

        for nodo in self.adj:
            if nodo not in ids:
                self.tarjan_dfs(nodo, ids, low, on_stack, stack, sccs, index)
        
        return sccs

    def visualizar(self, sccs, nodos_sin_conexion):
        G = nx.DiGraph()
        color_map = {}
        for i, componente in enumerate(sccs):
            for nodo in componente:
                color_map[nodo] = i
                for vecino in self.adj.get(nodo, []):
                    G.add_edge(nodo, vecino)

        for nodo in nodos_sin_conexion:
            G.add_node(nodo) 

        posicion = nx.spring_layout(G, k=0.5, seed=42)
        
        
        colores = []
        for nodo in G.nodes():
            if nodo in nodos_sin_conexion:
                colores.append(0)  
            else:
                colores.append(color_map.get(nodo, 0)) 

        
        nx.draw(G, posicion, with_labels=True, node_color=colores, cmap=plt.cm.rainbow, node_size=500)
        plt.show()

class NodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Nodos")
        self.root.geometry("500x500")
        self.nodos = []
        self.current_nodo = 'A'

        self.btn_nuevo_nodo = tk.Button(root, text="Nuevo Nodo (+)", command=self.nuevo_nodo, width=15, height=2)
        self.btn_nuevo_nodo.pack(pady=5)

        self.lista_nodos = tk.Listbox(root)
        self.lista_nodos.pack(pady=5, fill=tk.BOTH, expand=True)

        self.btn_editar_nodo = tk.Button(root, text="Editar Nodo", command=self.editar_nodo, width=15, height=2)
        self.btn_editar_nodo.pack(pady=5)

        self.btn_procesar_nodos = tk.Button(root, text="Procesar Nodos", command=self.procesar_nodos, width=15, height=2)
        self.btn_procesar_nodos.pack(side=tk.BOTTOM, pady=10, anchor='se')
    
    def nuevo_nodo(self):
        self.abrir_ventana_nodo(self.current_nodo, nuevo=True)

    def abrir_ventana_nodo(self, nodo, nuevo=False, index=None):
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Editar Nodo {nodo}")
        ventana.geometry("300x150")

        label = tk.Label(ventana, text=f"Nodo {nodo}:")
        label.pack(pady=5)

        entry = tk.Entry(ventana)
        entry.pack(pady=5)

        if not nuevo and index is not None:
            entry.insert(0, ','.join(self.nodos[index][1]))

        def aceptar():
            adyacencias = entry.get()
            conexiones = [n.strip() for n in adyacencias.split(',') if n.strip()]
            if nuevo:
                self.nodos.append((nodo, conexiones))
                self.lista_nodos.insert(tk.END, f"Nodo {nodo}: {adyacencias}")
                self.current_nodo = chr(ord(self.current_nodo) + 1)
            else:
                self.nodos[index] = (nodo, conexiones)
                self.lista_nodos.delete(index)
                self.lista_nodos.insert(index, f"Nodo {nodo}: {adyacencias}")
            ventana.destroy()

        btn_aceptar = tk.Button(ventana, text="Aceptar", command=aceptar, width=10, height=2)
        btn_aceptar.pack(side=tk.LEFT, padx=10, pady=10)

        btn_cancelar = tk.Button(ventana, text="Cancelar", command=ventana.destroy, width=10, height=2)
        btn_cancelar.pack(side=tk.RIGHT, padx=10, pady=10)

    def editar_nodo(self):
        seleccion = self.lista_nodos.curselection()
        if seleccion:
            index = seleccion[0]
            nodo, _ = self.nodos[index]
            self.abrir_ventana_nodo(nodo, nuevo=False, index=index)

    def procesar_nodos(self):
        if not self.nodos:
            messagebox.showerror("Error", "No hay nodos para procesar.")
            return

        grafo = SocialNetWorkGraph(len(self.nodos))
        for nodo, conexiones in self.nodos:
            for conexion in conexiones:
                grafo.add_following(nodo, conexion)

        sccs_kosaraju = grafo.kosaraju()
        sccs_tarjan = grafo.tarjan()

    
        nodos_sin_conexion = [nodo for nodo, conexiones in self.nodos if not conexiones]

        grafo.visualizar(sccs_kosaraju, nodos_sin_conexion)
        grafo.visualizar(sccs_tarjan, nodos_sin_conexion)

if __name__ == "__main__":
    root = tk.Tk()
    app = NodoApp(root)
    root.mainloop()
