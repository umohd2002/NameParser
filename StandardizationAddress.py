# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:04:17 2022

@author: onais
"""
import json

Stdfile=open("Standardization_Codes.txt","r")
def StdAddress(Address):
    Tr=False
    StAd=Stdfile.readlines()
    for key,value in list(Address.items()):
        for i in StAd:
            cmp=i.strip("\n").split("|")
            if key==cmp[0] and value==cmp[1]:
                Address[key]=cmp[2]
        if key=="USAD_ZIP":
            if "-" in value:
                zipc=value.split("-")
                Address["USAD_ZIP"]=zipc[0]
                Address["USAD_ZIP4"]=zipc[1]
        
    return Address

Address=json.load(open("ConvertedJSONAddressesOutput.json","r"))

for i in Address.items():
    print(StdAddress(i[1]))
    print("\n\n")