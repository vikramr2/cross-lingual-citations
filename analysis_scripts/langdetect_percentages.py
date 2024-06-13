import pandas as pd
from collections import Counter

df = pd.read_csv('ocmeta_last_5yrs_langtag.csv')

# Calculate the percentage of each occurrence in the 'fruits' column
percentages = df['langdetect'].value_counts(normalize=True) * 100

# Print the results
print(percentages)
