# Importing Module 
import pandas as pd
import numpy as np
import xml.etree.cElementTree as ET
import re
import datetime
import os
import sqlite3

# Parsing XMl in Python
# tree=ET.parse('assignment-data.xml') #Parsing Xml file
tree=ET.parse('assignment-data.xml')     #Parsing from demo Xml file 
root=tree.getroot()          # getting root elelmts of XMl
root.tag                   #Getting tag from root
root.attrib                #getting attribute 
path="sanction_data1.txt"
q_path="sanction_queries.txt"
ppath="plcae_data.txt"
q_ppath="plcae_quries.txt"


# -------------------------------- swiss-sanctions-list --------------------------
san_program = tree.findall('sanctions-program')
sanctions={}
#accessing each sanction Tag
for sanction_tag in san_program:    
    ssid=sanction_tag.attrib["ssid"] 
    v_date=sanction_tag.attrib["version-date"]  
    pre_v_date=sanction_tag.attrib["predecessor-version-date"]
    #ssid,v_date,pre_v_date are attributes if each sanction tag
    #therefor acess attributes with key
    #create dictionary to store data 
    #add ssid as key and its values will be another dictionary
    sanctions[ssid]={}
    sanctions[ssid]["v_date"]=v_date
    sanctions[ssid]["pre_v_date"]=pre_v_date
    #added v_date and pre_v_date in the ssid dicionary
    sanctions[ssid]["sanc_data"]=[]
    #tags inside the main sanction tag are the data for the sanction
    #sanc_data is the key inside
    #store the values/data in the array/List with 
    for sanction_inner_tag in range(0,len(sanction_tag)):
        value=sanction_tag[sanction_inner_tag].text
        if value == "":
            value="-"
        else:
            sanctions[ssid]["sanc_data"].append(value)
fh=open(path,"a")
fh.write("ssid|version_date|predecessor_version_date|key|name|set|origin\n")
for ssid in sanctions:
    ver_date=str(sanctions[ssid]["v_date"])
    pre_ver_date=str(sanctions[ssid]["pre_v_date"])
    values_list=sanctions[ssid]["sanc_data"]
    if len(values_list) == 13:
        fh.write("%s|%s|%s|%s|%s|%s|%s\n"%(ssid,ver_date,pre_ver_date,values_list[0],values_list[4],values_list[8],values_list[12]))
        fh.write("%s|%s|%s|%s|%s|%s|%s\n"%(ssid,ver_date,pre_ver_date,values_list[1],values_list[5],values_list[9],values_list[12]))
        fh.write("%s|%s|%s|%s|%s|%s|%s\n"%(ssid,ver_date,pre_ver_date,values_list[2],values_list[6],values_list[10],values_list[12]))
        fh.write("%s|%s|%s|%s|%s|%s|%s\n"%(ssid,ver_date,pre_ver_date,values_list[3],values_list[7],values_list[11],values_list[12]))
        
fh.close()
fh=open(path,"r")
wfh=open(q_path,"a")
header=0
for line in fh:
    if header == 0:
        header=1
    else:
        line=line.lstrip()
        line=line.rstrip()
        array=[]
        array=re.split("\|",line)
#         print(array[1])
        wfh.write("insert into sanction_table (ssid,version_date,predecessor_version_date,key,name,set,origin) values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")\n"%(array[0],array[1],array[2],array[3],array[4],array[5],array[6]))
fh.close() 
wfh.close()

san_places = tree.findall('place')
places={}
for san_placestag in san_places:
    ssid=san_placestag.attrib["ssid"]
    places[ssid]={}
    #added v_date and pre_v_date in the ssid dicionary
    places[ssid]["place_data"]=[]
    #tags inside the main sanction tag are the data for the sanction
    #sanc_data is the key inside
    #store the values/data in the array/List with 
    for places_inner_tag in range(0,6):
        print(places_inner_tag)
        try:
            value=san_placestag[places_inner_tag].text
            if value == "":
                places[ssid]["place_data"].append("-")
            else:
                places[ssid]["place_data"].append(value)
        except IndexError:
            places[ssid]["place_data"].append("-")

# print(str(places))

fh=open(ppath,"a")
fh.write("ssid|location|location-variant|area|area-variant|country\n")
for ssid in places:
    values_list=places[ssid]["place_data"]
    if len(values_list) == 6:
        fh.write("%s|%s|%s|%s|%s|%s\n"%(ssid,values_list[0],values_list[1],values_list[2],values_list[3],values_list[4]))

fh.close()
fh=open(ppath,"r")
wfh=open(q_ppath,"a")
header=0
for line in fh:
    if header == 0:
        header=1
    else:
        line=line.lstrip()
        line=line.rstrip()
        array=[]
        array=re.split("\|",line)
#         print(array[1])
        wfh.write("insert into place_table (ssid,location,location-variant,area,area-variant,country) values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")\n"%(array[0],array[1],array[2],array[3],array[4],array[5]))
fh.close() 
wfh.close()


#------------------ import sqlite3
con = sqlite3.connect("swisssanctionslist.db")
cur = con.cursor()

#---------------------- Open Txt file for data insert in Databse
sanction=open(q_path,"r")
places=open(q_ppath,"r") 

header=0
for line in sanction:
    if header == 0:
        header=1
    else:
        line=line.lstrip()
        line=line.rstrip()

for lines in places:
    if header == 0:
        header=1
    else:
        lines=lines.lstrip()
        lines=lines.rstrip()

cur = con.cursor()

#------------ Creating DB Table sabction
cur.execute("CREATE TABLE Sanction(ssid, version_date, predecessor_version_date, Program_key, Program_name, Program_set, origin)")

cur.execute('''/S'''%line)

#----------cretaing DB table for Places
cur.execute("CREATE TABLE Places(ssid,location,location-variant,area,area-variant,country)")
cur.execute('''/S'''%lines)

#----closing text File after DB insertion
sanction.close() 
places.close()

con.close()

