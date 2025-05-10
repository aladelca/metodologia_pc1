import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_categorical_analysis(df, column):
    """
    Función para analizar y visualizar la relación entre variables categóricas y attrition.
    Soporta tanto variables categóricas normales como variables dummy codificadas.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        column (str): Nombre de la columna categórica a analizar
    """
    plt.figure(figsize=(12, 6))
    
    # Verificar si la columna está codificada como dummy
    if column not in df.columns:
        # Buscar columnas dummy relacionadas
        dummy_cols = [col for col in df.columns if col.startswith(f"{column}_")]
        if not dummy_cols:
            raise ValueError(f"No se encontraron columnas relacionadas con {column}")
            
        # Reconstruir la variable categórica original
        categories = []
        for idx, row in df[dummy_cols].iterrows():
            cat = next((col.replace(f"{column}_", "") for col, val in row.items() if val == 1), None)
            categories.append(cat)
        
        # Crear una serie temporal con la categoría reconstruida
        temp_series = pd.Series(categories, index=df.index)
        
        # Calcular porcentajes de Attrition por categoría
        attrition_by_cat = pd.crosstab(temp_series, df['Attrition'], normalize='index') * 100
    else:
        # Si la columna existe, usar el código original
        attrition_by_cat = pd.crosstab(df[column], df['Attrition'], normalize='index') * 100
    
    # Crear gráfico usando seaborn
    sns.barplot(x=attrition_by_cat.index, y=attrition_by_cat[1])
    plt.title(f'Porcentaje de Attrition por {column}')
    plt.ylabel('Porcentaje de Attrition')
    plt.xlabel(column)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    print(f'\nPorcentaje de Attrition por {column}:')
    print(attrition_by_cat[1].sort_values(ascending=False)) 