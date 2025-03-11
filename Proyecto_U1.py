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

    def visualizar(self, sccs, nodos_sin_conexion, metodo):
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
        colores = [color_map.get(nodo, 0) for nodo in G.nodes()]

        plt.figure(figsize=(8, 6))
        plt.title(f"Visualización del Grafo - Método {metodo}")
        nx.draw(G, posicion, with_labels=True, node_color=colores, cmap=plt.cm.rainbow, node_size=500)
        plt.show()

class PerfilApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Perfiles")
        self.root.geometry("500x500")
        self.perfiles = []

        self.btn_nuevo_perfil = tk.Button(root, text="Nuevo Perfil (+)", command=self.nuevo_perfil, width=15, height=2)
        self.btn_nuevo_perfil.pack(pady=5)

        self.lista_perfiles = tk.Listbox(root)
        self.lista_perfiles.pack(pady=5, fill=tk.BOTH, expand=True)

        self.btn_editar_perfil = tk.Button(root, text="Editar Perfil", command=self.editar_perfil, width=15, height=2)
        self.btn_editar_perfil.pack(pady=5)

        self.btn_procesar_perfiles = tk.Button(root, text="Procesar Perfiles", command=self.procesar_perfiles, width=15, height=2)
        self.btn_procesar_perfiles.pack(side=tk.BOTTOM, pady=10, anchor='se')

    def nuevo_perfil(self):
        self.abrir_ventana_perfil(nuevo=True)

    def editar_perfil(self):
        seleccion = self.lista_perfiles.curselection()
        if seleccion:
            index = seleccion[0]
            self.abrir_ventana_perfil(nuevo=False, index=index)
        else:
            messagebox.showerror("Error", "Selecciona un perfil para editar.")

    def abrir_ventana_perfil(self, nuevo=False, index=None):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar/Editar Perfil")
        ventana.geometry("300x200")

        tk.Label(ventana, text="Nombre del Perfil:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack(pady=5)

        tk.Label(ventana, text="Conexiones (separadas por coma):").pack(pady=5)
        entry_conexiones = tk.Entry(ventana)
        entry_conexiones.pack(pady=5)

        if not nuevo and index is not None:
            perfil, conexiones = self.perfiles[index]
            entry_nombre.insert(0, perfil)
            entry_conexiones.insert(0, ','.join(conexiones))

        def aceptar():
            nombre = entry_nombre.get().strip()
            conexiones = [n.strip() for n in entry_conexiones.get().split(',') if n.strip()]
            if nuevo:
                self.perfiles.append((nombre, conexiones))
                self.lista_perfiles.insert(tk.END, f"Perfil {nombre}: {','.join(conexiones)}")
            else:
                self.perfiles[index] = (nombre, conexiones)
                self.lista_perfiles.delete(index)
                self.lista_perfiles.insert(index, f"Perfil {nombre}: {','.join(conexiones)}")
            ventana.destroy()

        tk.Button(ventana, text="Aceptar", command=aceptar, width=10, height=2).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(ventana, text="Cancelar", command=ventana.destroy, width=10, height=2).pack(side=tk.RIGHT, padx=10, pady=10)

    def procesar_perfiles(self):
        if not self.perfiles:
            messagebox.showerror("Error", "No hay perfiles para procesar.")
            return

        grafo = SocialNetWorkGraph(len(self.perfiles))
        for perfil, conexiones in self.perfiles:
            for conexion in conexiones:
                grafo.add_following(perfil, conexion)

        sccs_kosaraju = grafo.kosaraju()
        sccs_tarjan = grafo.tarjan()

        nodos_sin_conexion = [perfil for perfil, conexiones in self.perfiles if not conexiones]

        grafo.visualizar(sccs_kosaraju, nodos_sin_conexion, "Kosaraju")
        grafo.visualizar(sccs_tarjan, nodos_sin_conexion, "Tarjan")

if __name__ == "__main__":
    root = tk.Tk()
    app = PerfilApp(root)
    root.mainloop()
