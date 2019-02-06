import vsp.py
import numpy as np
import csv



path = "C:\\Users\\a.lejon\\Desktop\\Thesis\\OpenVSP\\geometries\\Test" # Add whatever path you want here
dir_name = "C:\\Users\\a.lejon\\Desktop\\Thesis\\OpenVSP\\geometries\\Test"
sec_id_1 = vsp.GetXSec(1,0); # Center body
sec_id_2 = vsp.GetXSec(2,0); # Transition zone 
sec_id_3 = vsp.GetXSec(3,0); # Wing


sweep_id_1 = vsp.GETXSecParm(sec_id_1,"Sweep");
sweep_id_2 = vsp.GETXSecParm(sec_id_2,"Sweep");
taper_id_3 = vsp.GETXSecParm(sec_id_3,"Taper");
twist_id_3 = vsp.GETXSecParm(sec_id_3,"Twist");
sweep_id_3 = vsp.GETXSecParm(sec_id_3,"Sweep");



sweep_id_3 = vsp.GETXSecParm(sec_id_3,"Sweep");




def createGeom(wing_twist_angle,wing_sweep_angle,wing_taper_ratio,center_body_sweep,transition_sweep_angle):

	# sets wing twist
	vsp.SetParmVal(twist_id_3,wing_twist_angle)
	
	# Sets wing sweep
	vsp.SetParmVal(sweep_id_3,wing_sweep_angle)

	# Sets wing taper
	vsp.SetParmVal(taper_id_3,wing_taper_ratio)
	
	# Sets center body sweep
	vsp.SetParmVal(sweep_id_1,center_body_sweep)
	
	# Sets position of wing (this is the most unclear one since it only sets stuff for the 
	vsp.SetParmVal(sweep_id_3,transition_sweep_angle)
	
	
	vsp.update();
	vsp.WriteVSPFile(path)
	file_name = str(wing_twist_angle) +"_"+ str(wing_sweep_angle) + "_" +str(wing_taper_ratio)+"_"+str(center_body_sweep)+ "_" + str(transition_sweep_angle);
	file_name=+"_DegenGeom.csv"
	
	vsp.SetComputationFileName(vsp.DEGEN_GEOM_CSV_TYPE,dir_name+file_name)
	vsp.Update()
	vsp.ComputeDegenGeom(vsp.SET_ALL,vsp.DEGEN_GEOM_CSV_TYPE)

