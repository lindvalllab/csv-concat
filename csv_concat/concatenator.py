import csv
import os
from typing import Sequence, TextIO


class Concatenator:
    def __init__(self, filenames: Sequence[str]):
        self.filenames = filenames
        if len(self.filenames) == 0:
            self.fieldnames: Sequence[str] = []
        else:
            # Get field names present in all the files in the same order as the first file
            with open(filenames[0]) as first_file:
                first_rd = csv.DictReader(first_file)
                first_fields = first_rd.fieldnames if first_rd.fieldnames is not None else []

            common_fieldnames = set(first_fields)
            for filename in self.filenames[1:]:
                with open(filename) as file:
                    reader = csv.DictReader(file)
                    if reader.fieldnames is None:
                        common_fieldnames = set()
                    else:
                        common_fieldnames &= set(reader.fieldnames)
            self.fieldnames = [field for field in first_fields if field in common_fieldnames]

    def write_file(self, output_file: TextIO) -> None:
        writer = csv.writer(output_file, lineterminator=os.linesep)
        writer.writerow(self.fieldnames)
        for filename in self.filenames:
            with open(filename) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    writer.writerow([row[field] for field in self.fieldnames])
