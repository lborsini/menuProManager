import sqlite3
import json
import bcrypt

class DatabaseController:
    def __init__(self, db_path="app_database.db"):
        """Conexión a la base de datos"""
        self.conn = sqlite3.connect(db_path)
        self.init_db()

    def init_db(self):
        """Inicializa las tablas de la base de datos"""
        cursor = self.conn.cursor()

        # Crear tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
            )
        """)

        # Crear tabla de secciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)

        # Crear tabla de platos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                section_id INTEGER NOT NULL,
                ingredients TEXT, -- Almacena ingredientes en formato JSON
                FOREIGN KEY (section_id) REFERENCES sections (id)
            )
        """)

        # Crear tabla de menús
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                dishes TEXT, -- Almacena platos seleccionados en formato JSON
                toppings TEXT -- Almacena toppings en formato JSON
            )
        """)

        # Crear tabla de órdenes de compra
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                ingredients TEXT, -- Almacena ingredientes para la orden en formato JSON
                pdf_path TEXT NOT NULL
            )
        """)

        self.conn.commit()

    def hash_password(self, password):
        """Hashea una contraseña usando bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def close(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()
