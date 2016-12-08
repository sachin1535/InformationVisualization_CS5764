import xml.etree.ElementTree as ET
tree = ET.parse("C:\\Users\\sachin77\\Documents\\ArcGIS\\Projects\\NIS-CAD\\Database\\buildinRef.xml")
root = tree.getroot()
child1 = root.getchildren()

import json
from pprint import pprint

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
	bldgName.append(str(ele['amp_folder_name'])
	bldgno.append(ele['gis_bldg_id'])
	bldgFodler.append(ele['amp_folder_id'])
	print(len(bldgName[cnt])
	if len(bldgName[cnt])>6:
		parts = bldgName[cnt].split('(')
		bldgName[cnt] = parts[1][:-1]
		print(bldgName[cnt])
	whereclause = """{} LIKE %{}% And {} <> ' '""".format(arcpy.AddFieldDelimiters('CampusBuilingData', "computed_bldg"),bldgName[cnt][0:3])
	fs = arcpy.UpdateCursor('CampusBuilingData', whereclause )
	for row in fs: 
		row.setValue('Building_Number',bldgno[cnt])
		row.setValue('computed_bldg_ref',bldgName[cnt])
		fs.updateRow(row)
	cnt =cnt+1


for row in fs:
	bldgno.append(data[cnt]['gis_bldg_id'])
	bldgName.append(data[cnt]['amp_folder_name'])
	bldgFodler.append(data[cnt]['amp_folder_id'])

	row.setValue('Building_Number')
	row.setValue('computed_bldg_ref')
	cnt = cnt+1;
rows = arcpy.InsertCursor('BuildingsInfo')
for cnt in range(len(codeList)):
    row = rows.newRow()
    row.setValue("BuildingName", buildinNameList[cnt])
    row.setValue("Code", codeList[cnt])
    rows.insertRow(row)
