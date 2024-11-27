# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 21:33:57 2023

@author: Salman Khan
"""


import re
# from tqdm import tqdm
# import pandas as pd
import json 
# import collections 
#Parsing 1st program
# import re
import os.path
import Rulebased as rulebased
import PreprocessingName as PreProc
from DB_Operations import DB_Operations

from datetime import datetime,timedelta
today=datetime.today()
current_time = datetime.now().time()
time_string = current_time.strftime("%H:%M:%S")
unique = timedelta(microseconds=-1)



file_dir = os.path.dirname(os.path.realpath('__file__'))


from pathlib import Path

root_folder = Path(__file__).parents[1]

ExceptionList = []



def throwException(originalInput):
    db_operations = DB_Operations(database_url='sqlite:///KnowledgeBase.db')
    clue = db_operations.get_clue_data_as_dict()
    ck = list(clue.keys())
    cv = list(clue.values())
    PackName=PreProc.PreProcessingNameName().NamesCleaning(originalInput)
    component_dict = {}
    component_dict = db_operations.get_components()
    NameList = PackName[0]
    NameList= [item for item in NameList if item]# != ","]
    rules=rulebased.RuleBasedNameParser.NameParser(NameList,ck,cv)
    # print("Rules: ",rules)
    for m in rules:
        component = m[1]
        if component not in component_dict.keys():
            m[1] = "USNM_NA"
            m.append("Not Selected")
        else:
            m.append(component_dict[component])
    # print("M: ",m)
    
    ID = "1"
    ExceptionDict = {
        "Record ID": ID,
        "INPUT": originalInput,
        str(Mask_1): rules
    }
    
    if ExceptionList:
        ExceptionList[0]= ExceptionDict
    
    else:
        ExceptionList.append(ExceptionDict)
    
    return True, ExceptionList


def Name_Parser(line,originalInput):
    global Result, Exception_file_name, FirstPhaseList, Mask_1, NameList, rules
    Result={}
    Exception_=False
    Exception_file_name=""
    
    # Strips the newline character
    Observation=0
    Total=0
    Truth_Result={}
    dataFinal={}
    FirstPhaseList=[]
    PackName=PreProc.PreProcessingNameName().NamesCleaning(line)
    NameList = PackName[0]
    NameList= [item for item in NameList if item]
    TrackKey=[]
    Mask=[]
    Combine=""
    LoopCheck=1
    ID = "1"
    component_dict = {}
    
    db_operations = DB_Operations(database_url='sqlite:///KnowledgeBase.db')
    clue = db_operations.get_clue_data_as_dict()
    ck = list(clue.keys())
    cv = list(clue.values())
    component_dict = db_operations.get_components()
    #print("\n Component Dict: ", component_dict)
    for A in NameList:
        FirstPhaseDict={}
        NResult=False
        try:
            Compare=A[0].isdigit()
        except:
            print()
        if A==",":
            Mask.append(Combine)
            Combine=""
            FirstPhaseList.append(",")
            #FirstPhaseList.append("Seperator")
        elif A==" ":
            continue
        elif A!="," and len(A)==1:
            
            NResult=True
            Combine+="I"
            TrackKey.append("I")
            FirstPhaseDict["I"] = A
            FirstPhaseList.append(FirstPhaseDict)
        else:
            
            for k in range(len(ck)):
                if A ==ck[k]:
                    # token1 = []
                    temp=cv[k]
                    NResult=True
                    Combine+=temp
                    FirstPhaseDict[temp] = A 
                    FirstPhaseList.append(FirstPhaseDict)
                    TrackKey.append(temp)
            if NResult==False:
                Combine+="W"
                TrackKey.append("W")
                FirstPhaseDict["W"] = A
                FirstPhaseList.append(FirstPhaseDict)
        if LoopCheck==len(NameList):
            Mask.append(Combine)
        
        LoopCheck+=1
    Mask_1=",".join(Mask)
    FirstPhaseList = [FirstPhaseList[b] for b in range(len(FirstPhaseList)) if FirstPhaseList[b] != ","]
    Found=False
    FoundDict={}
    if db_operations.check_mask_exists(Mask_1):
        FoundDict[Mask_1] = db_operations.get_data_for_mask(Mask_1)
        Found = True
    if Found:
        Observation+=1
        Mappings=[]
        uiMappings = []
        for K2,V2 in FoundDict[Mask_1].items():
            FoundDict_KB=FoundDict[Mask_1]
            sorted_Found={k: v for k ,v in sorted(FoundDict_KB.items(), key=lambda item:item[1])}
        dict_found={}
        print("+++++++sort=============",sorted_Found)
        for k,v in sorted_Found.items():
            for i in v:
                dict_found[i]=k
        nest_list=[]
        #print("dict",dict_found)
        mask=Mask_1.replace(",","")
        for i in range(0,len(FirstPhaseList)):
            token=""
            for k,v in FirstPhaseList[i].items():
                token=v
                component_description = component_dict[dict_found[i+1]]
            uiMappings.append([token,dict_found[i+1],mask[i],component_description])
        
        for K2,V2 in sorted_Found.items():
            Temp=""
            Merge_token=""
            for p in V2:
                for K3,V3 in FirstPhaseList[p-1].items():
                   Temp+=" "+V3
                   Temp=Temp.strip()      
                   Merge_token+= ""+K3
                   found = False
                   for entry in Mappings:
                       if entry[0] == K2:
                           
                           entry[1] += K3
                           entry[2] = ""
                           entry[2] += Temp
                           found = True
                           break
                   if not found:
                       Mappings.append([K2, K3, V3])
                       break

        FoundDict_KB=FoundDict[Mask_1]
        sorted_Found={k: v for k ,v in sorted(FoundDict_KB.items(), key=lambda item:item[1])}
                  
        try:
            Result["Input"]= originalInput
            Result["Output"]=uiMappings
            # messagebox.showinfo("Success!",f"{originalInput}\n\nName Successfully Parsed!\n\nOutput derived from Active Learning")
        except:
            Result["Input"]= originalInput
            Result["Output"]=uiMappings
            # messagebox.showinfo("Success!",f"{originalInput}\n\nName Successfully Parsed!\n\nOutput derived from Active Learning")

        
        
        OutputDict = {
                "Record ID": ID,
                "INPUT": originalInput,
                str(Mask_1): Mappings
            }
        
    else:
        Exception_=True
        rules=rulebased.RuleBasedNameParser.NameParser(NameList, ck, cv)
        # print(rules)
        ExceptionDict = {
            "Record ID": ID,
            "INPUT": originalInput,
            str(Mask_1): rules
        }
        Result["Input"]=originalInput
        Result["Output"]=rules
        for m in Result["Output"]:
            
            component = m[1]
            if component not in component_dict.keys():
                m[1] = "USNM_NA"
                m.append("Not Selected")
            else:
                m.append(component_dict[component])
        
        if ExceptionList:
            ExceptionList[0] = ExceptionDict
            
        else:
            ExceptionList.append(ExceptionDict)
            
        
       
        
        
    Total+=1
   
    return (Result, Mask_1,Exception_file_name, throwException,Exception_)