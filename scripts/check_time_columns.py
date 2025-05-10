import pandas as pd

# Leer el archivo
df = pd.read_csv('data/clean/encoded_data.csv')

# Buscar columnas relacionadas con tiempo
time_related_cols = [col for col in df.columns if any(time_word in col.lower() 
                    for time_word in ['year', 'time', 'duration', 'period'])]

print("Columnas relacionadas con tiempo disponibles:")
for col in time_related_cols:
    print(f"- {col}") 