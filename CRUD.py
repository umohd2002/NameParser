# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:59:53 2023

@author: Salman Khan
"""

# main.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
# import json
# from ORM import MaskTable, ComponentTable, MappingJSON, User, UserRole, ExceptionTable, MapCreationTable
import json
from DB_Operations import DB_Operations
from ORM import User,UserRole,MaskTable, ComponentTable, MappingJSON, ExceptionTable, MapCreationTable

from sqlalchemy import create_engine

def read_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    dictionary_file_path = r"C:\Users\skhan2\Desktop\Census Bureau Research\NameAndAddressParser\Name And Address Parser\JSONMappingDefault.json"

    data= read_data_from_file(dictionary_file_path)
    Session = sessionmaker(create_engine('sqlite:///KnowledgeBase_Test.db'))
    session = Session()
    try:
        for mask, components in data.items():
            # Add new mask to MaskTable if not exists
            mask_record = session.query(MaskTable).filter_by(mask=mask).first()
            if not mask_record:
                mask_record = MaskTable(mask=mask)
                session.add(mask_record)
                session.commit()
            session.flush()

            mask_id = mask_record.mask

            for component_key, values in components.items():
                # Add new component to ComponentTable if not exists
                component_record = session.query(ComponentTable).filter_by(component=component_key).first()
                if not component_record:
                    component_record = ComponentTable(component=component_key)
                    session.add(component_record)
                    session.commit()
                session.flush()

                for value in values:
                    # Check if mapping already exists
                    mapping_json_record = session.query(MappingJSON).filter_by(
                        mask_index=mask_id,
                        component_index=component_record.component,
                        component_value=value
                    ).first()
                    if not mapping_json_record:
                        # Add new mapping
                        new_mapping = MappingJSON(
                            mask_index=mask_id,
                            component_index=component_record.component,
                            component_value=value
                        )
                        session.add(new_mapping)
                        session.commit()

        # session.commit()

    except IntegrityError as e:
        # Handle any integrity errors during commit
        session.rollback()
        print(f"Error: {e}")

    finally:
        if session is not None:
            session.close()
