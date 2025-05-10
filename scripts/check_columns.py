import pandas as pd

# Leer el archivo
df = pd.read_csv('data/clean/encoded_data.csv')

# Imprimir las columnas
print("Columnas disponibles:")
print(df.columns.tolist()) 