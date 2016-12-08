import arcpy
from arcpy import env
import os
path = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/WAP-Results.gdb"
pathRes = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/Floor-Results.gdb"
env.workspace = path
path = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/WAP-Results.gdb"
arcpy.env.workspace = path
datafs = arcpy.ListFeatureClasses();
for fs in datafs:
	floorList = set((row.getValue("FLOOR") for row in arcpy.SearchCursor(fs)))
	buildind_Name = set((row.getValue("B_NAME") for row in arcpy.SearchCursor(fs)))
#Creating Floor Layers
for floor in floorList: 
	if floor != None:
		whereclause = """{} = '{}'""".format(arcpy.AddFieldDelimiters(fs, "FLOOR"),floor)			
		arcpy.Select_analysis(fs,pathRes+"\\"+fs+"_"+floor, whereclause)

#Creating Polygons 
env.workspace = pathRes
datafs = arcpy.ListFeatureClasses();
for fs in datafs:
	if  fs != "Buildings":
		arcpy.CreateThiessenPolygons_analysis(fs, "Thiessen_Polygons", "ALL")
		arcpy.Clip_analysis("Thiessen_Polygons", "Buildings", fs+"_Clip", "")
		arcpy.Delete_management("Thiessen_Polygons")
datafs = arcpy.ListFeatureClasses();
for fs in datafs:
	if fs[len(fs)-4:len(fs)]== "Clip":
		cnt=1;
		features = arcpy.UpdateCursor(fs)
		for row in features:
			# arcpy.AddField_management(fs,"Population",'DOUBLE')
			# arcpy.AddField_management(fs,"stime","TEXT")
			# arcpy.AddField_management(fs,"etime","TEXT")
			row.setValue("Population",cnt)
			row.setValue("stime",'2016-11-08 07:05:08')
			row.setValue("etime",'2016-11-08 18:50:39')
			features.updateRow(row)
			cnt=cnt+1
		for row in features:
			# arcpy.AddField_management('BuildingEdit',"Height",'DOUBLE')
			row.setValue("Height",25)
			features.updateRow(row)
			cnt=cnt+1