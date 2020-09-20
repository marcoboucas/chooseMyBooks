"""Loading and Saving of a library."""

import pandas as pd

from .book_handler import BookHandler


class LibraryLoader(BookHandler):
    """Loader and Saver of libraries."""

    library: pd.DataFrame
    file: str

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
