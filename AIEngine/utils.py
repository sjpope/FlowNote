import re
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    doc = nlp(text)
    lemmatized = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return " ".join(lemmatized)

def strip_html_tags(input_string):
    html_tag_pattern = re.compile('<.*?>')
    return html_tag_pattern.sub('', input_string)

def remove_prompt_from_content(prompt, content):
    try:
        start_index = content.index(prompt) + len(prompt)
    except ValueError:
        start_index = 0
    return content[start_index:].strip()

def preprocess_and_extract_keywords(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word not in stop_words]
    return keywords
