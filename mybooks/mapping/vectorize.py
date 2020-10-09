"""Vectorize books."""
from typing import List
import logging

import numpy as np
import umap
from sklearn.feature_extraction.text import TfidfVectorizer

MAX_FEATURES = 10000
N_NEIGHBORS = 15


def vectorize_books(books: List[str]) -> np.array:
    """Create an embedding."""
    logging.debug("Create the vectorizer")
    vectorizer = TfidfVectorizer(
        lowercase=True,
        strip_accents="ascii",
        analyzer="word",
        stop_words=None,
        ngram_range=(1, 3),
        max_df=0.8,
        min_df=0.0,
        max_features=MAX_FEATURES
    )

    logging.debug("Generate the vectors")
    vectors = vectorizer.fit_transform(books)

    logging.debug("Create the Dimension Reducer")
    reducer = umap.UMAP(
        n_neighbors=N_NEIGHBORS,
        n_components=2,
        metric="euclidean",
        random_state=42,
        verbose=False,
    )
    logging.info("Dimension Reduction ...")
    embedding = reducer.fit_transform(vectors)
    logging.info("Dimension Reduction OK")

    return embedding