def createAVL(file):
	with open(file) as csv_file, file as file_name:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 2087 # Found from looking at csv file
		row_counter = 0
		col_counter = 0
		# List preparation 
		x = [[] for i in range(13)]
		y = [[] for i in range(13)]
		z = [[] for i in range(13)]
	
		for row in csv_reader:
			if line_count == 2087:
				print('Column names are {", ".join(row)}')
				line_count += 1
			if line_count == 2326: 
				print('Reached end of plate file segment, aborting')
				break
			else:
				if line_count >= 2088:
					if row_counter % 14 != 0:
						x[col_counter].append(row[1]) # Appends the x coordinate to list 
						y[col_counter].append(row[2]) # Appends the y coordinate to list 
						z[col_counter].append(row[3]) # Appends the z coordinate to list 
						row_counter+=1
					elif row_counter % 14 == 0:
						x[col_counter].append(row[1]) # Same as above 
						y[col_counter].append(row[2]) # Same as above 
						z[col_counter].append(row[3]) # Appends the z coordinate to list 
						row_counter = 0
					
						print('Finished column')
						col_counter+=1
				line_count += 1
		# Postprocessing: Flip the data around so we instead look at chordwise position 
		fixed_x = [[] for i in range(16)]
		fixed_y = [[] for i in range(16)]
 
		for currentCol in range(13): # To keep track of what column we're working on 
			for listElement,i in enumerate(x[currentCol]):
				fixed_x[i].append(listElement) # Creates transposed list
			for listElement,i in enumerate(y[currentCol]):
				fixed_y[i].append(listElement) # Creates transposed list
			
	# At this point we should have a list with 17 lists with 14 values each. 
	
	# AVL file is structured as follows: 
	
	'''
	# =================================================
	#xle  yle    zle      chord    angle nspan  sspace
	SECTION
	0.     0.     0.      20.0     0   0          0
	
	# =================================================
	#xle  yle    zle      chord    angle nspan  sspace
	SECTION
	2.56      3.68     0.      16.91     0   0          0
	
	Thus, we create the AVL file by taking the difference 
	chord = fixed_x[0][-1] - fixed_x[0][0]
	xle = fixed_x[1][0] - fixed_x[0][0]
	yle = fixed_y[1][0] - fixed_y[0][0]
	
	TODO: THIS DOESN'T CHANGE ANGLE. 
	
	Set angle at 9th element to 0 and from 10th and onwards do angle / elements increase per element 
	Airfoil for these also need to be changed to naca instead of reflex
	
	'''
	filename = file_name[:-4]
	filename+".txt"
	f = open(filename,"w+");
	print("File opened.")
	f.write("Blended Wing Body - Configuration 1\n")
	f.write("# =================================================\n")
	f.write("# Mach\n")
	f.write("0.78\n")
	f.write("# IYsym   IZsym   Zsym\n")
	f.write("0       0       0.0\n")
	f.write("# Sref    Cref    Bref\n")
	f.write("313.15     10.79     20.69\n")
	f.write("# Xref    Yref    Zref\n")
	f.write("6.67     0.0     0.0\n")
	f.write("# =================================================\n")
	f.write("# =================================================\n")
	f.write("SURFACE\n")
	f.write("Wing\n")
	f.write("# Nchordwise  Cspace   Nspanwise   Sspace\n")
	f.write("20            1       26       1.0\n")
	f.write("YDUPLICATE\n")
	f.write("0.0\n")
	angle = int(filename[:1])
	angle_list = np.linspace(0, angle, num=6)
	angle_idx = 0
	for list,idx in enumerate(fixed_x):
		if idx==0:
			f.write("# =================================================\n")
			f.write("#xle  yle    zle      chord    angle nspan  sspace\n")
			f.write("SECTION\n")
			
			f.write("0.     0.     0.      20.0     0   0          0")
		
			f.write("AFILE\n")
			f.write("reflex.txt\n")
		
		
		if idx<8 and idx>0:
			f.write("# =================================================\n")
			f.write("#xle  yle    zle      chord    angle nspan  sspace\n")
			f.write("SECTION\n")
			chord = fixed_x[idx][-1] - fixed_x[idx][0]
			xle = fixed_x[idx][0] - fixed_x[idx-1][0]
			yle = fixed_y[idx][0] - fixed_y[idx-1][0]

			f.write(xle) # PUT IN X_LE CALC HERE
			f.write(".     ")
			f.write(yle) # PUT IN Y_LE CALC HERE
			f.write(".     ")
			f.write("0.     ") # IN Z_LE PLACE
			f.write(chord) # PUT IN chord CALC HERE
			f.write(".     ")
			f.write() # PUT IN angle CALC HERE
			f.write("0.     ")
		
			f.write("AFILE\n")
			f.write("reflex.txt\n")
		if idx>8:
			
			f.write("# =================================================\n")
			f.write("#xle  yle    zle      chord    angle nspan  sspace\n")
			f.write("SECTION\n")
			chord = fixed_x[idx][-1] - fixed_x[idx][0]
			xle = fixed_x[idx][0] - fixed_x[idx-1][0]
			yle = fixed_y[idx][0] - fixed_y[idx-1][0]

			f.write(xle) # PUT IN X_LE CALC HERE
			f.write(".     ")
			f.write(yle) # PUT IN Y_LE CALC HERE
			f.write(".     ")
			f.write("0.     ") # IN Z_LE PLACE
			f.write(chord) # PUT IN chord CALC HERE
			f.write(".     ")
			f.write(angle_list[angle_idx]) # PUT IN angle CALC HERE
			f.write(".     ")
			f.write("AFILE\n")
			f.write("naca.txt\n")
			angle_idx+=1
	f.close()
	print("File closed.") 
	
	
for wing_twist in range(-5,0):

	for wing_sweep in range(20,22):

		for wing_taper in range(2,8):
			taper = wing_taper/10; 

			for centerbody_sweep in range(30,32):

				for transition_sweep in range(-50,45):
					
					createGeom(wing_twist,wing_sweep,wing_taper,centerbody_sweep,transition_sweep);	