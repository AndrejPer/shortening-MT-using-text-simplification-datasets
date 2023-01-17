import pandas as pd

df = pd.read_csv("relabeled_ppdb_small.csv", delimiter='\|\|\|', engine='python')
df = df.drop_duplicates()

# Sort the dataframe by the value of the fifth field in ascending order
df = df.sort_values(by=df.columns[4])

df.to_csv("sorted_ppdb_small.csv", sep='|', index=False)
