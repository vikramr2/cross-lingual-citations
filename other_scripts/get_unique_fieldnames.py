import pandas as pd

df = pd.read_csv('../data/cleaned/oc_corroborated_langdata.csv')

field = df['field'].unique()
subfield = df['subfield'].unique()

print(f'oa_corroborated_langdata.csv unique fields: {len(field)}')
print(f'oa_corroborated_langdata.csv unique subfields: {len(subfield)}')
