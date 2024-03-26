import spacy

nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    doc = nlp(text)
    result = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        result.append(token.lemma_)
    return " ".join(result)

# Use this for multiple notes (Grouping Feature)
# processed_notes = [preprocess_text(note) for note in notes] 

# Use python scripts to preprocess & clean notes
# TO-DO: Add more preprocessing steps as needed