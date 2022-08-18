import multiprocessing
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable

from concatenator import Concatenator
from _version import __version__


class UserInterface:
    def __init__(self) -> None:
        """
        merge: function that merges csv files
        """
        self.root = tk.Tk()
        self.root.title(f"CSV Concatenator v{__version__}")
        self.concatenator = Concatenator([])

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
        self.file_box = tk.Listbox(
            content, height=10, state=tk.DISABLED, disabledforeground="black"
        )
        self.columns_box = tk.Listbox(
            content,
            height=10,
            selectmode="extended",
            exportselection=False,
            selectbackground="white",
            selectforeground="black",
            foreground="gray"
        )
        self.select_files_button = ttk.Button(
            content,
            text="Select files",
            command=self.open_files)
        self.run_button = ttk.Button(
            content,
            text="Combine",
            command=self.combine)

        file_label.grid(column=0, row=0, sticky='s', pady=(5, 0))
        columns_label.grid(column=1, row=0, sticky='s', pady=(5, 0))
        self.file_box.grid(column=0, row=1, sticky='nsew', padx=10)
        self.columns_box.grid(column=1, row=1, sticky='nsew', padx=10)
        self.select_files_button.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
        self.run_button.grid(column=1, row=2, sticky='nsew', padx=10, pady=10)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=0)
        content.rowconfigure(1, weight=1)
        content.rowconfigure(2, weight=0)

        self.select_files_button.focus()

    def run(self) -> None:
        self.root.mainloop()

    def open_files(self) -> None:
        opened_files = filedialog.askopenfilenames(
            filetypes=[("Comma-separated files", "*.csv")]
        )
        filenames = [] if opened_files == '' else opened_files
        self.file_box.config(state=tk.NORMAL)
        self.file_box.delete(0, tk.END)
        self.file_box.insert(0, *filenames)
        self.file_box.config(state=tk.DISABLED)
        self.concatenator = Concatenator(filenames)
        self.columns_box.insert(0, *self.concatenator.fieldnames)
        self.columns_box.selection_set(0, tk.END)

    def combine(self) -> None:
        output_filename = filedialog.asksaveasfilename(
            filetypes=[("Comma-separated files", "*.csv")]
        )
        if output_filename != '' and output_filename is not None:
            self.columns_box.config(state=tk.DISABLED)
            self.select_files_button.config(state=tk.DISABLED)
            self.run_button.config(state=tk.DISABLED)

            def process() -> None:
                columns = self.columns_box.curselection()
                with open(output_filename, 'w') as output_file:
                    self.concatenator.write_file(output_file, columns)

            thread = multiprocessing.Process(target=process)
            thread.start()

            def on_finish() -> None:
                messagebox.showinfo('Done!', message='Files combined successfully')
                self.columns_box.config(state=tk.NORMAL)
                self.select_files_button.config(state=tk.NORMAL)
                self.run_button.config(state=tk.NORMAL)

            create_loading_window(self.root, thread, on_finish)


def create_loading_window(root: tk.Tk,
                          thread: multiprocessing.Process,
                          on_finish: Callable[[], None]) -> None:
    loading_window = tk.Toplevel(root)
    if sys.platform.startswith('linux'):
        loading_window.attributes('-type', 'dialog')
    elif sys.platform.startswith('windows'):
        loading_window.attributes('-toolwindow', True)
    loading_window.title('Processing')
    progress = ttk.Progressbar(loading_window, orient='horizontal', mode='indeterminate')
    progress.pack()
    progress.start(10)

    def check_if_running() -> None:
        if thread.is_alive():
            loading_window.after(10, check_if_running)
        else:
            loading_window.destroy()
            on_finish()

    loading_window.after(50, check_if_running)
    loading_window.mainloop()
