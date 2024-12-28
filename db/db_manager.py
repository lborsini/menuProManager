import sqlite3
import bcrypt
import json

class Database:
    def __init__(self, db_path="app_database.db"):
        """Inicializa la conexión a la base de datos."""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.init_db()

    def init_db(self):
        """Crea las tablas necesarias si no existen."""
        cursor = self.conn.cursor()

        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
            )
        """)

        # Tabla de secciones

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)

        # Tabla de platos

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                section_id INTEGER NOT NULL,
                ingredients TEXT, -- Almacena JSON de ingredientes y cantidades
                FOREIGN KEY (section_id) REFERENCES sections (id)
            )
        """)

        # Tabla de menús

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                dishes TEXT, -- Almacena JSON con platos organizados por sección
                toppings TEXT -- Almacena JSON con toppings y cantidades
            )
        """)

        # Tabla de historial de menús

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu_id INTEGER NOT NULL,
                pdf_path TEXT NOT NULL,
                FOREIGN KEY (menu_id) REFERENCES menus (id)
            )
        """)

        # Tabla de órdenes de compra

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                ingredients TEXT, -- Almacena JSON con ingredientes y cantidades
                pdf_path TEXT NOT NULL
            )
        """)

        self.conn.commit()

    def hash_password(self, password):
        """Hashea una contraseña usando bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    # -------- CRUD para Usuarios -------- #

    def add_user(self, username, password, role):
        """Agrega un nuevo usuario a la base de datos."""
        cursor = self.conn.cursor()
        try:
            hashed_password = self.hash_password(password)
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, hashed_password, role))
            self.conn.commit()
            return f"Usuario '{username}' agregado exitosamente."
        except sqlite3.IntegrityError:
            return f"Error: El usuario '{username}' ya existe."

    def get_users(self):
        """Obtiene todos los usuarios de la base de datos."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        return [{"id": user[0], "username": user[1], "role": user[2]} for user in users]

    def update_user(self, user_id, username=None, password=None, role=None):
        """Actualiza un usuario existente en la base de datos."""
        cursor = self.conn.cursor()
        try:
            if username:
                cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
            if password:
                hashed_password = self.hash_password(password)
                cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
            if role:
                cursor.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
            self.conn.commit()
            return f"Usuario con ID {user_id} actualizado exitosamente."
        except sqlite3.Error as e:
            return f"Error al actualizar el usuario: {e}"

    def delete_user(self, user_id):
        """Elimina un usuario de la base de datos."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.conn.commit()
            return f"Usuario con ID {user_id} eliminado exitosamente."
        except sqlite3.Error as e:
            return f"Error al eliminar el usuario: {e}"

    # -------- CRUD para Secciones -------- #

    def add_section(self, name):
        """Agrega una nueva sección."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO sections (name) VALUES (?)", (name,))
            self.conn.commit()
            return f"Sección '{name}' agregada exitosamente."
        except sqlite3.IntegrityError:
            return f"Error: La sección '{name}' ya existe."


    def get_sections(self):
        """Obtiene todas las secciones."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM sections")
        sections = cursor.fetchall()
        return [{"id": section[0], "name": section[1]} for section in sections]


    def update_section(self, section_id, name):
        """Actualiza una sección."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE sections SET name = ? WHERE id = ?", (name, section_id))
            self.conn.commit()
            return f"Sección con ID {section_id} actualizada exitosamente."
        except sqlite3.Error as e:
            return f"Error al actualizar la sección: {e}"


    def delete_section(self, section_id):
        """Elimina una sección."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM sections WHERE id = ?", (section_id,))
            self.conn.commit()
            return f"Sección con ID {section_id} eliminada exitosamente."
        except sqlite3.Error as e:
            return f"Error al eliminar la sección: {e}"

    # -------- CRUD para Platos -------- #

    def add_dish(self, name, section_id, ingredients):
        """Agrega un nuevo plato con ingredientes."""
        cursor = self.conn.cursor()
        try:
            ingredients_json = json.dumps(ingredients)  # Convertir ingredientes a JSON
            cursor.execute("INSERT INTO dishes (name, section_id, ingredients) VALUES (?, ?, ?)",
                           (name, section_id, ingredients_json))
            self.conn.commit()
            return f"Plato '{name}' agregado exitosamente."
        except sqlite3.IntegrityError:
            return f"Error: El plato '{name}' ya existe."

    def get_dishes(self):
        """Obtiene todos los platos, junto con sus secciones e ingredientes."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT d.id, d.name, s.name AS section_name, d.ingredients
            FROM dishes d
            JOIN sections s ON d.section_id = s.id
        """)
        dishes = cursor.fetchall()
        return [{"id": dish[0], "name": dish[1], "section": dish[2], 
                 "ingredients": json.loads(dish[3])} for dish in dishes]

    def update_dish(self, dish_id, name=None, section_id=None, ingredients=None):
        """Actualiza un plato existente."""
        cursor = self.conn.cursor()
        try:
            if name:
                cursor.execute("UPDATE dishes SET name = ? WHERE id = ?", (name, dish_id))
            if section_id:
                cursor.execute("UPDATE dishes SET section_id = ? WHERE id = ?", (section_id, dish_id))
            if ingredients:
                ingredients_json = json.dumps(ingredients)
                cursor.execute("UPDATE dishes SET ingredients = ? WHERE id = ?", (ingredients_json, dish_id))
            self.conn.commit()
            return f"Plato con ID {dish_id} actualizado exitosamente."
        except sqlite3.Error as e:
            return f"Error al actualizar el plato: {e}"


    def delete_dish(self, dish_id):
        """Elimina un plato de la base de datos."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM dishes WHERE id = ?", (dish_id,))
            self.conn.commit()
            return f"Plato con ID {dish_id} eliminado exitosamente."
        except sqlite3.Error as e:
            return f"Error al eliminar el plato: {e}"

    # -------- CRUD para Menús -------- #

    def add_menu(self, date, dishes, toppings):
        """Agrega un nuevo menú con platos y toppings."""
        cursor = self.conn.cursor()
        try:
            dishes_json = json.dumps(dishes)  # Convertir platos a JSON
            toppings_json = json.dumps(toppings)  # Convertir toppings a JSON
            cursor.execute("INSERT INTO menus (date, dishes, toppings) VALUES (?, ?, ?)",
                           (date, dishes_json, toppings_json))
            self.conn.commit()
            return f"Menú para la fecha '{date}' agregado exitosamente."
        except sqlite3.Error as e:
            return f"Error al agregar el menú: {e}"


    def get_menus(self):
        """Obtiene todos los menús registrados."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, date, dishes, toppings FROM menus")
        menus = cursor.fetchall()
        return [{"id": menu[0], "date": menu[1],
                 "dishes": json.loads(menu[2]), "toppings": json.loads(menu[3])} for menu in menus]


    def update_menu(self, menu_id, date=None, dishes=None, toppings=None):
        """Actualiza un menú existente."""
        cursor = self.conn.cursor()
        try:
            if date:
                cursor.execute("UPDATE menus SET date = ? WHERE id = ?", (date, menu_id))
            if dishes:
                dishes_json = json.dumps(dishes)
                cursor.execute("UPDATE menus SET dishes = ? WHERE id = ?", (dishes_json, menu_id))
            if toppings:
                toppings_json = json.dumps(toppings)
                cursor.execute("UPDATE menus SET toppings = ? WHERE id = ?", (toppings_json, menu_id))
            self.conn.commit()
            return f"Menú con ID {menu_id} actualizado exitosamente."
        except sqlite3.Error as e:
            return f"Error al actualizar el menú: {e}"


    def delete_menu(self, menu_id):
        """Elimina un menú de la base de datos."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM menus WHERE id = ?", (menu_id,))
            self.conn.commit()
            return f"Menú con ID {menu_id} eliminado exitosamente."
        except sqlite3.Error as e:
            return f"Error al eliminar el menú: {e}"

    # -------- CRUD para Órdenes de Compra -------- #

    def add_purchase_order(self, date, ingredients, pdf_path):
        """Agrega una nueva orden de compra."""
        cursor = self.conn.cursor()
        try:
            ingredients_json = json.dumps(ingredients)
            cursor.execute("INSERT INTO purchase_orders (date, ingredients, pdf_path) VALUES (?, ?, ?)",
                           (date, ingredients_json, pdf_path))
            self.conn.commit()
            return f"Orden de compra para la fecha '{date}' agregada exitosamente."
        except sqlite3.Error as e:
            return f"Error al agregar la orden de compra: {e}"


    def get_purchase_orders(self):
        """Obtiene todas las órdenes de compra."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, date, ingredients, pdf_path FROM purchase_orders")
        orders = cursor.fetchall()
        return [{"id": order[0], "date": order[1],
                 "ingredients": json.loads(order[2]), "pdf_path": order[3]} for order in orders]


    def delete_purchase_order(self, order_id):
        """Elimina una orden de compra."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM purchase_orders WHERE id = ?", (order_id,))
            self.conn.commit()
            return f"Orden de compra con ID {order_id} eliminada exitosamente."
        except sqlite3.Error as e:
            return f"Error al eliminar la orden de compra: {e}"


    def close(self):
        """Cierra la conexión a la base de datos."""
        self.conn.close()
