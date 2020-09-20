"""Books to 2D."""

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
import umap

from .loader import LibraryLoader


class BooksTo2D(LibraryLoader):
    """Give books a representation in a 2D space."""

    library: pd.DataFrame

    def generate_2D_vectors(self):
        """Generate 2D vectors."""

        # Transform text to vector
        vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents="ascii",
            analyzer="word",
            stop_words=None,
            ngram_range=(1, 3),
            max_df=0.8,
            min_df=0.0,
            max_features=100000
        )
        vectors = vectorizer.fit_transform(self.library['description'])

        # Dimension reduction without loosing neighbors information
        reducer = umap.UMAP(
            n_neighbors=15,
            n_components=2,
            metric="euclidean",
            random_state=42,
            verbose=False,
        )
        embedding = reducer.fit_transform(vectors)

        self.library['x_pos'] = embedding[:, 0]
        self.library['y_pos'] = embedding[:, 1]

        self.save_library()
