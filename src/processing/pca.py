"""Apply PCA."""

from sklearn.decomposition import PCA

def apply_PCA(matrix, n_components: int = 2):
    """Apply PCA to a matrix."""

    pca = PCA(n_components=n_components)

    vectors = pca.fit_transform(matrix.toarray())

    return vectors


if __name__ == "__main__":
    from ..library.library import Library
    from .tfidf import vectorize_tfidf
    import os
    library = Library(os.getenv('apiKey'))
    matrix = vectorize_tfidf(library.library)
    vectors = apply_PCA(matrix)
    print(vectors)
