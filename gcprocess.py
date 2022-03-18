from dataclasses import dataclass

@dataclass
class MachineDefinition:
    u_load : int
    u_return : int
    y_safe : int

#here a profile should be loaded
#md = MachineDefinition(10, 304, 0)   #Idefix_25
#md = MachineDefinition(10, 201, 100) #Idefix_15

class gcp:
	def __init__(self):
		print("GCP started")
		self.c_M10X_ignored = 0
		self.c_G92_ignored = 0
		self.c_init_settings_added = 0
		self.c_home_pause_after_layer = 0
		self.c_z_after_mesh = 0
		self.c_lines_left_alone = 0
		self.c_valve_stop = 0
		
	def load_file(self, filename):
		self.input_filename = filename
		print(f"Loading file {filename}")
		self.file = open(filename, "r")
		self.proc_text = []

	def show_report(self):
		print("===========================================================")
		print(f"Finished processing {self.input_filename}")
		print()
		print(f"Lines processed: {self.current_line_nr}")
		print()
		print(f"M10X commands removed: {self.c_M10X_ignored}")
		print(f"G92 commands removed: {self.c_G92_ignored}")
		print(f"Initial settings added: {self.c_init_settings_added}")
		print(f"Home&pause after layer: {self.c_home_pause_after_layer}")
		print(f"Z commands after ;MESH: removed: {self.c_z_after_mesh}")
		print(f"Lines left alone: {self.c_lines_left_alone}")
		print(f"Valve close commands: {self.c_valve_stop}")
		if (self.c_valve_stop == 0): print("!ERROR! No valve stop command added to end")
		print("===========================================================")

	def save_to_file(self, filename):
		with open(filename, 'w') as f:
			for line in self.proc_text:
				f.write("%s" % line)

	def process(self, frequency, duty_cycle, layer_height, initial_layer_height, use_half_layers, machine):
		self.FIRST_MESH_PROCESSED = False
		self.valve_frequency = frequency
		self.valve_duty_cycle = duty_cycle
		self.layer_height = layer_height
		self.initial_layer_height = initial_layer_height
		self.use_half_layers = use_half_layers
		self.md = MachineDefinition(machine['u_load'], machine['u_return'], machine['y_safe']) #Idefix_15

		previous_line = ''

		print("Start processing with freq: {frequency:.0f}, duty_cycle: {duty_cycle:.1f}, layer_height: {layer_height:.0f}")
		#ignore commands:
		ignore_list = ('M104', 'M105', 'M107', 'M109')

		lines = self.file.readlines()
		self.current_line_nr = 0
		self.current_layer_index = 0
		for line in lines:
			self.current_line_nr += 1
			#IGNORE ANY LINES THAT WE DON'T WANT
			if line.startswith(ignore_list):
				print(f"[Line {self.current_line_nr}] Ignoring {line.strip()}")
				
				if line.startswith('M'):
					self.c_M10X_ignored += 1
				elif line.startswith('G92'): #to remove
					#self.c_G92_ignored += 1
					self.proc_text.append(line)
				
				previous_line = line
				continue

			#ADD INITIAL SETTINGS AFTER THE LAYER_COUNT
			if line.startswith(';LAYER_COUNT:'):
				print(f"[Line {self.current_line_nr}] Appending initial settings after {line.strip()}")
				self.proc_text.append(line)
				self.proc_text.append(self.get_initial_settings_string(self.valve_frequency,self.valve_duty_cycle, self.initial_layer_height, self.use_half_layers))
				
				self.c_init_settings_added += 1

				previous_line = line
				continue

			#ADD HOMING AND PAUSE AFTER EACH LAYER
			if line.startswith(';LAYER:'):
				#recall the last string which contains a G0 move to where we were
				last_g_code_command = self.proc_text[-2] #this line should be the original G0 move
				
				#pop this command, as we are going to add it after this
				self.proc_text.pop(-2)

				self.current_layer_index += 1
				
				time_elapse = self.proc_text[-1]
				if not time_elapse.startswith(';TIME_ELAPSED:'):
					#something is wrong here?
					print(f"[Line {self.current_line_nr}] ERROR: line after line before ';LAYER:' is not ;TIME_ELAPSED: but {line.strip()}")
				print(f"[Line {self.current_line_nr}] Found {line.strip()}, prepending homing&pausing")

				half_layer = self.layer_height / 2
				self.proc_text.append(f"""
;deposit one layer of {self.layer_height:,.1f} mm
G1 F7200 Y{self.md.y_safe}   ;move Y axis out of the way
G1 F3000 U{self.md.u_load}     ;move to begin position""")
				if self.use_half_layers:
					self.proc_text.append(f"""
G91                     ;enable relative motion
G1 Z{half_layer:,.2f}   ;move bed down half a layer
G90                     ;absolute positioning""")
				else:
					self.proc_text.append(f"""
G91                     ;enable relative motion
G1 Z{self.layer_height:,.2f}   ;move bed down one thickness
G90                     ;absolute positioning""")
				self.proc_text.append(f"""
G4 S1     ; wait one second to prevent it from continuing directly
M577 E1 S0              ;wait for endstop_1 turn low
G1 F3000 U{self.md.u_return}           ;deposit material""")

				if self.use_half_layers:
					self.proc_text.append(f"""
G91                     ;enable relative motion
G1 Z{half_layer:,.2f}   ;move bed down half a layer
G90       ;absolute positioning""")

				self.proc_text.append(f"""
G1 F3000 U{self.md.u_load}     ;scrape and return

""")

				self.c_home_pause_after_layer += 1
				
				self.proc_text.append(last_g_code_command)

				self.proc_text.append(line)
				previous_line = line
				continue

			#remove Z value from command after ';MESH:NONMESH' or after the first ;MESH (it is an exception)
			if previous_line.startswith(';MESH:NONMESH') or (previous_line.startswith(';MESH') and not self.FIRST_MESH_PROCESSED):
				self.FIRST_MESH_PROCESSED = True
				#find the a Z occurance
				pos = line.find(' Z')
				if pos != -1:
					print(f"[Line {self.current_line_nr}] Found {line.strip()} after {previous_line.strip()}. Removing the Z command!")
					line_without_z = line[:pos+1] + ';' + line[pos+1:]
					self.c_z_after_mesh += 1
				self.proc_text.append(line_without_z)

				previous_line = line
				continue

			#stop the valve at the end of the program
			if line.startswith(';M104 S0'): # ';M104 S0' somehow is always used at the end before homing'
				self.proc_text.append(line)
				self.proc_text.append("M42 P21 S0;stop the valve\n")
				self.c_valve_stop += 1

				previous_line = line
				continue


			#In all other cases we just add the line
			self.proc_text.append(line)
			self.c_lines_left_alone += 1

			previous_line = line
			continue



	def get_initial_settings_string(self, frequency, duty_cycle, initial_layer_thickness, use_half_layers):
		string = f"""M563 P1 D1 ;H0 ; tool 1 uses extruder 0, heater 0 (and fan 0)
T1 ;select tool 1
M302 P1 ;enable the cold extrusion (we don't care about temperatures!)

M106 P1 I-1 ;disable FAN1 signal
M571 P21 F{frequency} S{duty_cycle:,.2f} ; set the fan1 with the extruder"""

		if use_half_layers:
			string = (f"""{string}
;deposit initial layer of 3 mm
G1 F7200 Y{self.md.y_safe}   ;move Y axis out of the way
G1 F3000 U{self.md.u_load}     ;move to begin position
G91                     ;enable relative motion
G0 Z{initial_layer_thickness/2:,.2f}   ;move bed down half a layer
G90                     ;absolute positioning
G4 S1     ; wait one second to prevent it from continuing directly
M577 E1 S0              ;wait for endstop_1 turn low\n
G1 F3000 U{self.md.u_return}           ;deposit material
G91                     ;enable relative motion
G1 Z{initial_layer_thickness/2:,.2f}   ;move bed down half a layer
G90       ;absolute positioning
G1 F3000 U{self.md.u_load}     ;scrape and return

""")
		else:
			string = (f"""{string}
;deposit initial layer of 3 mm
G1 F7200 Y{self.md.y_safe}   ;move Y axis out of the way
G1 F3000 U{self.md.u_load}     ;move to begin position
G91                     ;enable relative motion
G0 Z{initial_layer_thickness:,.2f}                 ;move bed down initial layer
G90                     ;absolute positioning
G4 S1     ; wait one second to prevent it from continuing directly
M577 E1 S0              ;wait for endstop_1 turn low\n
G1 F3000 U{self.md.u_return}           ;deposit material
G1 F3000 U{self.md.u_load}            ;scrape and return

""")

		return string

