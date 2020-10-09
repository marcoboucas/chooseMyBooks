"""Create a model that finds neighbors."""

import numpy as np
from sklearn.neighbors import KDTree


def create_finder(coordinates: np.array) -> KDTree:
    """Create the coordinates finder."""
    return KDTree(
        coordinates,
        leaf_size=40,
        metric='minkowski'
    )
