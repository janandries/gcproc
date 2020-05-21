# gcproc
G-Code preprocessor for using Cura generated extrusion code for water jet 3D cement printing.

# Functionality

The processor should do the following steps:

1: ADD with the setting you need after F and S in the last command after `;LAYER_COUNT:`

	M563 P1 D0 ;H0 ; tool 1 uses extruder 0, heater 0 (and fan 0)
	T1 ;select tool 1
	M302 P1 ;enable the cold extrusion

	M106 P1 I-1 ;disable FAN1 signal
	M571 P21 F50 S0.3 ;is the command to set the fan with the extruder
	
2: REMOVE commands `M104` `M105` `M107` `M109`

3: REMOVE all `G92 E0` commands (not sure if necessary?!)

4: ADD before each `;LAYER:` where the layer number is >=1 
	G28 X ;Home
	G28 Y
	G0 F6000 X0 Y0 Z6
	G4 P30000 ;pause 30s
	REMEMBER to put the Z value correct to the layer!!
	
5: ADD after what you add before the last G command before `;TIME_ELAPSED:` at the end of each layer, with `G0`
```
	EXAMPLE: 
	(G0 X63.538 Y122.911 THIS LINE is the same
	;TIME_ELAPSED:7.787348

	G28 X ;Home
	G28 Y
	G0 F6000 X0 Y0 Z6
	G4 P30000 ;pause 30s 
	G0 X63.538 Y122.911 OF THIS with G0 even if before was G1

	;LAYER:1) 
```
6: ADD at the end of the Gcode before the homing this command
```
M42 P21 S0;stop the valve
```
	
7: Remove all the movement of the Z at the end of the layers

8: Before you run double check the Z and check the speed you are using if it is the one you need
