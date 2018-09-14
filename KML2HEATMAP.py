"""
KML2HEATMAP.py
v0.1   14.09.2018
Landon Halloran 

A python script that creates a javascript-based html heatmap from longitude, latitude
coordinate pairs contained in kml files. See the readme.md...
"""

import os
import xml.etree.ElementTree as ET

################################################
# PLEASE DEFINE THESE INPUTS
myAPI='AIzaSyDq8TuSdMWVCeFwCUIFUQ_mbNZfVozysPY' # Sorry, you have to get your own!
kml_folder='example_kml_files/'
init_long=6.9
init_lat=47
init_zoom=12
fileoutname='example_output.html'
################################################

# read in header and footer for html:
hhtml = open('header_html.txt','r')
headercode = hhtml.read()
hhtml.close()
headercode=headercode.replace('###LONG###',str(init_long))
headercode=headercode.replace('###LAT###',str(init_lat))
headercode=headercode.replace('###ZOOM###',str(init_zoom))
fhtml = open('footer_html.txt','r')
footercode = fhtml.read()
fhtml.close()
footercode=footercode.replace('###API###',myAPI)

files = []

for file in sorted(os.listdir(kml_folder)):
    files.append(file)

XYZ=[]
for file in files:
    tree = ET.parse(kml_folder+file)
    # adapted from https://stackoverflow.com/questions/45863208/how-to-get-a-list-of-coordinates-from-a-kml-file-in-python
    lineStrings = tree.findall('.//{http://www.opengis.net/kml/2.2}LineString')
    for attributes in lineStrings:
        for subAttribute in attributes:
            if subAttribute.tag == '{http://www.opengis.net/kml/2.2}coordinates':
                #print(subAttribute.text)
                coordtext=subAttribute.text
                coordtext1=coordtext.split()
                for c in coordtext1:
                    cc=c.split(',')
                    XYZnow = list(map(lambda x: float(x.replace(",", "")), cc))
                    XYZ.append(XYZnow)

f = open(fileoutname, 'w')
f.write(headercode)
for XYZline in XYZ[:-1]: #write all but last
    X=str(XYZline[0])
    Y=str(XYZline[1])
    stringout='new google.maps.LatLng('+Y+', '+X+'),\n'
    f.write(stringout)  # python will convert \n to os.linesep
XYZlast=XYZ[-1]
X=str(XYZline[0])
Y=str(XYZline[1])
stringout='new google.maps.LatLng('+Y+', '+X+')\n'
f.write(stringout)  # python will convert \n to os.linesep
f.write(footercode)
f.close()
print('KML files parsed and exported to file: '+ fileoutname)
