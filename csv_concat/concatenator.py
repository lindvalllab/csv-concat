import csv
from typing import List, TextIO


class Concatenator:
    def __init__(self, files: List[TextIO]):
        self.readers = [csv.DictReader(file) for file in files]
