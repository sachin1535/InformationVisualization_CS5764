import arcpy
from arcpy import env
import os 
path = "C:\Users\sachin77\Documents\ArcGIS\Projects\NIS"
gdb_path = "C:\Users\sachin77\Documents\ArcGIS\Projects\NIS"
gdb = "mynisDB.gdb"
env.workspace = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS"
op_gdb_path = os.path.join(gdb_path, gdb)
reference_scale = "1000"
for file in os.listdir(path):
	if file.endswith(".dwg"):
		print "found " + file
		input_file = os.path.join(path,file)
		try:
			arcpy.CADToGeodatabase_conversion(input_file,op_gdb_path,file[:-4],reference_scale)
		except:
			print arcpy.GetMessage()

arcpy.Select_analysis(r"HARPER_HALL_1STFLOOR_0042ca01\Point","WAP_POINTS", "\"Layer\" = 'E-COMM-WIRELESS'")
arcpy.Select_analysis(r"HARPER_HALL_1STFLOOR_0042ca01\Annotation","CADAnno")
infoList_Anno = arcpy.da.TableToNumPyArray("CADAnno",["Text","Owner"])
infoWap = arcpy.da.TableToNumPyArray("WAP_POINTS","Handle")


# for point in infoWap:
# 	for x in infoList:
# 		if x[1]== point[0]:
# 			print x[0] + "points " + point[0]

tf= open("Wap_IDs.txt1","w")
for point in infoWap :
	for x in infoList_Anno:
		if x[1]== point[0]:
			tf.write("{} \n".format(x[0]))
tf.close()



# in Arc Pro 
import arcpy
from arcpy import env
import os

path = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS"
gdb_path ="C:/Users/sachin77/Documents/ArcGIS/Projects/NIS"
gdb = "mynisDB.gdb"
env.workspace = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS"
op_gdb_path = os.path.join(gdb_path, gdb)
reference_scale = "1000"

for file in os.listdir(path):
	if file.endswith(".dwg"):
		print ("found " + file)
		input_file = os.path.join(path,file)
		try:
			arcpy.CADToGeodatabase_conversion(input_file,op_gdb_path,file[:-4],reference_scale)
		except:
			print(arcpy.GetMessage())

arcpy.Select_analysis("C:/Users/sachin77/Documents/ArcGIS/Projects/NIS\mynisDB.gdb\HARPER_HALL_1STFLOOR_0042ca01\Point","WAP_POINTS", "\"Layer\" = 'E-COMM-WIRELESS'")

arcpy.Select_analysis("C:/Users/sachin77/Documents/ArcGIS/Projects/NIS\mynisDB.gdb\HARPER_HALL_1STFLOOR_0042ca01\Annotation","Anno_Lyr")

infoList_Anno = arcpy.da.TableToNumPyArray("C:/Users/sachin77/Documents/ArcGIS/Projects/NIS\Anno_Lyr.shp",["Text","Owner"])

infoWap = arcpy.da.TableToNumPyArray("C:/Users/sachin77/Documents/ArcGIS/Projects/NIS\WAP_POINTS.shp","Handle")

tf= open("Wap_IDs.txt2","w")
for point in infoWap :
	for x in infoList_Anno:
		if x[1]== point[0]:
			tf.write("{} \n".format(x[0]))
tf.close()
