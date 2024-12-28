import sys
from PyQt5.QtWidgets import QApplication
from controllers.controlador_app import ControladorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controlador = ControladorApp()
    controlador.iniciar_aplicacion()  # Método principal del controlador
    sys.exit(app.exec_())
