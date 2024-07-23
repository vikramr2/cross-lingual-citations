import pandas as pd
from datetime import datetime

# Print the date and time of run
current_datetime = datetime.now()
print(f"Run Date and Time: {current_datetime}")

# Load the CSV files
oa_df = pd.read_csv("../data/cleaned/oc_openalex_langdata.csv")
cr_df = pd.read_csv("../data/cleaned/oc_crossref_langdata.csv")

# Merge the DataFrames on the common identifier 'doi'
merged_df = pd.merge(oa_df, cr_df[['doi', 'language']], on='doi', how='left', suffixes=('_oa', '_cr'))

# Filter out entries where either oa_df's or cr_df's language tag is missing
filtered_merged_df = merged_df[merged_df['language_oa'].notna() & merged_df['language_cr'].notna()]

# Calculate the percentage of matching language tags
matching_tags = filtered_merged_df['language_oa'] == filtered_merged_df['language_cr']
percent_matching = matching_tags.mean() * 100
print(f"Percentage of matching language tags: {percent_matching:.2f}%")
print(f"Expressed as a fraction: {matching_tags.sum()}/{matching_tags.count()}")

# Display a few mismatched tags
mismatched_tags = filtered_merged_df[~matching_tags]
print("Mismatched language tags (sample):")
print(mismatched_tags[['doi', 'language_oa', 'language_cr']].head())

# Replace oa_df's language tags with cr_df's language tags if they exist in cr_df
oa_df.set_index('doi', inplace=True)
cr_df.set_index('doi', inplace=True)
oa_df.update(cr_df[['language']])
oa_df.reset_index(inplace=True)

# Save the updated oa_df back to CSV if needed
oa_df.to_csv("../data/cleaned/oc_corroborated_langdata.csv", index=False)

# Display the updated DataFrame
print("Updated oa_df (sample):")
print(oa_df.head())
