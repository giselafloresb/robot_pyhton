# excel_processor.py

import pandas as pd
import json

class ExcelProcessor:
    def __init__(self, file_path, district, secciones_json_path):
        self.file_path = file_path
        self.district = district
        with open(secciones_json_path, 'r') as file:
            self.secciones_distritos = json.load(file)
        self.df = None

    def load_excel(self):
        try:
            self.df = pd.read_excel(self.file_path)
            # Llenar 'Paterno' o 'Materno' con 'X' si están vacíos
            self.df['Paterno'] = self.df['Paterno'].fillna('X')
            self.df['Materno'] = self.df['Materno'].fillna('X')
            # Agregar la columna 'Error'
            self.df['Error'] = ""
            return True, "Archivo cargado correctamente."
        except Exception as e:
            return False, f"Ha ocurrido un error al cargar el archivo: {e}"

    def validate_columns(self):
        required_columns = ['Nombre', 'Paterno', 'Materno', 'Telefono', 'Calle', 'Num', 'Colonia', 'CP', 'CVE_ELEC', 'Municipio', 'Seccion']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            return False, f"Faltan las siguientes columnas: {', '.join(missing_columns)}"
        return True, "Todas las columnas requeridas están presentes."

    def validate_records(self):
        self.df['Valid'] = self.df.apply(self.validate_record, axis=1)
        invalid_records = self.df[~self.df['Valid']]
        # Actualizar la columna 'Error' con los mensajes de error
        self.df['Error'] = invalid_records['Error'].values
        return invalid_records

    def validate_record(self, record):
        # Verificar que el Nombre no esté vacío y que al menos uno de Paterno o Materno esté presente
        if pd.isnull(record['Nombre']):
            record['Error'] = "El campo 'Nombre' no puede estar vacío."
            return False
        # Verificar que CP sea vacío o tenga 5 dígitos
        if not pd.isnull(record['CP']) and len(str(record['CP'])) != 5:
            record['Error'] = "El campo 'CP' debe estar vacío o contener 5 dígitos exactos."
            return False
        # Verificar que el Teléfono sea vacío o tenga 10 dígitos
        if not pd.isnull(record['Telefono']) and len(str(record['Telefono'])) != 10:
            record['Error'] = "El campo 'Telefono' debe estar vacío o contener 10 dígitos exactos."
            return False
        # Verificar que la Sección pertenezca al Distrito definido
        if not self.is_section_valid(record['Seccion']):
            record['Error'] = "La Sección no pertenece al Distrito seleccionado."
            return False
        return True

    def is_section_valid(self, section):
        return self.secciones_distritos.get(str(section)) == self.district
