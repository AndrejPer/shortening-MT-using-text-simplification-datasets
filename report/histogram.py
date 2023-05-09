import pandas as pd
import numpy as np

column_names = ['Tag', 'Longer', 'Shorter', 'Score', 'Ratio', 'Equivalence']
df = pd.read_csv("../sorted_ppdb_small.csv", delimiter='\|', engine='python')
df = df.drop_duplicates()
print(df['Ratio'])

#ratios = [ratio for ratio in df['Ratio']]
ratios = df['Ratio'].to_numpy()
print(ratios[7000:7007])

import matplotlib.pyplot as plt

bins = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05]
hist, bins = np.histogram(ratios, bins=bins)
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width)
plt.show()
