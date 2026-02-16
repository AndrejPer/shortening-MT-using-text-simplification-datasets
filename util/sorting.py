import pandas as pd

print('start')
column_names = ['Tag', 'Longer', 'Shorter', 'Score', 'Ratio', 'Equivalence']
print('star')
df = pd.read_csv("../relabeled_ppdb/relabeled_ppdb_xxl_lexical.csv", delimiter=' \|\|\| ', engine='python', names=column_names)
# dropping duplicates
print('or')
df = df.drop_duplicates()
#print(df)

# sort the dataframe by the value of the fifth field in ascending order
df = df.sort_values(by=df.columns[4])

# dropping duplicates based on Longer column
# keeping only the rule that shrinks the Longer the most, first appearance
# df = df.drop_duplicates(subset=['Longer'])
df = df.drop_duplicates()
# duplicate_values = df[df["Longer"].duplicated(keep=False)]["Longer"].unique()
# print(duplicate_values[:20])


#print(df)

# keep only the pairs with equivalence entailment
df = df[df['Equivalence'] == 'Equivalence']
print(df)

df.to_csv("../sorted_ppdb/sorted_ppdb_xxl_lexical.csv", sep='|', index=False, )

# df = df[df['Longer'].strip() != df['Shorter'].strip() + 'ing']
# drop rows where "Longer" is the concatenation of "Shorter" and 's'
df = df[~(df["Longer"] == df["Shorter"] + "s")]
print("here")
df = df[df['Ratio'] < 1.0]
print('there')



df.to_csv("../sorted_ppdb/actual_ppdb_xxl_lexical.csv", sep='|', index=False, )
