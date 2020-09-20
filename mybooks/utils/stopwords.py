"""Stopwords loading."""
import os

curent_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(curent_path, "..", 'data/stopwords.txt'), "r") as file:
    STOPWORDS = file.readlines()
