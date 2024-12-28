from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

class MainFrame(QMainWindow):
    def __init__(self, app_controlador=None):  # Acepta un argumento adicional
        super().__init__()
        self.app_controlador = app_controlador  # Guarda la referencia al controlador principal
        self.main = uic.loadUi('interface/main_frame.ui', self)  # Carga el archivo .ui
        self.init_ui()

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
