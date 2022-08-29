from gcprocess import gcp
import functools
import re

test_string = [
";LAYER:1",
";TYPE:FILL",
";MESH:20220822_Daroc-rif_All materials.stl",
"G1 X108.5 Y105.63 E67.27987",
"G0 X112 Y107.504",
"G1 X112 Y96.367 E82.55542",
"G0 X115.5 Y97.627",
"G1 X115.5 Y106.399 E94.58712",
"G0 X94.5 Y154.867",
"G1 X94.5 Y163.409 E106.30335",
"G0 F1000.12 X91 Y164.718",
"G1 X91 Y153.468 E121.73389",
"G0 F2000 X87.5 Y153.946",
"G1 F2000 X87.5 Y163.789 E135.23458"
]

outcome = [
";LAYER:1",
";TYPE:FILL",
";MESH:20220822_Daroc-rif_All materials.stl",
"G1 X108.5 Y105.63 P1",
"G0 X112 Y107.504",
"G1 X112 Y96.367 P1",
"G0 X115.5 Y97.627",
"G1 X115.5 Y106.399 P1",
"G0 X94.5 Y154.867",
"G1 X94.5 Y163.409 P1",
"G0 X91 Y164.718",
"G1 X91 Y153.468 P1",
"G0 X87.5 Y153.946",
"G1 X87.5 Y163.789 P1"
]

# g = gcp()
# g.set_list_of_instructions(test_string)
#
# o = g.append_p0_to_g0(test_string)
# o = g.replace_e_for_p1(o)
#
#
# if functools.reduce(lambda x, y: x and y, map(lambda a, b: a == b, o, outcome), True):
#     print("Both List are same")
# else:
#     print("Not same")
#

def check_g1(text):
    source = r"(G1 (?:F\d+(?:.?\d*)? )?X\d+(?:.\d*)? Y\d+(?:.\d*)?)(?: E\d+(?:.\d*))"
    target = r"\1 P1"

    for line in text:
        print(f"line: {line}")
        print(re.findall(source, line))
        print(f"subbed: {re.sub(source, target, line)}")
        print()

def append_p0_to_g0(text):
    source = r"(G0 (?:F\d+(?:.?\d*)? )?X\d+(?:.\d*)? Y\d+(?:.\d*)?)"
    target = r"\1 P0"

    for line in text:
        print(f"line: {line}")
        print(re.findall(source, line))
        print(f"subbed: {re.sub(source, target, line)}")
        print()

def replace_all_g0_g1_x_y_speeds(text):
    source = r"(G[01] )(F\d+(?:.?\d*)?)( X\d+(?:.\d*)? Y\d+(?:.\d*)?.*)"
    speed = 5000
    target = f"\\1F{speed}\\3"

    for line in text:
        print(f"line: {line}")
        print(re.findall(source, line))
        print(f"subbed: {re.sub(source, target, line)}")
        print()

#def replace

replace_all_g0_g1_x_y_speeds(test_string)


