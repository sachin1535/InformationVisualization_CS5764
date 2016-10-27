# NI&S CAD-GIS Translation for Wireless Access Points


## Algorithm pseudocode


```python
create destination feature class for merged points

        geometry type: point

        projection: (probably State Plane VA South 4502 coord system)

        fields: {field1, field2, field3, field4, field5, DWG_NAME, BLDG, FLOOR, AMP_ID}

 

        foreach building_dir in cad_dir:

                foreach dwg in building_dir:

                In <filename.dwg> Point:

                        write output columns for

                                source DWG Name,

                                [derived] building ID

                                derived] floor number

                        select RefName where Layer = E-COMM-WIRELESS

                        Foreach RefName:

                                select all points in <filename>.dwg <RefName> as refNamePoints

                        Select all points in <filename>.dwg Annotation where Layer = E-COMM-WIRELESS as annotationPoints

                        Union annotationPoints and refNamePoints as unionSet

                        dump all points and their attributes into destination feature class

                        for attribute n in unionSet.count(attributes):       

                                destination.field<n>= union set.n

 

# now, iterating over the new feature class with all the merged points and attributes:

foreach feature i:
        foreach attribute column:
                attempt to figure out which attribute contains a WAP ID formatted string

                crack apart comma separated names

                foreach comma separated name part c

                        do concatenation to match aMP formatting

                        query the AMP WAP list to see if there is a match

                        if yes:

                                destination[i].AMP_ID =c
								
```