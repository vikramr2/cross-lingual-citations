import pandas as pd
from langdetect import detect as langdetect_detect, LangDetectException, detect_langs
from pandarallel import pandarallel

# Initialize pandarallel
pandarallel.initialize(progress_bar=False, nb_workers=16)

def detect_language_with_confidence(text):
    # text = str(text)
    try:
        detections = detect_langs(text)
        if detections:
            most_likely_language = detections[0]
            lang = most_likely_language.lang
            confidence = most_likely_language.prob
            return lang, confidence
    except Exception as e:
        return None, 0

# Example CSV containing paper titles
df = pd.read_csv('ocmeta_last_5yrs.csv')

# Apply the function in parallel
df[['detected_language', 'confidence']] = df['title'].parallel_apply(
    lambda x: pd.Series(detect_language_with_confidence(x))
)

df.to_csv('ocmeta_last_5yrs_langdetect_probs.csv')
