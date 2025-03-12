📌 Proyecto SCORE

Este repositorio contiene código y notebooks para el análisis exploratorio de datos de crédito, con el objetivo de estudiar factores que afectan la clasificación de riesgo crediticio.

📂 Estructura del Proyecto

📂 SCORE/
│── 📂 calibration_code/          # Código para análisis y modelado
│   │── __init__.py
│   │── config.py                 # Funciones de configuración y rutas de datos
│   │── modelling_tools.py         # Funciones de análisis univariado, bivariado y multivariado
│   │── data_cleaning.py           # Funciones para limpieza de datos
│   │── utils.py                   # Funciones utilitarias
│   │── visualization_tools.py      # Funciones para visualización de datos
│
│── 📂 calibration_data/           # Datos utilizados en el análisis
│   │── Credit_score_cleaned_data.csv  # Datos originales
│
│── 📂 notebooks/                  # Notebooks organizados por análisis
│   │── 📂 0_UNIVARIATE_ANALYSIS/   # Análisis univariado 
│   │── 📂 1_BIVARIATE_ANALYSIS/    # Análisis bivariado de variables
│   │── 📂 2_MULTIVARIATE_ANALYSIS/ # Análisis multivariado (cuando corresponda)
│   │── DescripciónDatos.doc        # Documento con la descripción de los datos
│
│── 📂 venv/                        # Entorno virtual de Python
│
│── .gitignore                      # Archivos y carpetas a ignorar en Git
│── requirements.txt                 # Dependencias del proyecto
│── README.md                        # Instrucciones de uso y documentación del proyecto


⚠️ Estado Actual

Actualmente, el proyecto NO tiene un flujo de ejecución definido. En su lugar, el repositorio sirve como base para análisis de datos en notebooks.

🚀 Cómo Usar Este Repositorio

1️⃣ Clonar el repositorio:

git clone https://github.com/adoljc87/SCORE.git

cd SCORE

2️⃣ Crear y activar un entorno virtual:

python -m venv venv
venv\Scripts\activate  # En Mac/Linux: source venv/bin/activate

3️⃣ Instalar dependencias:

pip install -r requirements.txt

4️⃣ Ejecutar Jupyter Notebook:

jupyter notebook

5️⃣ Explorar los notebooks en notebooks/.

📝 Notebooks Disponibles

✅ Análisis Univariado: Explora cada variable de forma individual.
🔄 Análisis Bivariado: En proceso de desarrollo.
⏳ Análisis Multivariado: Aún no iniciado.


📊 Generación del HTML del Análisis Univariado

Para generar un archivo HTML con los resultados:

1️⃣ Activa el entorno virtual y navega a la carpeta de análisis univariado:

2️⃣ Ejecuta el notebook y conviértelo a HTML:

jupyter nbconvert --to html --execute --no-input "24_AnálisisUnivariado.ipynb"

El archivo HTML generado permitirá visualizar los resultados sin necesidad de ejecutar Jupyter Notebook.

📌 IMPORTANTE: No hay un main.py, por lo que cada análisis debe ejecutarse desde su respectivo notebook.