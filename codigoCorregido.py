import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
import matplotlib as mpl


model = pd.read_csv(
    r"model.txt", sep='\s+', skiprows = 3,
    parse_dates = {'Timestamp': [0, 1]}, index_col = 'Timestamp')

model.head()

pd.plotting.scatter_matrix(model.loc[model.index[:1000], 'M(m/s)':'D(deg)'])
pd.plotting.scatter_matrix(model.loc[model.sort_values('M(m/s)', ascending=False).index[:1000],'M(m/s)':'D(deg)'])

model.loc[:, 'M(m/s)'].plot.hist(bins=np.arange(0, 35))
model['month'] = model.index.month
model['year'] = model.index.year

model.groupby(by = ['year', 'month']).mean().head(24)

model.groupby(by=['year', 'month']).mean().plot(y='M(m/s)', figsize=(15, 5))

monthly = model.groupby(by=['year', 'month']).mean()
monthly['ma'] = monthly.loc[:, 'M(m/s)'].rolling(5, center=True).mean()
monthly.head()


monthly.loc[:, ['M(m/s)', 'ma']].plot(figsize=(15, 6))

monthly.loc[:, 'M(m/s)'].reset_index().pivot(index='year', columns='month')

monthly.loc[:, 'M(m/s)'].reset_index().pivot(index='year', columns='month').T.loc['M(m/s)'].plot(figsize=(15, 5), legend=False)
