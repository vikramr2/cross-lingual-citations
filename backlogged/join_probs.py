import pandas as pd
# from tqdm import tqdm


# Define the function to determine 'overall' and 'winner'
def determine_overall_winner(row):
    if row['langid_prob'] > row['langdetect_prob']:
        return row['langid'], 'langid'
    else:
        return row['langdetect'], 'langdetect'


# Enable the tqdm pandas integration
# tqdm.pandas()

# Read the CSV files
langid = pd.read_csv('ocmeta_last_5yrs_langid_probs.csv')
langdetect = pd.read_csv('ocmeta_last_5yrs_langdetect_probs.csv')

# Select and rename columns
langdetect = langdetect.rename(columns={
    'detected_language': 'langdetect',
    'confidence': 'langdetect_prob'
})
langid = langid[['id', 'detected_language', 'confidence']].rename(columns={
    'detected_language': 'langid',
    'confidence': 'langid_prob'
})

# Merge the DataFrames
combined = pd.merge(langdetect, langid, on='id', how='inner')

# Apply the function to the DataFrame with a progress bar
combined[['overall', 'winner']] = combined.apply(
    lambda row: pd.Series(determine_overall_winner(row)), axis=1
)

combined.to_csv('ocmeta_last_5yrs_language_combined.csv')
