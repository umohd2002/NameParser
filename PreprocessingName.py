# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 12:50:21 2023

 

@author: onais
"""

import re

 

 

class PreProcessingNameName:
    def __init__(self):
        self
    def NamesCleaning(self,line):
        line=line.lstrip(',')
        line=re.sub(r'[^a-zñáéíóúüÑÁÉÍÓÚÜA-Z\s,-]+', '',line)

        Name=re.sub(' +', ' ',line)
        Name=re.sub(',',' , ',Name)
        
        Name=Name.upper()

        NameList = re.split(r"\s|\s,\s", Name)
        try:
            NameList.remove("")
        except:
            True


        return (NameList,Name)
    
