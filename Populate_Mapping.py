# -*- coding utf-8 -*-
"""
Created on Sat Mar  5 05:51:15 2022

@author: onais
"""

import re
from tqdm import tqdm
import pandas as pd
import json 
import os

# specify the directory path
dir_path_Multiple = 'Exceptions/MultiLine Exceptions/'
dir_path_Single = 'Exceptions/SingleException/'

# list all files in the directory
file_Single = os.listdir(dir_path_Single)
file_multiple = os.listdir(dir_path_Multiple)


# print the list of files

print("Select One Option")

print("1. Single Exception")
print("2. Multi Line Exception")
option1=int(input("Enter your option"))
Single_file_dict={}
Multi_file_dict={}

Multi_option1=0
Single_option1=0

if option1==1:
    i=1
    for file in file_Single:
        Single_file_dict[i]=file
        print(str(i)+" )---- "+file)
        i+=1
    print("0 )---- to EXIT")
    Single_option1=int(input("Enter index of the file"))



elif option1==2:
    
    i=1
    for file in file_multiple:
        Multi_file_dict[i]=file
        print(str(i)+" )---- "+file)
        i+=1
    print("0 )---- to EXIT")
    Multi_option1=int(input("Enter index of the file"))


    
FileName=""

if Multi_option1:
    FileName="Exceptions/MultiLine Exceptions/"+Multi_file_dict[Multi_option1]


elif Single_option1:
    FileName="Exceptions/SingleException/"+Single_file_dict[Single_option1]

#hg
DF=[]
ii=0
count = 0
FinalList=[]
# Strips the newline character
DF=pd.DataFrame()
C=1
CC=1
JsonData={}
AllAddress_Key_Value_As_MASK_Comp={}
USAD_Conversion_Dict={"1":"USAD_SNO","2":"USAD_SPR","3":"USAD_SNM","4":"USAD_SFX","5":"USAD_SPT","6":"USAD_ANM","7":"USAD_ANO","8":"USAD_CTY","9":"USAD_STA","10":"USAD_ZIP","11":"USAD_ZP4","12":"USAD_BNM","13":"USAD_BNO","14":"USAD_RNM","15":"USAD_RNO","16":"USAD_ORG","17":"USAD_MDG","18":"USAD_MGN","19":"USAD_HNM","20":"USAD_HNO"}
USAD_Conversion_Dict_Detail={"1":"USAD_SNO Street Number","2":"USAD_SPR Street Pre-directional","3":"USAD_SNM Street Name","4":"USAD_SFX Street Suffix","5":"USAD_SPT Street Post-directional","6":"USAD_ANM Secondary Address Name","7":"USAD_ANO Secondary Address Number","8":"USAD_CTY City Name","9":"USAD_STA State Name","10":"USAD_ZIP Zip Code","11":"USAD_ZP4 Zip 4 Code","12":"USAD_BNM Box Name","13":"USAD_BNO Box Number","14":"USAD_RNM Route Name","15":"USAD_RNO Route Number","16":"USAD_ORG Organization Name","17":"USAD_MDG Military Rd Name","18":"USAD_MGN Military Rd Number","19":"USAD_HNM Highway Name","20":"USAD_HNO Highway Number"}
i=1
List_Index_Mask={}



print()

with open(FileName,'r+') as d:
    FirstPhaseLisCopyt=json.load(d)
    FirstPhaseList=FirstPhaseLisCopyt
    AddOrRemove=False
    MaskComparision={}
    for Key, Value in FirstPhaseLisCopyt.items():
        for Key1,Key2 in MaskComparision.items():
            if(Key==Key1):
                FirstPhaseList.pop(Key)
    Break=False
    print()
    
    for Key,Value in list(FirstPhaseList.items()):
        MaskI=1
        USAD_Mapping={"USAD_SNO":[],"USAD_SPR":[],"USAD_SNM":[],"USAD_SFX":[],"USAD_SPT":[],"USAD_ANM":[],"USAD_ANO":[],"USAD_CTY":[],"USAD_STA":[],"USAD_ZIP":[],"USAD_ZP4":[],"USAD_BNM":[],"USAD_BNO":[],"USAD_RNM":[],"USAD_RNO":[],"USAD_ORG":[],"USAD_MDG":[],"USAD_MGN":[],"USAD_HNO":[],"USAD_HNM":[]}
        USAD_Mapping_Tokens={"USAD_SNO":"","USAD_SPR":"","USAD_SNM":"","USAD_SFX":"","USAD_SPT":"","USAD_ANM":"","USAD_ANO":"","USAD_CTY":"","USAD_STA":"","USAD_ZIP":"","USAD_ZP4":"","USAD_BNM":"","USAD_BNO":"","USAD_RNM":"","USAD_RNO":"","USAD_ORG":"","USAD_MDG":"","USAD_MGN":"","USAD_HNO":"","USAD_HNM":""}
        Address=""
        for k in Value:
            for m,n in k.items():
                Address+=" "+n
    
        for k in Value:
            for k1,v1 in USAD_Conversion_Dict_Detail.items():
                print(v1,"=",k1)
            print("Address For Reference")
            print(Address)
            print(k)
            token=""
            for ke,v in k.items():
                token=v
            temp=(input("---> (Enter Index of Component)"))
            if temp not in USAD_Conversion_Dict_Detail.keys():
                Break=True
                break
            USAD_Mapping_Tokens[USAD_Conversion_Dict[temp]]+=" "+token
            USAD_Mapping_Tokens[USAD_Conversion_Dict[temp]]=USAD_Mapping_Tokens[USAD_Conversion_Dict[temp]].strip()
            USAD_Mapping[USAD_Conversion_Dict[temp]].append(MaskI)
            MaskI+=1
        dict2={k: v for k, v in USAD_Mapping_Tokens.items() if v}
        print(dict2)
        dict={k: v for k, v in USAD_Mapping.items() if v}
        print(dict)
        list_of_dict=[Address,dict2,dict]
        
        dictData={}
        dictData[Key]=dict
        Count_Of_Masks=0
        if Break:
            break
        with open('DisplayFile.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
            Count_Of_Masks=len(data)+1
          
            data[Key] =list_of_dict # <--- add `id` value.
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f,indent=4)
            f.truncate()# remove remaining part
        # FirstPhaseList.pop(Key)
        d.seek(0)        # <--- should reset file position to the beginning.
        json.dump(FirstPhaseList, d,indent=4)
        d.truncate()# remove re
    


        # print("Mask Generated is ",Mask_1)
    # print("Index\tMaskToken\t\tAddress Token")
    # i=1
    # for k in FirstPhaseList:
    #     for key,value in k.items():
    #         print(i,"\t\t",key,"\t\t\t\t",value) 
    #     i+=1