import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handelCat(self):
        for c in self._model.getCat():
            self._view._ddcategory.options.append(ft.dropdown.Option(key = str(c[0]) , text = str(c[1])))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        categoria = self._view._ddcategory.value
        data1 = self._view._dp1.value
        data2 = self._view._dp2.value
        if categoria is None or data1 is None or data2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Prima scegli una categoria e le sue date", color="red"))
            return
        self._model.buildGraph(categoria,data1,data2)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato\nN.nodi: {self._model.graph_details()[0]}\nN.archi: {self._model.graph_details()[1]}"))
        self._view.update_page()

    def handleBestProdotti(self, e):
        # Primo controllo: assicuriamoci che l'utente abbia creato il grafo
        if len(self._model._graph.nodes) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Crea prima il grafo!", color="red"))
            self._view.update_page()
            return

        # Chiediamo al model i 5 migliori
        top5 = self._model.top5()  # <-- Cambiato nome metodo per coincidere con model.py

        # Stampiamo i risultati nell'interfaccia
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("I cinque prodotti più venduti sono:"))

        for prodotto, score in top5:
            # Stampiamo nome del prodotto, anno e score (seguendo lo screenshot di esempio del PDF)
            riga = f"{prodotto.product_name} - {prodotto.model_year} with score {score}"
            self._view.txt_result.controls.append(ft.Text(riga))

        self._view.update_page()

    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
