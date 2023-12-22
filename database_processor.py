import datetime
import mysql.connector
from config import DATABASE_CONFIG


class DatabaseProcessor:
    def __init__(self):
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def create_connection(self):
        """
        Crea y devuelve una conexión a la base de datos.
        """
        try:
            conn = mysql.connector.connect(**DATABASE_CONFIG)
            if conn.is_connected():
                print("Conexión a la base de datos establecida exitosamente")
                return conn
            else:
                print("No se pudo establecer la conexión a la base de datos")
        except mysql.connector.Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    # trae el siguiente registro
    def fetch_next_record(self, district):
        query = """
            SELECT r.*
                FROM registros r 
                JOIN secciones s ON r.seccion = s.num_seccion
            WHERE (isnull(estatus) OR r.estatus = 'Error Inesperado') AND s.dist_fed = %s
            ORDER BY id ASC LIMIT 1
            """
        self.cursor.execute(query, (district,))
        result = self.cursor.fetchone()
        return result

    def fetch_districts(self):
        """
        Fetches all available districts.
        """
        query = "SELECT DISTINCT distrito FROM usuarios ORDER BY distrito"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_users_by_district(self, district):
        """
        Fetches users for a given district.
        """
        query = """
        SELECT usuario, CONCAT(nombre, ' ', paterno, ' ', materno) as nombre_completo, usuario, contrasena 
        FROM usuarios WHERE distrito = %s ORDER BY nombre_completo
        """
        self.cursor.execute(query, (district,))
        return self.cursor.fetchall()

    def update_record_start(self, record_id, start_time):
        # start_time = datetime.now()
        query = "UPDATE registros SET inicio = %s, estatus = 'en_proceso' WHERE id = %s"
        self.cursor.execute(query, (start_time, record_id))
        self.conn.commit()

    def update_record_end(self, record_id, end_time, status):
        # end_time = datetime.now()
        query = "UPDATE registros SET fin = %s, estatus = %s WHERE id = %s"
        self.cursor.execute(query, (str(end_time), str(status), record_id))
        self.conn.commit()

    def reconnect(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass  # La conexión ya estaba cerrada o no se pudo cerrar
        try:
            self.conn = self.create_connection()
            self.cursor = self.conn.cursor(dictionary=True)
            print("Reconexión a la base de datos exitosa.")
        except Exception as e:
            print(f"Error al reconectar a la base de datos: {e}")

    def __del__(self):
        self.cursor.close()
        self.conn.close()
