import tkinter as tk
from tkinter import filedialog, ttk
from typing import Callable


class UserInterface:
    def __init__(
        self,
        merge: Callable[[], None],
    ):
        """
        merge: function that merges csv files
        """
        self.merge = merge
        self.root = tk.Tk()
        self.root.title("CSV Merger")

        # Important variables
        self.data_file_var = tk.StringVar(value='')
        self.filter_file_var = tk.StringVar(value='')
        # Set up interface
        content = ttk.Frame(self.root)
        content.grid(column=0, row=0, sticky='nsew')
        frame = ttk.Frame(content, borderwidth=5, relief="ridge")
        frame.grid(column=0, row=0, columnspan=2, rowspan=3, sticky='nsew')

        file_label = ttk.Label(content, text="Files")
        columns_label = ttk.Label(content, text="Columns")
        self.file_box = tk.Listbox(content, height=10, selectmode="extended")
        self.columns_box = tk.Listbox(content, height=10)
        self.select_files_button = ttk.Button(
            content,
            text="Select files",
            command=self.open_files)
        self.run_button = ttk.Button(
            content,
            text="Combine",
            command=lambda: None)

        file_label.grid(column=0, row=0, sticky='s', pady=(5, 0))
        columns_label.grid(column=1, row=0, sticky='s', pady=(5, 0))
        self.file_box.grid(column=0, row=1, sticky='nsew', padx=10)
        self.columns_box.grid(column=1, row=1, sticky='nsew', padx=10)
        self.select_files_button.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
        self.run_button.grid(column=1, row=2, sticky='nsew', padx=10, pady=10)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=0)
        content.rowconfigure(1, weight=1)
        content.rowconfigure(2, weight=0)

        self.select_files_button.focus()

    def run(self) -> None:
        self.root.mainloop()

    def open_files(self) -> None:
        filenames = filedialog.askopenfilenames(
            filetypes=[("Comma-separated files", "*.csv")]
        )
        self.file_box.delete(0, tk.END)
        self.file_box.insert(0, *filenames)
