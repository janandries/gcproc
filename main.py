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
layer_height = int(input("Enter layer height [mm]: "))

h.process(frequency, duty_cycle, layer_height)

h.save_to_file(file_path + '.output')

print()

h.show_report()

print()
print("Done.")
print()
print("WARNING: STOPPING THE VALVE AT END OF PROGRAM NOT YET IMPLEMENTED")
print("DON'T FORGET TO MANUALLY ADD 'M42 P21 S0;stop the valve' AT THE ")
print("END OF THE FILE!")
print()

input("Press enter to continue...")