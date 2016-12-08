import arcpy
from arcpy import env
import os
path = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/CADFiles/";
gdb_path ="C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/"
gdb = "NIS-CAD.gdb"
env.workspace = "C:/Users/sachin77/Documents/ArcGIS/Projects/NIS-CAD/"
op_gdb_path = os.path.join(gdb_path, gdb);
print(op_gdb_path);
reference_scale = "10"
#arcpy.CreateFeatureclass_management(gdb_path,"WapPoints")
path2features = list()
cadBlockRefNames = list(tuple());
for (path,folders,files) in os.walk(path):
	if folders is not empty:
		print(folders)
cnt = 0;
for file in os.listdir(path):
	if file.endswith(".dwg"):
		print("found " + file)
		input_file = os.path.join(path,file)
		try:
			arcpy.CADToGeodatabase_conversion(input_file,path,file[:-4],reference_scale)
			path2features.append(gdb_path+gdb+'\\'+file[0:len(file) -4]);
			if cnt==0:
				arcpy.Select_analysis(path2features[cnt]+"\\" + "Point","tempPoint", "\"Layer\" = 'E-COMM-WIRELESS'")
				infoNLRef = arcpy.da.TableToNumPyArray("tempPoint.shp","RefName")
				infoNLRef = set(infoNLRef[0])
				infoNLRef = tuple(infoNLRef)
				cadBlockRefNames.append(infoNLRef)
				arcpy.Delete_management("tempPoint.shp")
				print(cadBlockRefNames)
				for featureCls in cadBlockRefNames[cnt]:
					arcpy.Select_analysis(path2features[cnt]+"\\" +featureCls ,"temp1", "\"Layer\" = 'E-COMM-WIRELESS'")
					infoNLWAP = arcpy.da.TableToNumPyArray("temp1.shp","PORTAL")
					print(infoNLWAP)				
					arcpy.Select_analysis(path2features[cnt]+"\\" + "Annotation","temp2", "\"Layer\" = 'E-COMM-WIRELESS'")
					AnnoNLWAP = arcpy.da.TableToNumPyArray("temp2.shp","Text")
					print(AnnoNLWAP)
					arcpy.Merge_management(["temp1.shp","temp2.shp"], "NewmanWapPoints.shp")
					arcpy.DeleteFeatures_management("temp1.shp")
					arcpy.DeleteFeatures_management("temp2.shp")
					

					#creating combine list
					infoNLWAP = infoNLWAP.tolist()
					infoNLWAP = set(infoNLWAP)
					infoNLWAP = list(infoNLWAP)

					AnnoNLWAP = AnnoNLWAP.tolist()
					AnnoNLWAP = set(AnnoNLWAP)
					AnnoNLWAP = list(AnnoNLWAP)
					Combo = list();
					waplist = [infoNLWAP,AnnoNLWAP];
					for ele in waplist:
						for name in ele:
							parts = name[0].split(',');
							Combo.append(parts[0]);
					print(Combo)
					Combo.sort();
					Combo = set(Combo);
					Combo = list(Combo)
					exportName = gdb_path+file[0:len(file)-4]+"_WapPoints"+".txt"
					tf= open(exportName,"w")
					for wapid in Combo: 
						if wapid != ' ':
								tf.write("LIB-234{} \n".format(wapid))
					tf.close()
					cnt = cnt+1;				
			else:
				arcpy.Select_analysis(path2features[cnt]+"\\" + "Point"+str(cnt),"tempPoint", "\"Layer\" = 'E-COMM-WIRELESS'")
				infoNLRef = arcpy.da.TableToNumPyArray("tempPoint.shp","RefName")
				infoNLRef = set(infoNLRef[0])
				infoNLRef = tuple(infoNLRef)
				cadBlockRefNames.append(infoNLRef)
				arcpy.Delete_management("tempPoint.shp")
				print(cadBlockRefNames)
				for featureCls in cadBlockRefNames[cnt]:
					arcpy.Select_analysis(path2features[cnt]+"\\" +featureCls+str(cnt) ,"temp1", "\"Layer\" = 'E-COMM-WIRELESS'")
					infoNLWAP = arcpy.da.TableToNumPyArray("temp1.shp","PORTAL")
					print(infoNLWAP)				
					arcpy.Select_analysis(path2features[cnt]+"\\" + "Annotation" + str(cnt),"temp2", "\"Layer\" = 'E-COMM-WIRELESS'")
					AnnoNLWAP = arcpy.da.TableToNumPyArray("temp2.shp","Text")
					print(AnnoNLWAP)
					arcpy.Merge_management(["temp1.shp","temp2.shp"], "NewmanWapPoints.shp")
					arcpy.DeleteFeatures_management("temp1.shp")
					arcpy.DeleteFeatures_management("temp2.shp")
					infoNLWAP = infoNLWAP.tolist()

					#creating combine list
					infoNLWAP = set(infoNLWAP)
					infoNLWAP = list(infoNLWAP)

					AnnoNLWAP = AnnoNLWAP.tolist()
					AnnoNLWAP = set(AnnoNLWAP)
					AnnoNLWAP = list(AnnoNLWAP)
					Combo = list();
					waplist = [infoNLWAP,AnnoNLWAP];
					for ele in waplist:
						for name in ele:
							parts = name[0].split(',');
							Combo.append(parts[0]);
					print(Combo)
					Combo = set(Combo);
					Combo = list(Combo)
					Combo.sort();
					exportName = gdb_path+file[0:len(file)-4]+"_WapPoints"+".txt"
					print(exportName);
					tf= open(exportName,"w")
					for wapid in Combo: 
						if wapid != ' ':
								tf.write("LIB-234{} \n".format(wapid))
					tf.close()
					cnt = cnt+1;
		except:
			print(arcpy.GetMessage())