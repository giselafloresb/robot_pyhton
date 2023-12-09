# ui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from excel_processor import ExcelProcessor
import threading

class ErrorWindow:
    def __init__(self, master, errors):
        self.master = master
        master.title("Errores de Validación")

        self.error_text = tk.Text(master, wrap=tk.WORD)
        self.error_text.pack(fill=tk.BOTH, expand=True)

        self.error_text.insert(tk.END, "Errores de Validación:\n\n")
        for i, error in enumerate(errors, start=1):
            self.error_text.insert(tk.END, f"Registro {i}:\n{error}\n\n")

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Captura Masiva")
        master.configure(bg='white')

        style = ttk.Style()
        style.theme_use('default')

        guinda_color = '#800000'
        style.configure('TButton', background=guinda_color, foreground='white')
        style.configure('TLabel', background='white', foreground=guinda_color)
        style.configure('TEntry', fieldbackground='white', foreground='black')
        style.configure('TMenubutton', background='white', foreground=guinda_color)

        style.map('TButton', background=[('active', guinda_color)], foreground=[('active', 'white')])

        self.label_user = ttk.Label(master, text="Usuario")
        self.label_user.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.entry_user = ttk.Entry(master)
        self.entry_user.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.label_password = ttk.Label(master, text="Contraseña")
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.entry_password = ttk.Entry(master, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.label_district = ttk.Label(master, text="Distrito")
        self.label_district.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.district_var = tk.StringVar(master)
        self.district_var.set("Selecciona un Distrito")  # Valor por defecto
        self.optionmenu_district = ttk.OptionMenu(master, self.district_var, "Selecciona un Distrito", *[str(i) for i in range(1, 9)])
        self.optionmenu_district.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.file_name_label = ttk.Label(master, text="Ningún archivo seleccionado", background='white')
        self.file_name_label.grid(row=3, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

        self.button_load = ttk.Button(master, text="Cargar Archivo Excel", command=self.load_file)
        self.button_load.grid(row=4, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.button_start = ttk.Button(master, text="Iniciar Validación", state='disabled', command=self.start_validation)
        self.button_start.grid(row=5, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.progress = ttk.Progressbar(master, orient='horizontal', length=200, mode='indeterminate')
        self.progress.grid(row=6, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=3)

    def load_file(self):
        user = self.entry_user.get()
        password = self.entry_password.get()
        district = self.district_var.get()

        if not user or not password:
            messagebox.showerror("Campos Requeridos", "Por favor, complete los campos de usuario y contraseña.")
            return

        if district == "Selecciona un Distrito":
            messagebox.showerror("Distrito Requerido", "Por favor, selecciona un distrito.")
            return

        file_path = filedialog.askopenfilename(title="Selecciona un archivo Excel", filetypes=[("Excel files", "*.xlsx;*.xls")])

        if file_path:
            self.file_name_label.config(text="Cargando archivo...")
            self.progress.start(10)
            threading.Thread(target=self.load_excel, args=(file_path,), daemon=True).start()
            self.show_download_button()  # Mostrar el botón de descarga después de cargar el archivo

    def show_download_button(self):
        self.button_start.config(state='normal')

    def load_excel(self, file_path):
        user = self.entry_user.get()
        password = self.entry_password.get()
        district = self.district_var.get()
        
        secciones_json_path = 'data/secciones_distritos.json'  # Ruta actualizada al archivo JSON
        self.excel_processor = ExcelProcessor(file_path, district, secciones_json_path)
        loaded, message = self.excel_processor.load_excel()

        self.progress.stop()
        if loaded:
            self.master.after(0, lambda: self.file_name_label.config(text=f"Archivo cargado: {file_path.split('/')[-1]}"))

    def start_validation(self):
        valid, message = self.excel_processor.validate_columns()
        if not valid:
            messagebox.showerror("Error en el archivo", message)
            return

        invalid_records = self.excel_processor.validate_records()
        if not invalid_records.empty:
            # Agregar la columna 'Error' al DataFrame original con los mensajes de error
            self.excel_processor.df['Error'] = invalid_records['Error'].values
            # Guardar el DataFrame con la columna de errores en un nuevo archivo Excel
            error_file_path = "registros_con_errores.xlsx"
            self.excel_processor.df.to_excel(error_file_path, index=False)
            # Crear un mensaje con la liga de descarga
            message_with_link = f"Se han encontrado registros con errores. Puede descargar el archivo con los registros y mensajes de error en [este enlace]({error_file_path})."
            messagebox.showinfo("Validación", message_with_link, icon='info')
            self.show_download_button()  # Mostrar el botón de descarga después de la ventana de alerta
        else:
            messagebox.showinfo("Validación", "Todos los registros son válidos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
