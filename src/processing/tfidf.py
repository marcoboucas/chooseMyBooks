"""Use of the PCA to visualize the books."""

from sklearn.feature_extraction.text import TfidfVectorizer

from src.utils.stopwords import STOPWORDS


def vectorize_tfidf(library):
    """Vectorize the data from the library."""

    vectorizer = TfidfVectorizer(
        strip_accents="ascii",
        lowercase=True,
        analyzer="char",
        stop_words=STOPWORDS,
        ngram_range=(3, 6),
        max_df=1.0,
        min_df=0.0,
        max_features=None
    )

    vectors = vectorizer.fit_transform(library['description'])
    return vectors


if __name__ == "__main__":
    from ..library.library import Library
    import os
    library = Library(os.getenv('apiKey'))
    vectorize_tfidf(library.library)
