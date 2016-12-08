import json
from pprint import pprint
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
with open("C:\\Users\\sachin77\\Documents\\ArcGIS\\Projects\\NIS-CAD\\Database\\amp-realtime-bldgs_1612040125.json") as data_file:    
    data = json.load(data_file)
# arcpy.AddField_management("BuildingsInfo","BuildingName","TEXT")
# arcpy.AddField_management("BuildingsInfo","Code", 'DOUBLE')
bldgno = list()
bldgName = list()
bldgFodler = list()
cnt=0;
for ele in data:
	print(ele)
	bldgName.append(ele['amp_folder_name'])
	bldgno.append(ele['gis_bldg_id'])
	bldgFodler.append(ele['amp_folder_id'])
	print(len(bldgName[cnt]))
	if bldgName[cnt].find('(') !=-1:
		parts = bldgName[cnt].split('(')
		bldgName[cnt] = parts[1][:-1]
		print(bldgName[cnt])
	whereclause = """{} LIKE '%{}%'""".format(arcpy.AddFieldDelimiters('CampusBuilingData', "computed_bldg"),bldgName[cnt][0:3])
	fs = arcpy.UpdateCursor('CampusBuilingData', whereclause )
	for row in fs: 
		if len(bldgno[cnt])<4:
			row.setValue('Building_Number','0'+bldgno[cnt])
		else:
			row.setValue('Building_Number',bldgno[cnt])
		row.setValue('computed_bldg_ref',bldgName[cnt])
		fs.updateRow(row)
	cnt =cnt+1