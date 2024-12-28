import sqlite3
import bcrypt
from PyQt5 import QtCore, QtWidgets


class ControladorLogin:
    def __init__(self, interfaz):
        self.interfaz = interfaz
        self.conexion = sqlite3.connect("app_database.db")  # Ruta a la base de datos
        self.interfaz.entry_user_login.setFocus()  # Foco inicial en el campo de usuario
        self.interfaz.setTabOrder(self.interfaz.entry_user_login, self.interfaz.entry_pass_login)  # Tab de Usuario a Contraseña
        self.interfaz.setTabOrder(self.interfaz.entry_pass_login, self.interfaz.btn_submit_login)
        self.interfaz.btn_submit_login.setDefault(True)

        self.apply_shadow(self.interfaz.entry_user_login)
        self.apply_shadow(self.interfaz.entry_pass_login)
        self.apply_shadow(self.interfaz.btn_submit_login)
        self.apply_shadow(self.interfaz.lbl_login_login)
        self.apply_shadow(self.interfaz.lbl_user_login)
        self.apply_shadow(self.interfaz.label)
        self.apply_shadow(self.interfaz.lbl_pass_login)
        self.apply_shadow(self.interfaz.frame)
        self.apply_shadow(self.interfaz.loginFrame)
        self.apply_shadow(self.interfaz.lbl_error_login)

        

    def validar_credenciales(self, username, plain_password):
        cursor = self.conexion.cursor()
        try:
            # Obtener la contraseña hasheada del usuario
            cursor.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            # Si no se encuentra el usuario
            if not user:
                return None

            # Extraer datos del usuario
            user_id, db_username, hashed_password, role = user

            # Verificar la contraseña usando bcrypt
            if bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
                # Credenciales válidas, devolver los detalles del usuario
                return {"id": user_id, "username": db_username, "role": role}
            else:
                # Contraseña incorrecta
                return None
        except sqlite3.Error as e:
            self.interfaz.lbl_error_login.setText(f"Error al validar credenciales: {e}")
            return None

    def apply_shadow(self, widget):
        """Aplica un efecto de sombra a los widgets."""
        shadow = QtWidgets.QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(10)
        shadow.setColor(QtCore.Qt.black)
        shadow.setOffset(3, 3)
        widget.setGraphicsEffect(shadow)
