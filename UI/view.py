import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP Exercise on MIA Art database"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None
        self.ddlunghezza = None
        self.btnPercorsoOttimo = None

    def load_interface(self):
        # title
        self._title = ft.Text("Database collezione di Tonon", color="orange", size=24)
        self._page.controls.append(self._title)

        # controls
        self._btnAnalizzaOggetti = ft.ElevatedButton(text="Analizza oggetti",
                                                     on_click=self._controller.handleAnalizzaOggetti,
                                                     bgcolor="orange",
                                                     color="white",
                                                     width=200)
        self._txtIdOggetto = ft.TextField(label="Id Oggetto", color="orange", border_color="orange", disabled=True)
        self._btnCompConnessa = ft.ElevatedButton(text="Cerca Connessa", on_click=self._controller.handleCompConnessa,
                                                  bgcolor="orange",
                                                  color="white",
                                                  width=200, disabled=True)
        self._btnCercaOggetto = ft.ElevatedButton(text="Cerca Oggetto", on_click=self._controller.cercaOggetto,
                                                  bgcolor="orange",
                                                  color="white",
                                                  width=360, disabled=True)
        self.ddlunghezza = ft.Dropdown(label="Lunghezza", disabled=True)
        self.btnPercorsoOttimo = ft.ElevatedButton(text="Percorso", on_click=self._controller.handlePercorsoOttimo, bgcolor="orange",
                                                   color="white",
                                                   disabled=True, width=360)
        riga2 = ft.Row([self.ddlunghezza], alignment="CENTER")
        riga3 = ft.Row([self._btnCercaOggetto, self.btnPercorsoOttimo], alignment="CENTER")
        self._page.controls.append(ft.Row([self._btnAnalizzaOggetti, self._txtIdOggetto, self._btnCompConnessa],
                                          alignment=ft.MainAxisAlignment.CENTER))
        self._page.controls.append(riga2)
        self._page.controls.append(riga3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller
    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller
    def update_page(self):
        self._page.update()
