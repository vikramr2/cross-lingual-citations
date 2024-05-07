import pandas as pd

# Reading the CSV content
df = pd.read_csv('ocmeta_last_5yrs.csv')

# Adding the 'omid' column by extracting the desired part from the 'id' column
df['omid'] = df['id'].apply(lambda x: ' '.join([part for part in x.split() if part.startswith('omid:br/')]))

df.to_csv('ocmeta_last_5yrs.csv', index=False)
