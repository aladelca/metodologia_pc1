"""Este módulo contiene un método para codificar las variables categoricas."""
import os
import pandas as pd

os.chdir("..")
from src.features.feedback_jefes import procesar_feedback_jefes
from src.preprocessing.config import RUTA_ENCODED_DATA
from src.preprocessing.encoding import apply_label_encoding, apply_one_hot_encoding

def encoding_variables():
  """
    Transforma las variables categóricas y crea un CSV a partir de la codificación.

    Realiza los siguientes pasos:
    1. Carga el dataset de procesar_feedback_jefes.
    2. Aplica Label Encoding a las columnas binarias.
    3. Aplica One Hot Encoding a las columnas nominales.
    4. Guarda el dataset en un archivo encoded_data.csv en la ruta data/clean.

    Returns:
      N/A
  """
  
  #Llamar al metodo procesar_feedback_jefes y asignarlo a una variable
  df_feedback_jefes = procesar_feedback_jefes()

  # Label Encoding a columnas binarias
  binary_cols = ['Attrition', 'Gender', 'Over18']
  df_encoded, label_encoders = apply_label_encoding(df_feedback_jefes, binary_cols)

  # One Hot Encoding a columnas nominales
  one_hot_cols = ['BusinessTravel', 'Department', 'EducationField', 'JobRole', 'MaritalStatus']
  df_encoded = apply_one_hot_encoding(df_encoded, one_hot_cols)

  # Guardar dataset limpio
  df_encoded.to_csv(RUTA_ENCODED_DATA, index=False)