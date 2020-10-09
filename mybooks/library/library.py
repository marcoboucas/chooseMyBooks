"""
Library class for books.
"""

from typing import Optional, List
import os
import logging

import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree
from sklearn.feature_extraction.text import TfidfVectorizer
import umap
import matplotlib
import matplotlib.pyplot as plt


from .api_caller import APICaller


class Library(APICaller):
    """Library Object."""

    finder: KDTree

    def __init__(
        self,
        api_key: Optional[str] = None,
        file: str = "./library.csv"
    ):
        """Init."""
        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('API_KEY', "")
        self.file = file
        self.load_library()

    def load_library(self):
        """Load library."""
        try:
            self.library = pd.read_csv(self.file)
            self.library = self.library[~self.library['description'].isna()]
        except:
            self.library = pd.DataFrame()
        self.compute_values()

    def save_library(self):
        """Save library."""
        self.library.to_csv(self.file, index=False)

    def generate_2d_vectors(
        self,
        max_features: int = 100000,
        n_neighbors: int = 15
    ):
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
            max_features=max_features
        )
        logging.info("Vectorization ...")
        vectors = vectorizer.fit_transform(self.library['description'])
        logging.info("Vectorization OK")

        # Dimension reduction without loosing neighbors information
        reducer = umap.UMAP(
            n_neighbors=n_neighbors,
            n_components=2,
            metric="euclidean",
            random_state=42,
            verbose=False,
        )
        logging.info("Dimension Reduction ...")
        embedding = reducer.fit_transform(vectors)
        logging.info("Dimension Reduction OK")

        # Get coordinates
        self.library['x_pos'] = embedding[:, 0]
        self.library['y_pos'] = embedding[:, 1]

        logging.info("Generate colors ...")
        # Generate colors
        self.library['author'] = self.library['authors'].apply(lambda x: x[0])

        # Give a color per author
        authors_names = self.library['author'].unique().tolist()
        colors = plt.cm.get_cmap("hsv", len(authors_names))
        author_to_color = {
            authors_names[i]: matplotlib.colors.to_hex(colors(i))
            for i in range(len(authors_names))
        }
        self.library['color'] = self.library['author'].apply(lambda x: author_to_color[x])

        # Create the Nearest Neighbors finder
        logging.info("Create the NearestNeighbors finder ...")
        self.generate_finder()

        self.save_library()

    def generate_finder(self):
        """Generate the KDTree Finder."""
        self.finder = KDTree(
            self.library[["x_pos", "y_pos"]],
            leaf_size=40, metric='minkowski'
        )

    def find_nearest(self, coordinates: List[float], k: int = 5):
        """Find the closest books from coordinates."""
        return self.finder.query([coordinates], k=k, return_distance=False)[0]

    def get_coordinates(self, indexes):
        """Return the coordinates (as numpy array) of all the books."""
        return np.array(self.library.iloc[indexes][["x_pos", "y_pos"]])


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    library = Library(api_key=os.getenv('apiKey', ""))
    library.fetch(tag="", author="Bernard Minier")
    print(library.library[['title', 'ISBN13']].head(80))
