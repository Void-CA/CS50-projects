import pandas as pd

df = pd.read_csv('shopping.csv')
df['Administrative'] = df['Administrative'].astype(int)
print(df.shape[0])
print(df['Revenue'].values)