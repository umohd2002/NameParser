# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:57:31 2023

@author: Salman Khan
"""


from DB_Operations import DB_Operations
from sqlalchemy.orm import sessionmaker
from ORM import ComponentTable


database_url = 'sqlite:///KnowledgeBase_Test.db'
db_operations = DB_Operations(database_url)

class View_DataBase():
    def View_maskTable():
        mask_data = db_operations.get_Mask_data()
        print("Data from Mask Table:")
        for row in mask_data:
            print(f"Mask: {row.mask}")
    def View_componentTable():
        component_data = db_operations.get_Component_data()
        print("\nData from Component Table:")
        for row in component_data:
            print(f"Component: {row.component}, Description: {row.description}")
    def View_MappingJsonTable():
        MappingJSON_data = db_operations.get_MappingJSON_data()
        print("\nData from MappingJSON Table:")
        for row in MappingJSON_data:
            print(f"Mask: {row.mask_index}, Component: {row.component_index}, Token Index: {row.component_value}")
    View_maskTable()
    View_componentTable()
    View_MappingJsonTable()
View_DataBase()