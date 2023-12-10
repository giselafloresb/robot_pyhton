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
        style.configure('TMenubutton', background='white',
                        foreground=guinda_color)

        style.map('TButton', background=[
                  ('active', guinda_color)], foreground=[('active', 'white')])

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
        self.optionmenu_district = ttk.OptionMenu(
            master, self.district_var, "Selecciona un Distrito", *[str(i) for i in range(1, 9)])
        self.optionmenu_district.grid(
            row=2, column=1, padx=10, pady=5, sticky="ew")

        self.file_name_label = ttk.Label(
            master, text="Ningún archivo seleccionado", background='white')
        self.file_name_label.grid(
            row=3, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

        self.button_load = ttk.Button(
            master, text="Cargar Archivo Excel", command=self.load_file)
        self.button_load.grid(row=4, column=0, padx=10,
                              pady=10, sticky="ew", columnspan=2)

        self.button_start = ttk.Button(
            master, text="Iniciar Validación", state='disabled', command=self.start_validation)
        self.button_start.grid(row=5, column=0, padx=10,
                               pady=10, sticky="ew", columnspan=2)

        self.progress = ttk.Progressbar(
            master, orient='horizontal', length=200, mode='indeterminate')
        self.progress.grid(row=6, column=0, padx=10, pady=5,
                           sticky="ew", columnspan=2)

        self.result_label = ttk.Label(master, text="", background='white')
        self.result_label.grid(row=7, column=0, padx=10,
                               pady=5, sticky="ew", columnspan=2)

        self.download_button = ttk.Button(
            master, text="Descargar Registros Inválidos", state='disabled', command=self.download_invalid_records)
        self.download_button.grid(
            row=8, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=3)

    def load_file(self):
        user = self.entry_user.get()
        password = self.entry_password.get()
        district = self.district_var.get()

        if not user or not password:
            messagebox.showerror(
                "Campos Requeridos", "Por favor, complete los campos de usuario y contraseña.")
            return

        if district == "Selecciona un Distrito":
            messagebox.showerror("Distrito Requerido",
                                 "Por favor, selecciona un distrito.")
            return

        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo Excel", filetypes=[("Excel files", "*.xlsx;*.xls")])

        if file_path:
            self.file_name_label.config(text="Cargando archivo...")
            self.progress.start(10)
            threading.Thread(target=self.load_excel, args=(
                file_path,), daemon=True).start()
            self.show_download_button()

    def show_download_button(self):
        self.button_start.config(state='normal')

    def load_excel(self, file_path):
        user = self.entry_user.get()
        password = self.entry_password.get()
        district = self.district_var.get()

        # Ruta actualizada al archivo CSV
        secciones_csv_path = 'data/secciones_distritos.csv'
        self.excel_processor = ExcelProcessor(
            file_path, district, secciones_csv_path)
        loaded, message = self.excel_processor.load_excel()

        self.progress.stop()
        if loaded:
            self.master.after(0, lambda: self.file_name_label.config(
                text=f"Archivo cargado: {file_path.split('/')[-1]}"))

    def start_validation(self):
        valid, message = self.excel_processor.validate_columns()
        if not valid:
            messagebox.showerror("Error en el archivo", message)
            return

        count_invalid_records = self.excel_processor.validate_records()
        total_invalid = count_invalid_records
        total_valid = len(self.excel_processor.df) - total_invalid

        # Actualizar la etiqueta de resultados con la cantidad de registros válidos e inválidos
        if total_invalid > 0:
            self.result_label.config(text=f"Registros válidos: {
                                     total_valid}\nRegistros inválidos: {total_invalid}")
            self.download_button.config(state='normal')
        else:
            self.result_label.config(
                text=f"Todos los registros son válidos. Total registros: {total_valid}")
            self.download_button.config(state='disabled')

    def download_invalid_records(self):
        # Pedir al usuario que elija dónde guardar el archivo de registros eliminados
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar registros eliminados como"
        )
        if filepath:
            # Guardar los registros eliminados en la ubicación seleccionada
            try:
                self.excel_processor.removed_records.to_excel(
                    filepath, index=False)
                messagebox.showinfo(
                    "Guardar archivo", f"Registros eliminados guardados exitosamente en {filepath}")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Ocurrió un error al guardar el archivo: {e}")

    def download_corrected_records(self):
        # Pedir al usuario que elija dónde guardar el archivo de registros corregidos
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar registros corregidos como"
        )
        if filepath:
            # Guardar los registros corregidos en la ubicación seleccionada
            try:
                self.excel_processor.df.to_excel(filepath, index=False)
                messagebox.showinfo(
                    "Guardar archivo", f"Registros corregidos guardados exitosamente en {filepath}")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Ocurrió un error al guardar el archivo: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
