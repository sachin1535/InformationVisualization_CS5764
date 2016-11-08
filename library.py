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
print(op_gdb_path)
reference_scale = "10"
#arcpy.CreateFeatureclass_management(gdb_path,"WapPoints")
path2features = list()
cadBlockRefNames = list(tuple())
foldersList = list()
for (pathtemp,folders,filesTemp) in os.walk(path):
	if len(folders) !=0:
	    for folder in folders:
	    	foldersList.append(folder)
	    	#arcpy.CreateFolder_management(op_gdb_path, folder)
for folder in foldersList:
	print(folder)
	print(path)
	out_feature_dataset = folder
	arcpy.CreateFeatureclass_management(gdb_path, folder+"WAP_Points.shp", "POINT")
	arcpy.AddField_management(folder+"WAP_Points.shp","WAPID","TEXT")
	arcpy.AddField_management(folder+"WAP_Points.shp","B.NAME","TEXT")
	fieldMappings = arcpy.FieldMappings()
	fieldMappings.addTable(folder+"WAP_Points.shp")
	for file in os.listdir(path+folder):
		if file.endswith(".dwg"):
			input_file = os.path.join(path+folder,file)
			print("found " + input_file)
			try:
				datasets_exist = arcpy.ListDatasets()
				if folder in datasets_exist:
					arcpy.Delete_management(folder);
					arcpy.CADToGeodatabase_conversion(input_file,op_gdb_path,out_feature_dataset,reference_scale)
					print(folder in datasets_exist)				
				else:
					arcpy.CADToGeodatabase_conversion(input_file,op_gdb_path,out_feature_dataset,reference_scale)
					print(folder in datasets_exist)				
				
				path2features = op_gdb_path+"\\"+out_feature_dataset
				arcpy.Select_analysis(path2features+"\\" + "Point","tempPoint.shp", "\"Layer\" = 'E-COMM-WIRELESS'")
				infoNLRef = arcpy.da.TableToNumPyArray("tempPoint.shp","RefName")
				infoNLRef = set(infoNLRef[0])
				infoNLRef = tuple(infoNLRef)
				cadBlockRefNames = infoNLRef
				arcpy.Delete_management("tempPoint.shp")
				print(cadBlockRefNames)
				for featureCls in cadBlockRefNames:
					whereclause = """{} = 'E-COMM-WIRELESS' And {} <> ' '""".format(arcpy.AddFieldDelimiters(path2features+"\\" +featureCls, "Layer"),arcpy.AddFieldDelimiters(path2features+"\\" +featureCls, "PORTAL"))
					arcpy.Select_analysis(path2features+"\\" +featureCls ,"temp1.shp", whereclause )
					infoNLWAP = arcpy.da.TableToNumPyArray("temp1.shp","PORTAL")
					#print(infoNLWAP)	
					whereclause = """{} = 'E-COMM-WIRELESS' And {} <> ' '""".format(arcpy.AddFieldDelimiters(path2features+"\\" +featureCls, "Layer"),arcpy.AddFieldDelimiters(path2features+"\\" +featureCls, "Text"))			
					arcpy.Select_analysis(path2features+"\\" + "Annotation","temp2.shp", whereclause)
					AnnoNLWAP = arcpy.da.TableToNumPyArray("temp2.shp","Text")
					#print(AnnoNLWAP)
					#merger layers features in one feature layer 
					#Adding Point X and Point Y fields 
					#Merging different points in One Layer
					fldMap = arcpy.FieldMap() 
					fldMap.addInputField("temp1.shp","PORTAL")
					currwaps = fldMap.outputField
					currwaps.name, currwaps.aliasName, currwaps.type = "WAPID", "WAPID", "TEXT"
					fldMap.outputField = currwaps
					fieldMappings.addFieldMap(fldMap)
					arcpy.Append_management('temp1.shp', folder+"WAP_Points.shp", 'NO_TEST',fieldMappings)
					
					fldMap = arcpy.FieldMap() 
					fldMap.addInputField("temp2.shp","Text")
					currwaps = fldMap.outputField
					currwaps.name, currwaps.aliasName, currwaps.type = "WAPID", "WAPID", "TEXT"
					fldMap.outputField = currwaps
					fieldMappings.addFieldMap(fldMap)
					arcpy.Append_management('temp2.shp', folder+"WAP_Points.shp", 'NO_TEST',fieldMappings)

					#Deleting the Temporary created Feature Classes
					arcpy.Delete_management("temp1.shp")
					arcpy.Delete_management("temp2.shp")
					#Delete IOdenticle points 
					arcpy.DeleteIdentical_management(folder+"WAP_Points.shp", 'WAPID')
					#creating combine list
					infoNLWAP = infoNLWAP.tolist()
					AnnoNLWAP = AnnoNLWAP.tolist()
					Combo = list()
					waplist = [infoNLWAP,AnnoNLWAP]
					for ele in waplist:
						for name in ele:
							parts = name[0].split(',')
							Combo.append("LIB-234"+parts[0])
					print(Combo)

					#Writing results for Each File
					dir_ForResults = wap_results_path+"\\"+folder+"\\"
					dd = os.path.dirname(dir_ForResults)
					if not os.path.exists(dd):
					    os.mkdir(dd)
					exportResults = dd+"\\"+file[0:len(file)-4]+".txt"
					tf= open(exportResults,"w")
					for wapid in Combo: 
						if wapid != ' ':
								tf.write("{}\n".format(wapid))
					tf.close()

					dir_ForDB = xml_files_path+folder+"\\"
					dd = os.path.dirname(dir_ForDB)
					if not os.path.exists(dd):
					    os.mkdir(dd)
					print(dir_ForDB)
					currXMLFile = dir_ForDB+file[:-4]+".xml"
					if not os.path.isfile(currXMLFile):
						arcpy.ExportXMLWorkspaceDocument_management(op_gdb_path+"\\"+folder,dir_ForDB+file[:-4]+".xml")
	arcpy.AddGeometryAttributes_management(folder+"WAP_Points.shp", 'POINT_X_Y_Z_M', 'FEET_US', 'SQUARE_MILES_US')
	#create list of the WA ID's
	Combo = list()
	waplist = arcpy.da.TableToNumPyArray(folder+"WAP_Points.shp","WAPID")
	waplist = waplist.tolist()
	for ele in waplist:
		for name in ele:
			parts = name.split(',')
			Combo.append("LIB-234"+parts[0])
	print(Combo)
	#Update the WAPIDs with Exact required id == AMP system 
	features = arcpy.UpdateCursor(folder+"WAP_Points.shp")
	features.reset()
	for ele in range(len(Combo)):
		row = features.next()
		row.setValue("WAPID",Combo[ele])
		row.setValue("B.NAME",folder)
		features.updateRow(row)
			except:
				print(arcpy.GetMessage())    				