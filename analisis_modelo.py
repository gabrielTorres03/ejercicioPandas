import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar los datos del archivo model.txt
model = pd.read_csv(
    "model.txt", 
    delim_whitespace=True, 
    skiprows=3, 
    parse_dates={'Timestamp': [0, 1]}, 
    index_col='Timestamp'
)

# Mostrar las primeras filas del DataFrame
print("Primeras filas del DataFrame:")
print(model.head())

# Scatter matrix para los primeros 1000 registros
pd.plotting.scatter_matrix(
    model.loc[model.index[:1000], 'M(m/s)':'D(deg)'], 
    figsize=(10, 10)
)
plt.suptitle("Scatter Matrix - Primeros 1000 Registros")
plt.show()

# Scatter matrix ordenado por 'M(m/s)'
pd.plotting.scatter_matrix(
    model.loc[model.sort_values('M(m/s)', ascending=False).index[:1000], 'M(m/s)':'D(deg)'],
    figsize=(10, 10)
)
plt.suptitle("Scatter Matrix - Ordenado por 'M(m/s)'")
plt.show()

# Histograma de la columna 'M(m/s)'
model['M(m/s)'].plot.hist(bins=np.arange(0, 35), color='blue', alpha=0.7)
plt.title("Histograma de 'M(m/s)'")
plt.xlabel("M(m/s)")
plt.ylabel("Frecuencia")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Agregar columnas 'month' y 'year'
model['month'] = model.index.month
model['year'] = model.index.year

# Agrupación por año y mes, y calcular promedios
monthly = model.groupby(by=['year', 'month']).mean()
print("Promedios agrupados por año y mes:")
print(monthly.head())

# Promedios mensuales con Media Móvil (Moving Average)
monthly['ma'] = monthly['M(m/s)'].rolling(5, center=True).mean()

# Visualización de los promedios mensuales y la media móvil
monthly.loc[:, ['M(m/s)', 'ma']].plot(figsize=(15, 6))
plt.title("Promedio Mensual y Media Móvil de 'M(m/s)'")
plt.xlabel("Tiempo (Año-Mes)")
plt.ylabel("Velocidad M(m/s)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(['Promedio Mensual', 'Media Móvil'])
plt.show()

# Pivotar datos para obtener una vista por año y mes
pivot = monthly.loc[:, 'M(m/s)'].reset_index().pivot(index='year', columns='month')
print("Datos Pivotados (Año vs Mes):")
print(pivot)

# Visualización de los datos pivotados
pivot.T.plot(
    figsize=(15, 5), legend=False, cmap='viridis'
)
plt.title("Datos Pivotados por Año y Mes - 'M(m/s)'")
plt.xlabel("Mes")
plt.ylabel("Velocidad Media (M/m/s)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
