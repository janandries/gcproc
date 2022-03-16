import gcprocess

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

h = gcprocess.gcp()

print()
print("Select file in dialog window")

file_path = filedialog.askopenfilename()

h.load_file(file_path)

print(f"Selected file: {file_path}")
print()
frequency = int(input("Enter valve frequency [Hz]: "))
duty_cycle = float(input("Enter valve duty cycle [0-1]: "))
layer_height = float(input("Enter layer height [mm]: "))
initial_layer_height = float(input("Enter INITIAL layer height [mm]: "))
use_half_layers = int(input("Deposit in one direction (1) or in both directions (2)?: "))

h.process(frequency, duty_cycle, layer_height, initial_layer_height, use_half_layers==2)

h.save_to_file(file_path + '.output')

print()

h.show_report()

input("Press enter to continue...")