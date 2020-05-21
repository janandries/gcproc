import gcprocess

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

h = gcprocess.gcp()
h.load_file()

file_path = filedialog.askopenfilename()




