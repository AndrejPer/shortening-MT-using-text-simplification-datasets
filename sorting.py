import pandas as pd

column_names = ['Tag', 'Longer', 'Shorter', 'Score', 'Ratio', 'Equivalence']
df = pd.read_csv("relabeled_ppdb_small.csv", delimiter=' \|\|\| ', engine='python', names=column_names)
df = df.drop_duplicates()
print(df)

# Sort the dataframe by the value of the fifth field in ascending order
df = df.sort_values(by=df.columns[4])
print(df)
df = df[df['Equivalence'] == 'Equivalence']
print(df)

df.to_csv("sorted_ppdb_small.csv", sep='|', index=False, )
