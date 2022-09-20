import multiprocessing
from typing import List, Optional

from ui import UserInterface
from concatenator import Concatenator


def process(
    concatenator: Concatenator,
    columns: Optional[List[int]],
    output_filename: str
) -> None:
    with open(output_filename, 'w') as output_file:
        concatenator.write_file(output_file, columns)


if __name__ == '__main__':
    # Required for building on Windows
    # https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    multiprocessing.freeze_support()

    ui = UserInterface(process)
    ui.run()
