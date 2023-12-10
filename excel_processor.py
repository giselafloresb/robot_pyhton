import pandas as pd


class ExcelProcessor:
    def __init__(self, file_path, district, secciones_csv_path):
        self.file_path = file_path
        self.district = district
        self.secciones_df = self.load_secciones_df(secciones_csv_path)
        self.df = None

    def load_secciones_df(self, secciones_csv_path):
        # Leer el archivo CSV de secciones
        secciones_df = pd.read_csv(secciones_csv_path)
        return secciones_df

    def load_excel(self):
        try:
            self.df = pd.read_excel(self.file_path)
            return True, "Archivo cargado correctamente."
        except Exception as e:
            return False, f"Ha ocurrido un error al cargar el archivo: {e}"

    def validate_columns(self):
        required_columns = ['Nombre', 'Paterno', 'Materno', 'Telefono',
                            'Calle', 'Num', 'Colonia', 'CP', 'CVE_ELEC', 'Municipio', 'Seccion']
        missing_columns = [
            col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            return False, f"Faltan las siguientes columnas: {', '.join(missing_columns)}"
        return True, "Todas las columnas requeridas están presentes."

    def validate_records(self):
        self.df['Error'], self.df['Paterno'], self.df['Materno'] = zip(
            *self.df.apply(self.validate_record, axis=1))
        # Contar los registros inválidos como aquellos que tienen un mensaje de error no vacío
        count_invalid_records = self.df['Error'].apply(lambda x: x != "").sum()
        return count_invalid_records

    def validate_record(self, record):
        errors = []

        if pd.isnull(record['Nombre']):
            errors.append("El campo 'Nombre' no puede estar vacío.")

        # Convertir y validar 'Telefono' si no está vacío
        if not pd.isnull(record['Telefono']):
            telefono_str = str(int(record['Telefono'])) if isinstance(
                record['Telefono'], float) else str(record['Telefono'])
            if len(telefono_str) != 10:
                errors.append(
                    "El campo 'Telefono' debe contener 10 dígitos exactos.")

        # Convertir y validar 'CP' si no está vacío
        if not pd.isnull(record['CP']):
            cp_str = str(int(record['CP'])) if isinstance(
                record['CP'], float) else str(record['CP'])
            if len(cp_str) != 5:
                errors.append("El campo 'CP' debe contener 5 dígitos exactos.")

        # Validación de apellidos
        paterno = record['Paterno'] if pd.notnull(record['Paterno']) else ""
        materno = record['Materno'] if pd.notnull(record['Materno']) else ""
        if not paterno and not materno:
            errors.append(
                "Al menos uno de los campos 'Paterno' o 'Materno' debe estar presente.")
        else:
            if not paterno:
                paterno = 'X'
            if not materno:
                materno = 'X'

        if not self.is_section_valid(record['Seccion']):
            errors.append("La Sección no pertenece al Distrito seleccionado.")

        error_message = " | ".join(errors)
        return error_message, paterno, materno

    def is_section_valid(self, section):
        try:
            section_int = int(section)
            district_int = int(self.district)
            valid_sections = self.secciones_df[self.secciones_df['DIST_FED']
                                               == district_int]['SECCION'].tolist()
            return section_int in valid_sections
        except ValueError:
            return False
