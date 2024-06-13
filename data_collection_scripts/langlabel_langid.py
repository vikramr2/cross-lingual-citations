import pandas as pd
from py3langid.langid import LanguageIdentifier, MODEL_FILE


# Initialize the model
identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)

def detect_language_with_probability(line):
    try: 
        lang, prob = identifier.classify(line)
        return lang, prob
    except:
        return None, 0

# Example CSV containing paper titles
df = pd.read_csv('ocmeta_last_5yrs.csv')

# Apply the function in parallel
df[['detected_language', 'confidence']] = df['title'].apply(
    lambda x: pd.Series(detect_language_with_probability(x))
)

df.to_csv('ocmeta_last_5yrs_langid_probs.csv')
