import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._DAO = DAO
        self._graph = nx.MultiDiGraph()
        self._idMapNodi = None

    def getDateRange(self):
        return DAO.getDateRange()
    def getCat(self):
        return self._DAO.get_categories()

    def buildGraph(self,categoria,data1,data2):
        self._graph.clear()
        self._idMapNodi = {p.product_id: p for p in self._DAO.get_nodes(categoria)}
        listaEdges = self._DAO.get_edges(categoria,data1,data2)
        for prod in self._idMapNodi.values():
            self._graph.add_node(prod)
        for a,b,p in listaEdges:
            for a2,b2,p2 in listaEdges:
                nodo1 = self._idMapNodi.get(a)
                nodo2 = self._idMapNodi.get(a2)
                peso = p + p2
                if nodo1 is not None and nodo2 is not None:
                    if nodo1.product_id < nodo2.product_id:
                        self._graph.add_edge(nodo1,nodo2,peso)
                    elif nodo1.product_id > nodo2.product_id:
                        self._graph.add_edge(nodo2, nodo1, peso)
                    else:
                        self._graph.add_edge(nodo1, nodo2, peso)
                        self._graph.add_edge(nodo2, nodo1, peso)

    def graph_details(self):
        return len(self._graph.nodes),len(self._graph.edges)


