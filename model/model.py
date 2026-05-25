import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        #serve id_map per riottenere oggetto (nodi) dato un codice id
        self.nodi = []
        self.idMap = {}
        self.bestPercorso = []
        self.bestCosto = 0

    def getbestPercorso(self, nodoSorgente, lunghezza):
        self.bestPercorso = []
        self.bestCosto = 0
        parziale = [nodoSorgente] #dovrà contenere nodoSorgente + altri aggiunti con ricorsione
        #dato che seguiamo gli archi conviene ciclare solo sui nodi vicini, dato che mi interessano gli archi, dell'ultimo nodo inserito
        for n in self.grafo.neighbors(nodoSorgente):
            #se la classe del nodo che sto aggiungengo è la stessa del precedente posso aggiungerlo
            if nodoSorgente.classification == parziale[-1].classification:
                parziale.append(n)
                self.ricorsione(parziale, lunghezza)
                parziale.pop() #backtracking per far funzionare la ricorsione
        #finito questo ciclo mi aspetto di avere i valori ottimi e quindi li posso restituire
        return self.bestPercorso, self.bestCosto

    def ricorsione(self, parziale, lunghezza):
        #verificare condizione di terminazione
        if len(parziale) == lunghezza:
            #verifico che questa parziale sia meglio della best, ed esco, percheè le prossime saranno piu lunghe di lun --> non valide
            if self.costoPercorso(parziale) > self.bestCosto:
                self.bestCosto = self.costoPercorso(parziale)
                self.bestPercorso = copy.deepcopy(parziale)
            return
        #altro caso --> len(parziale) è minore di lun mancano ancora nodi da inserire
        #ma questa volta lo faccio sull'ultimo nodo e non su sorgente ovviamente
        for n in self.grafo.neighbors(parziale[-1]):
            if parziale[-1].classification == n.classification: #se soddisfatta rifaccio ricorsione + backtracking
                parziale.append(n)
                self.ricorsione(parziale, lunghezza)
                parziale.pop()

    def costoPercorso(self, percorso):
            costo = 0
            for i in range(0, len(percorso) - 1): #cicla su tutti gli archi e va a sommare il peso, 'costo'
                costo += self.grafo[percorso[i]][percorso[i+1]]['weight']
            return costo


    def buildGraph(self):
        #aggiungo nodi
        self.nodi = DAO.getAllNodes()
        for oggetto in self.nodi:
            self.idMap[oggetto.object_id] = oggetto
        self.grafo.add_nodes_from(self.nodi)
        #aggiungo gli archi per ogni coppia di oggetti nella stessa mostra e li peso (se la coppia appare in più mostre
        #trucco mettere primo oggetto 1 id > oggetto 2 id tc la coppia appare una sola volta per evento e
        # non appaia anche oggetto 2 - oggetto 1
        connessioni = DAO.getAllEdgesPesati()
        for u,v,w in connessioni: #unpack rapido di tupla a 3 elementi
            nodoU = self.idMap[u]
            nodoV = self.idMap[v]
            self.grafo.add_edge(nodoU, nodoV, weight=w)


    def getConnessioniNodo(self, nodoV1):
        #ricava tutta la componente connessa dato un nodo dall'utente
        return   #usabile anche con piu nodi insieme


    def getNumNodes(self):
        return len(self.grafo.nodes())

    def getNumEdges(self):
        return len(self.grafo.edges())

    def cercaIdMap(self, id):
        if id in self.idMap:
            return self.idMap[id]
        else:
            return None