# ui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from database_processor import DatabaseProcessor
from web_form_filler import main
import threading
import os
from datetime import datetime


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Captura Masiva")
        master.configure(bg='white')
        self.db_processor = DatabaseProcessor()
        self.user_var = ""
        self.district_var = ""

        style = ttk.Style()
        style.theme_use('default')

        guinda_color = '#800000'
        style.configure('TButton', background=guinda_color, foreground='white')
        style.configure('TLabel', background='white', foreground=guinda_color)
        style.configure('TEntry', fieldbackground='white', foreground='black')
        style.configure('TMenubutton', background='white',
                        foreground=guinda_color)

        style.map('TButton', background=[
                  ('active', guinda_color)], foreground=[('active', 'white')])

        # Distritos
        self.district_var = tk.StringVar(master)
        self.district_var.trace("w", self.district_selected)
        self.optionmenu_district = ttk.OptionMenu(
            master, self.district_var, "Selecciona un Distrito", *[])
        self.optionmenu_district.grid(
            row=0, column=1, padx=10, pady=5, sticky="ew")
        self.load_districts()

        # Usuarios
        self.user_var = tk.StringVar(master)
        self.user_var.trace(
            "w", lambda *args: self.verificar_datos_completos(*args))
        self.optionmenu_user = ttk.OptionMenu(
            master, self.user_var, "Selecciona un Usuario", *[])
        self.optionmenu_user.grid(
            row=1, column=1, padx=10, pady=5, sticky="ew")

        # Campo para especificar el número máximo de registros a procesar
        ttk.Label(master, text="Número de registros a capturar:").grid(
            row=2, column=1, padx=10, pady=5, sticky="e")
        self.max_records_var = tk.IntVar()
        self.entry_max_records = ttk.Entry(
            master, textvariable=self.max_records_var)
        self.entry_max_records.grid(
            row=3, column=1, padx=10, pady=5, sticky="ew")
        # Valor predeterminado para hora de fin
        self.entry_max_records.insert(0, "1")

        # Campo para especificar la espera en segundos entre registros
        ttk.Label(master, text="Tempo entre registros (segundos):").grid(
            row=4, column=1, padx=10, pady=5, sticky="e")
        self.espera_var = tk.IntVar()
        self.entry_espera = ttk.Entry(
            master, textvariable=self.espera_var)
        self.entry_espera.grid(
            row=5, column=1, padx=10, pady=5, sticky="ew")
        # Valor predeterminado para hora de fin
        self.entry_espera.insert(1, "1")

        # Agregar etiqueta y campo de entrada para Hora de Inicio
        ttk.Label(master, text="Hora de Inicio (HH:MM):").grid(
            row=6, column=1, padx=10, pady=5, sticky="e")
        self.entry_hora_ini = ttk.Entry(master)
        self.entry_hora_ini.grid(row=7, column=1, padx=10, pady=5, sticky="ew")
        # Valor predeterminado para hora de inicio
        self.entry_hora_ini.insert(0, "08:00")

        # Agregar etiqueta y campo de entrada para Hora de Fin
        ttk.Label(master, text="Hora de Fin (HH:MM):").grid(
            row=8, column=1, padx=10, pady=5, sticky="e")
        self.entry_hora_fin = ttk.Entry(master)
        self.entry_hora_fin.grid(row=9, column=1, padx=10, pady=5, sticky="ew")
        # Valor predeterminado para hora de fin
        self.entry_hora_fin.insert(0, "23:59")

        # Boton iniciar automatizacion
        self.automation_button = ttk.Button(
            master, text="Iniciar Automatización", state='disabled', command=self.start_automation)
        self.automation_button.grid(
            row=10, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        # Agregar etiquetas para el resumen
        self.label_procesados = ttk.Label(master, text="", background='white')
        self.label_procesados.grid(
            row=11, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

        self.label_automation_time = ttk.Label(
            master, text="", background='white')
        self.label_automation_time.grid(
            row=12, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=3)

        self.selected_user = None
        self.selected_password = None

    def load_districts(self):
        """
        Carga los distritos en el menú desplegable.
        """
        districts = self.db_processor.fetch_districts()
        menu = self.optionmenu_district['menu']
        menu.delete(0, 'end')
        for district in districts:
            menu.add_command(label=district['distrito'],
                             command=lambda value=district['distrito']: self.district_var.set(value))
        self.district_var.set("Selecciona un Distrito")

    def district_selected(self, *args):
        """
        Called when a district is selected. Loads the users of the selected district.
        """
        district = self.district_var.get()
        if district and district != "Selecciona un Distrito":
            users = self.db_processor.fetch_users_by_district(district)
            menu = self.optionmenu_user['menu']
            menu.delete(0, 'end')
            for user in users:
                menu.add_command(label=user['nombre_completo'],
                                 command=lambda value=user: self.user_selected(value))
            self.user_var.set("Selecciona un Usuario")
        else:
            # Limpia el menú de usuarios si no se selecciona ningún distrito
            self.user_var.set("Selecciona un Usuario")
            self.optionmenu_user['menu'].delete(0, 'end')
            self.verificar_datos_completos()

    def user_selected(self, user):
        """
        Called when a user is selected. Configures the user and password for use.
        """
        self.selected_user = user['usuario']
        self.selected_password = user['contrasena']
        # Aquí puedes usar self.selected_user y self.selected_password para la automatización
        # Actualizar la variable StringVar con el nombre completo del usuario seleccionado
        self.user_var.set(user['nombre_completo'])
        self.verificar_datos_completos()

    def verificar_datos_completos(self, *args):
        # Verifica si los campos requeridos están completos
        usuario_seleccionado = self.user_var.get() != "Selecciona un Usuario"

        if usuario_seleccionado:
            self.automation_button.config(state='normal')
        else:
            self.automation_button.config(state='disabled')

    def start_automation(self):
        # Deshabilitar el botón al inicio de la automatización
        self.automation_button.grid_remove()

        usuario = self.selected_user
        contrasena = self.selected_password
        distrito = self.district_var.get()
        max_records = self.max_records_var.get()
        start_time = datetime.now()
        espera = self.espera_var.get()
        records_processed = 0
        resumen = {
            'registros_procesados': 0,
            'registros_capturados': 0,
            'registros_omitidos': 0,
            'registros_duplicado': 0,
            'registros_sirena': 0,
            'registros_error': 0
        }
        # Obtener y validar las horas de inicio y fin
        try:
            hora_ini = datetime.strptime(
                self.entry_hora_ini.get(), "%H:%M").time()
            hora_fin = datetime.strptime(
                self.entry_hora_fin.get(), "%H:%M").time()
        except ValueError:
            self.automation_button.grid()
            messagebox.showerror("Error de Formato de Hora",
                                 "La hora debe estar en formato HH:MM.")
            return

        # Asegurarse de que la hora de inicio es menor que la hora de fin
        if hora_ini >= hora_fin:
            self.automation_button.grid()
            messagebox.showerror(
                "Error en Horas", "La hora de inicio debe ser menor que la hora de fin.")
            return

        # Asegúrate de especificar las rutas correctas para tu chromedriver y chrome.exe
        directorio_actual = os.getcwd()
        chrome_driver_path = os.path.join(
            directorio_actual, "env", "chromedriver", "chromedriver.exe")
        chrome_binary_path = os.path.join(
            directorio_actual, "env", "chrome", "chrome.exe")

        threading.Thread(target=self.run_automation, args=(
            usuario, contrasena, max_records, start_time, records_processed, resumen, espera, hora_ini, hora_fin, distrito, chrome_driver_path, chrome_binary_path), daemon=True).start()

    def run_automation(self, usuario, contrasena, max_records, start_time, records_processed, resumen, espera, hora_ini, hora_fin, distrito, chrome_driver_path, chrome_binary_path):
        try:
            main(usuario, contrasena, distrito, max_records, start_time, records_processed, resumen, espera, hora_ini, hora_fin, chrome_driver_path,
                 chrome_binary_path, self.db_processor, self.update_ui_callback)
        except Exception as e:
            print(f"Error en la automatización: {e}")
        finally:
            # Reactivar el botón una vez finalizada la automatización
            self.master.after(0, self.reactivate_automation_button)

    def reactivate_automation_button(self):
        # Reactivar el botón de automatización
        self.automation_button.grid()

    def update_ui_callback(self, resumen, start_time, end_time, total_time, average_record_time, mensaje_salida):
        # Actualizar etiquetas con el resumen
        self.label_procesados.config(text=f"Registros Procesados: {resumen['registros_procesados']}\nRegistros Capturados: {resumen['registros_capturados']}\nRegistros Omitidos: {
                                     resumen['registros_omitidos']}\n   Registros Duplicados: {resumen['registros_duplicado']}\n   Registros Previos en Sirena: {resumen['registros_sirena']}\n   Registros con otros Errores: {resumen['registros_error']}")
        self.label_automation_time.config(text=f"Hora de inicio: {start_time.strftime(
            '%H:%M:%S')}\nHora de finalización: {end_time.strftime('%H:%M:%S')}\nDuración total: {str(total_time)}\nTiempo promedio por Registro: {str(average_record_time)}\n\n {mensaje_salida}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.verificar_datos_completos()  # Inicializa el estado del botón de automatización
    root.mainloop()
