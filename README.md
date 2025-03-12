# Proyecto U1 - Grafo de Red Social

Este proyecto es una aplicación en **Python** que permite gestionar y visualizar grafos de redes sociales mediante la interfaz gráfica de **Tkinter** y las bibliotecas **NetworkX** y **Matplotlib**.

## 📌 Características
- 📍 **Creación y edición de nodos.**
- 🔗 **Representación de conexiones entre nodos.**
- 🔍 **Identificación de componentes fuertemente conectados** mediante los algoritmos de **Kosaraju** y **Tarjan**.
- 🎨 **Visualización del grafo** con colores diferenciados para los componentes.

## 🛠️ Requisitos
Asegúrese de tener instaladas las siguientes dependencias antes de ejecutar el proyecto:

```sh
pip install tkinter networkx matplotlib
```

## 🚀 Uso
Ejecute el script con el siguiente comando:

```sh
python Proyecto_U1.py
```

## 🖥️ Interfaz gráfica
1. **➕ Nuevo Nodo (+)**: Agregar un nuevo nodo con sus conexiones.
2. **✏️ Editar Nodo**: Modificar las conexiones de un nodo existente.
3. **⚙️ Procesar Nodos**: Ejecutar los algoritmos de **Kosaraju** y **Tarjan** para detectar componentes fuertemente conectados y visualizar el grafo resultante.

## 📊 Algoritmos Implementados
### 🔹 Kosaraju
Encuentra los **componentes fuertemente conectados** utilizando **DFS** y el grafo transpuesto.

### 🔹 Tarjan
Algoritmo basado en **búsqueda en profundidad (DFS)** para encontrar **componentes fuertemente conectados** con baja complejidad temporal.

## 👤 Autores
**Edison Giancarlo Garcia Castro**

**Angel Ibangovich**

**Sandra Yasmin Gomez Rodriguez**

**Elias Rodriguez**

**Ingrid Yamileth Ortega Castillo**