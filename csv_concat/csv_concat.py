import multiprocessing

from ui import UserInterface

if __name__ == '__main__':
    # Required for building on Windows
    # https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    multiprocessing.freeze_support()

    ui = UserInterface()
    ui.run()
