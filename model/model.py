from operator import attrgetter

import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.lista_rifugi=DAO.get_rifugi()
        self.rif_dict={}
        for rif in self.lista_rifugi:
            self.rif_dict[rif.id]=rif


    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO
        self.G.clear()
        connessioni=DAO.get_connessioni(year)
        for c in connessioni:
            self.G.add_edge(self.rif_dict[c.id_rifugio1],self.rif_dict[c.id_rifugio2])
        return self.G


    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        # TODO
        return list(self.G.nodes())


    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO
        vicini=list(self.G.neighbors(node))
        return len(vicini)

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO
        return nx.number_connected_components(self.G)

    def dfs_recursive(self,nodo,visitati):
        visitati.add(nodo)
        for neighbor in self.G.neighbors(nodo):
            if neighbor not in visitati:
                self.dfs_recursive(neighbor,visitati)
    def get_reachable_recursive(self,start):
        visitati=set()
        self.dfs_recursive(start,visitati)
        visitati.discard(start)
        return list(visitati)

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """

        # TODO
        bfs_albero=nx.bfs_tree(self.G,start)
        nodi_raggiungibili=[]
        for n in bfs_albero.nodes:
            if n!=start:
                nodi_raggiungibili.append(n)
        nodi_raggiungibili.sort(key=attrgetter('nome'))
        #return nodi_raggiungibili
        return self.get_reachable_recursive(start)