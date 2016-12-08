import arcpy
from arcpy import env
import os
path = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/CADFiles/"
gdb_path ="C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/"
xml_files_path = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/XML_DB/"
wap_results_path = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/WAPIdsFiles/"
WapLayerPath = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/WAPLayers/"
gdb = "NIS-CAD.gdb"
op_gdb_path = os.path.join(gdb_path, gdb)
env.workspace = op_gdb_path
fs = arcpy.UpdateCursor('CampusBuildingLog', "\"OBJECTID\" > {}".format(-1) )
waplist = list()
for row in fs:
	waplist.append(row.getValue("orig_ap_device"))
	print(etime)

cnt=1;
fs = arcpy.UpdateCursor('NM_Data', "\"OBJECTID\" > {}".format(-1) )
leneles = len(etimeList);
for row in fs:
	if leneles!=cnt:
		etime = row.setValue("EndTime",etimeList[cnt])
	cnt=cnt+1;
	fs.updateRow(row)
filepath = "C:\Users\sachin77\Documents\ArcGIS\Projects\NIS-CAD\Database\Building_Refernce_Data.xlsx"

for row in fs: 
	bldno = row.getValue("computed_bldg")

fs = arcpy.UpdateCursor('SheetVals')
codeslist = list()
buildingNameList = list()
for row in fs: 
	name = row.getValue('File_Name')
	nameparts = name.split('_')
	codeslist.append(nameparts[3][0:4] )
	buildingNameList.append((nameparts[0],nameparts[1])

fs = arcpy.UpdateCursor('SheetVals')
codeslist = list()
buildingNameList1 = list()
for row in fs: 
	name = row.getValue('File_Name')
	nameparts = name.split('_')
	codeslist.append(nameparts[len(nameparts)-1][0:4] )
	buildingNameList1.append(nameparts[0])

   

import json
from pprint import pprint

with open("C:\\Users\\sachin77\\Documents\\ArcGIS\\Projects\\NIS-CAD\\Database\\info.json") as data_file:    
    data = json.load(data_file)

features  = data["features"]
buildinNameList = list()
codeList = list()
for feature in features:
	attr = feature["attributes"]
	buildinNameList.append(attr["NAME"])
	codeList.append(attr["BLDG_NUM"])
	print(attr)
fs = arcpy.UpdateCursor('BuildingsInfo', "\"OBJECTID\" > {}".format(-1) )
# arcpy.AddField_management("BuildingsInfo","BuildingName","TEXT")
# arcpy.AddField_management("BuildingsInfo","Code", 'DOUBLE')

rows = arcpy.InsertCursor('BuildingsInfo')
for cnt in range(len(codeList)):
    row = rows.newRow()
    row.setValue("BuildingName", BuildingName[cnt])
    row.setValue("Code", codeList[cnt])
    rows.insertRow(row)

