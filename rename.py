import os
pathworldFiles = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/CADFiles/";
cadwaplist = list();
for file in os.listdir(pathworldFiles):
	if file.endswith(".dwg"):
		parts = file.split('_');
		nameWldFile = parts[len(parts)-1][0:len(parts[len(parts)-1])-4]+".wld";
		for fileIn in os.listdir(pathworldFiles):
			if fileIn.endswith(".wld"):
				if nameWldFile == fileIn:
					filePath = pathworldFiles + fileIn;
					os.rename(filePath,pathworldFiles+file[0:len(file)-4]+".wld")
