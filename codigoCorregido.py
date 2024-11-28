import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carga de datos
model = pd.read_csv(
    r"model.txt", sep=r'\s+', skiprows=3, index_col=False)

# Crear columna de timestamp y establecer como índice
model['Timestamp'] = pd.to_datetime(model.iloc[:, 0] + ' ' + model.iloc[:, 1])
model.set_index('Timestamp', inplace=True)

# Primeras filas del dataset
print(model.head())

# Matriz de dispersión
pd.plotting.scatter_matrix(model.loc[model.index[:1000], 'M(m/s)':'D(deg)'])
pd.plotting.scatter_matrix(
    model.loc[model.sort_values('M(m/s)', ascending=False).index[:1000], 'M(m/s)':'D(deg)'])

# Histograma
model.loc[:, 'M(m/s)'].plot.hist(bins=np.arange(0, 35))

# Agregar columnas de mes y año
model['month'] = model.index.month
model['year'] = model.index.year

# Promedio agrupado
monthly = model.groupby(by=['year', 'month']).mean()
monthly['ma'] = monthly['M(m/s)'].rolling(5, center=True).mean()

# Gráficos
monthly.loc[:, ['M(m/s)', 'ma']].plot(figsize=(15, 6))
monthly.loc[:, 'M(m/s)'].reset_index().pivot(index='year', columns='month').T.loc['M(m/s)'].plot(figsize=(15, 5), legend=False)
