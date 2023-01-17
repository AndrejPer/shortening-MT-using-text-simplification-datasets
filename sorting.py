import pandas as pd

# Read the input file into a Pandas dataframe
df = pd.read_csv("relabeled_ppdb_small.csv", delimiter='\|\|\|', engine='python')

# Sort the dataframe by the value of the fifth field in ascending order
df = df.sort_values(by=df.columns[4])

# Write the sorted dataframe to the output file one line at a time
df.to_csv("sorted_ppdb_small.csv", sep='|', index=False)
