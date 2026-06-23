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
        for id1, vendite1 in listaEdges:
            for id2,vendite2 in listaEdges:
                if id1 < id2:
                    nodo1 = self._idMapNodi.get(id1)
                    nodo2 = self._idMapNodi.get(id2)

                    if nodo1 is not None and nodo2 is not None:
                        peso = int(vendite1) + int(vendite2)
                        if vendite1 < vendite2:
                            self._graph.add_edge(nodo1,nodo2,peso)
                        elif vendite1 > vendite2:
                            self._graph.add_edge(nodo2, nodo1, peso)
                        else:
                            self._graph.add_edge(nodo1, nodo2, peso)
                            self._graph.add_edge(nodo2, nodo1, peso)
    def top5(self):
        lista = []
        for n in self._graph.nodes:
            peso_in = self._graph.in_degree(n, weight ='weight')
            peso_out = self._graph.out_degree(n, weight ='weight')
            score = peso_out-peso_in
            lista.append((n,score))
            lista.sort(key=lambda x: x[1], reverse= True)
            return lista[:5]

    def graph_details(self):
        return len(self._graph.nodes),len(self._graph.edges)


