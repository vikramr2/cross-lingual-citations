from py3langid.langid import LanguageIdentifier, MODEL_FILE

def detect_language_with_probability(line):  
    identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True) 
    lang, prob = identifier.classify(line)
    return lang, prob

# Example usage
text = "This is an example text."
language, probability = detect_language_with_probability(text)
print(f"Detected language: {language}, Probability: {probability}")
