import os

# Ruta base del proyecto (SCORE/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas relativas a partir de la base
DATA_DIR = os.path.join(BASE_DIR, "calibration_data")
CODE_DIR = os.path.join(BASE_DIR, "calibration_code")
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")

# Función para obtener la ruta de un archivo en calibration_data
def get_data_path(filename):
    return os.path.join(DATA_DIR, filename)

# Función para obtener la ruta de un módulo en calibration_code
def get_code_path(filename):
    return os.path.join(CODE_DIR, filename)

# Función para obtener la ruta de un notebook en notebooks/
def get_notebook_path(folder, filename):
    return os.path.join(NOTEBOOKS_DIR, folder, filename)
