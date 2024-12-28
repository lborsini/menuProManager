from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from controllers.controladores_login import ControladorLogin
from controllers.controladores_mainframe import MainFrame
from db.db_manager import Database

class ControladorApp(QMainWindow):
    def __init__(self):
        super(ControladorApp, self).__init__()
        self.ventana_actual = None
        self.controladores = {}
        self.db = Database('C:/Users/lean/Desktop/Menu Manager Pro/app_database.db')
        self.db.init_db()
        self.db.close()

    def iniciar_aplicacion(self):
        """Inicializa la aplicación cargando la ventana de login."""
        self.cargar_login()
        self.show()

    def cargar_login(self):
        """Carga la interfaz de login."""
        self.ventana_actual = LoginWindow(self)  # Instancia LoginWindow
        self.setCentralWidget(self.ventana_actual)

    def cargar_mainframe(self):
        """Carga la interfaz principal."""
        self.ventana_actual = MainFrame(self)
        self.setCentralWidget(self.ventana_actual)
        self.setFixedSize(1111, 888)


class LoginWindow(QMainWindow):
    def __init__(self, app_controlador):
        super(LoginWindow, self).__init__()
        loadUi("interface/login.ui", self)  # Carga el archivo .ui
        self.app_controlador = app_controlador
        self.controlador = ControladorLogin(self)  # Asocia ControladorLogin a esta ventana

        # Conecta el botón de login
        self.btn_submit_login.clicked.connect(self.validar_login)

    def validar_login(self):
        """Validar credenciales y manejar el flujo de la aplicación."""
        username = self.controlador.interfaz.entry_user_login.text().strip()
        password = self.controlador.interfaz.entry_pass_login.text().strip()

        user = self.controlador.validar_credenciales(username, password)

        if user:
            # Si las credenciales son válidas
            self.controlador.interfaz.lbl_error_login.setText("")
            self.app_controlador.cargar_mainframe()
        else:
            # Mostrar mensaje de error
            self.controlador.interfaz.lbl_error_login.setText("Usuario o contraseña incorrectos.")
            self.controlador.interfaz.lbl_error_login.setStyleSheet("color: red; font-size: 8pt; font-family: Arial;")
