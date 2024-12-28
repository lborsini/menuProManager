from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

class MainFrame(QMainWindow):
    def __init__(self, app_controlador=None):  # Acepta un argumento adicional
        super().__init__()
        self.app_controlador = app_controlador  # Guarda la referencia al controlador principal
        self.main = uic.loadUi('interface/main_frame.ui', self)  # Carga el archivo .ui
        self.init_ui()

        # Conectar las acciones del menú a métodos específicos
        self.main.newMenu.triggered.connect(self.show_pag_newMenu)
        #self.main.history.triggered.connect(self.show_pag_history)
        #self.main.purcharseOrder.triggered.connect(self.show_pag_purcharseOrder)
        self.main.newDish.triggered.connect(self.show_pag_newDish)
        self.main.updateDish.triggered.connect(self.show_pag_updateDish)
        self.main.newUser.triggered.connect(self.show_pag_manage_users)

    def init_ui(self):
        self.apply_shadow(self.main.btn_main_submit_7)  # Aplica sombras a los widgets
        self.apply_shadow(self.main.stackedWidget)
        self.apply_shadow(self.main.btn_main_submit_3)
        self.apply_shadow(self.main.btn_main_preView_3)
        self.apply_shadow(self.main.label_12)

    def apply_shadow(self, widget):
        """Aplica un efecto de sombra a los widgets."""
        shadow = QtWidgets.QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(10)
        shadow.setColor(QtCore.Qt.black)
        shadow.setOffset(3, 3)
        widget.setGraphicsEffect(shadow)

    # Métodos para cambiar las páginas del QStackedWidget
    def show_pag_newMenu(self):
        self.main.stackedWidget.setCurrentWidget(self.main.pag_create_menu)

    def show_pag_history(self):
        self.main.stackedWidget.setCurrentWidget(self.main.pag_History)

    def show_pag_purcharseOrder(self):
        self.main.stackedWidget.setCurrentWidget(self.main.pag_purcharseOrder)

    def show_pag_newDish(self):
        self.main.stackedWidget.setCurrentWidget(self.main.pag_dish_createNewDish)

    def show_pag_updateDish(self):
        self.main.stackedWidget.setCurrentWidget(self.main.pag_update_dish)

    def show_pag_manage_users(self):
        self.main.stackedWidget.setCurrentWidget(self.main.pag_manageUser)

        