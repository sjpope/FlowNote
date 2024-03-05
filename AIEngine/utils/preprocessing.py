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

# Notes is a list of strings here...may need to adjust this.
# processed_notes = [preprocess_text(note) for note in notes] 
