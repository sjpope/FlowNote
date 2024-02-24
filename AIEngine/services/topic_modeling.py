# Holds the logic for topic modeling, including training, updating, and utilizing topic models.

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from AIEngine.utils.preprocessing import preprocess_text

def perform_topic_modeling(notes):
    """Performs topic modeling on the provided notes."""
    processed_notes = [preprocess_text(note) for note in notes]

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(processed_notes)

    lda = LatentDirichletAllocation(n_components=5)  # Adjust n_components as needed
    lda.fit(X)

    feature_names = vectorizer.get_feature_names_out()
    for topic_idx, topic in enumerate(lda.components_):
        print(f"Topic #{topic_idx}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]))
