import flet as ft
from time import time

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        inizio = time()
        self._model.buildGraph()
        fine = time()
        prime20 = list(self._model.grafo.edges(data=True))[:20]
        #stampo valori e varie cazzate sui nodi
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente in {(fine - inizio):.2f} secondi"
                                                      f"\nNumero nodi / oggetti = {self._model.getNumNodes()}"
                                              f"\nNumero archi pesati secondo criteri = {self._model.getNumEdges()}\nStampo i primi 15 archi per esempio:", color = "green"))

        for nodo in prime20:
            self._view.txt_result.controls.append(ft.Text(f"{nodo[0].object_id} -> {nodo[1].object_id} | peso = {nodo[2]['weight']}"))

        self._view._txtIdOggetto.disabled = False
        self._view._btnCercaOggetto.disabled = False
        self._view.update_page()

    def handleCompConnessa(self,e):
        if not self._view._txtIdOggetto.value.isdigit():
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Attenzione! Valore inserito non compatibile con la ricerca", color = "red"))
            self._view._btnCompConnessa.disabled = True #ogni volta che sbaglio mi forza a rifare la ricerca da capo
            self._view.btnPercorsoOttimo.disabled = True
            self._view.update_page()
            return
        nodo = self._model.cercaIdMap(int(self._view._txtIdOggetto.value))
        if nodo is not None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text(f"Nodo trovato! In corso ricerca della componente connessa al nodo"
                                                          f" {self._view._txtIdOggetto.value}..." , color = "green"))
            #stampo connessioni
            connessioni = self._model.getConnessioniNodo(nodo)
            maxLunghezza = len(connessioni)
            for c in connessioni:
                self._view.txt_result.controls.append(ft.Text(c))
            self._view.txt_result.controls.append(
                ft.Text(f"Trovati {maxLunghezza} nodi connessi.", color="green"))
            #aggiungere il riempimento del menu dropdown
            self._view.ddlunghezza.disabled = False #si attiva solo se esiste una connessa diobo
            self._view.btnPercorsoOttimo.disabled = False
            for i in range(2, maxLunghezza):
                self._view.ddlunghezza.options.append(ft.dropdown.Option(i))#appendo un opzione
            self._view.update_page()
        else:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(
                ft.Text(f"Il nodo selezionato ({self._view._txtIdOggetto.value}), non esiste"
                        f",si prega di rieffettuare ricerca oggetto da capo", color="red"))
            self._view._btnCompConnessa.disabled = True
            self._view.btnPercorsoOttimo.disabled = True
            self._view.update_page()
        return


    def handlePercorsoOttimo(self,e):
        #so che id è valido perchè il puslante si attiva se e solo se tutto è soddisfatto
        sorgente = self._model.cercaIdMap(int(self._view._txtIdOggetto.value))
        lunghezza = self._view.ddlunghezza.value
        print(lunghezza)
        if lunghezza is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Selezionare una lunghezza minchione!", color = "red"))
            self._view.update_page()
            return
        inizio = time()
        percorso, costo = self._model.getbestPercorso(sorgente, int(lunghezza))
        fine = time()
        if percorso is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Nessun percorso ottimo disponibile possibile", color = "orange"))
            self._view.update_page()
            return
        else:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text(f"Cammino trovato (in {fine - inizio:.2f}s) a partire dal nodo selezionato '{sorgente}'"
                                                  f", con costo pari a {costo}, di seguito stampo i nodi appartenenti"
                                                  f"al percorso ottimo di lunghezza selezionata {lunghezza}:", color = "green"))
            for nodo in percorso:
                self._view.txt_result.controls.append(ft.Text(nodo))
            self._view.update_page()
            return





    #extra facile, connette e verifica idMap nelle chiavi se c'è un oggetto e ne restituisce il riferimento
    def cercaOggetto(self,e):
        if not self._view._txtIdOggetto.value.isdigit():
            self._view.txt_result.controls.append(ft.Text("Attenzione! Valore inserito non compatibile con la ricerca" , color = "red"))
            self._view.update_page()
            return
        oggetto = self._model.cercaIdMap(int(self._view._txtIdOggetto.value))
        if oggetto is not None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text(f"Oggetto trovato:  {oggetto}\n\n"
                                                          f"Ora è possibile passare alla ricerca componente connessa"
                                                          f" del nodo selezionato"))
            self._view._btnCompConnessa.disabled = False
            self._view.update_page()
        else:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text(f"Non esiste un oggetto con ID = {self._view._txtIdOggetto.value}!", color = "red"))
            self._view._btnCompConnessa.disabled = True
            self._view.btnPercorsoOttimo.disabled = True
            self._view.update_page()
        return