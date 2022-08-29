import gcprocess
import yaml

import tkinter as tk
import sys
from tkinter import filedialog
import os

OUTPUT_FOLDER = "output"

def key_at_index(mydict, index_to_find):
    for index, key in enumerate(mydict.keys()):
        if index == index_to_find:
            return key
    return None  # the index doesn't exist

root = tk.Tk()
root.withdraw()

h = gcprocess.gcp()

#first load the machines file
machines = []
try: 
    with open('machines.yaml') as f:
        machines = yaml.load(f, Loader=yaml.FullLoader)
except OSError as err:
        msg = "Error opening machines.yaml. Is the file there?"
        sys.exit(1)

print()
print("Select file in dialog window")

file_path = filedialog.askopenfilename()

h.load_file(file_path)

print(f"Selected file: {file_path}")
print()
frequency = int(input("Enter valve frequency [Hz]: "))
duty_cycle = float(input("Enter valve duty cycle [0-1]: "))
feed_rate = int(input("Enter desired feed rate [mm/min]: "))
layer_height = float(input("Enter layer height [mm]: "))
initial_layer_height = float(input("Enter INITIAL layer height [mm]: "))
use_half_layers = int(input("Deposit in one direction (1) or in both directions (2)?: "))

# print availble machines:
print("Please select a machine: ")
i = 0
for count, (key, value) in enumerate(machines.items(), 1):
    print(f"\t({count}) - {key}")
machine_idx = int(input())
machine = machines[key_at_index(machines, machine_idx-1)]

h.process(frequency, duty_cycle, feed_rate, layer_height, initial_layer_height, use_half_layers==2, machine)

h.show_report()

#check if output folder exist:
abs_output_folder = os.path.join(os.path.dirname(file_path), OUTPUT_FOLDER)
if not os.path.exists(abs_output_folder):
    print()
    print(f"Didn't find output folder. Creating '/output'")
    os.makedirs(abs_output_folder)
output_filename = os.path.join(abs_output_folder, os.path.basename(file_path))

h.save_to_file(output_filename)
print()
print(f"Written out to {output_filename}")
print()


input("Press enter to continue...")