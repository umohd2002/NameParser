# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:46:17 2023

@author: Salman Khan
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import json
from ORM import MaskTable, ComponentTable, MappingJSON, User, UserRole, ExceptionTable, MapCreationTable, ClueTable
# from LoginORM import UserRole, User

class DB_Operations:
    def __init__(self, database_url):
        self.database_url = database_url
        self.engine = create_engine(database_url)

    def open_database(self):
        return self.engine
    
    def check_mask_exists(self, mask):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            mask_record = session.query(MaskTable).filter_by(mask=mask).first()
            if mask_record: 
                return bool(mask_record)
            else:
                pass# print("Mask Not Found")
        finally:
            session.close()
    
    def get_clue_data_as_dict(self):
   
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            # Query all records from ClueTable
            clue_records = session.query(ClueTable).all()
            
            # Create a dictionary from the queried data
            clue_dict = {record.component_desc: record.token for record in clue_records}
            
            # Return the dictionary
            #print(clue_dict)
            return clue_dict
        
        
        finally:
            # Ensure session is closed
            session.close()

    def transfer_data(self, data):
        Session = sessionmaker(bind=self.engine)
        # session = None
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
            # print(f"Error: {e}")

        finally:
            if session is not None:
                session.close()

    def get_data_for_mask(self, mask):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            mask_record = session.query(MaskTable).filter_by(mask=mask).first()
    
            if mask_record:
                data_records = session.query(MappingJSON).filter_by(mask_index=mask_record.mask).order_by(MappingJSON.component_value).all()

                result_dict = {}
                # for record in data_records:
                #     result_dict[record.component_value] = record.component_index
                for record in data_records:
                    if record.component_index not in result_dict:
                        result_dict[record.component_index] = [record.component_value]
                    else:
                        result_dict[record.component_index].append(record.component_value)

                # print(result_dict)
                return result_dict
            else:
                pass
        finally:
            session.close()

    def get_data_for_all(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            mask_record = session.query(MaskTable).all()
            main_dict = {}
            for record in mask_record:
                data_records = session.query(MappingJSON).filter_by(mask_index=record.mask).order_by(MappingJSON.component_value).all()
                result_dict = {}
                for data_record in data_records:
                    if data_record.component_index not in result_dict:
                        result_dict[data_record.component_index] = [data_record.component_value]
                    else:
                        result_dict[data_record.component_index].append(data_record.component_value)
                main_dict[record.mask] = result_dict
            return main_dict
        finally:
            session.close()

    def get_component_description(self, component):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:

            component_record = session.query(ComponentTable).filter_by(component=component).first()

            if component_record:
                return component_record.description
            else:
                return "Not Selected"

        finally:
            session.close()
    
    def get_components(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:

            component_record = session.query(ComponentTable).all()
            component_dict = {}
            for data in component_record:
                if data.component not in component_dict:
                    component_dict[data.component] = data.description
            return component_dict

        finally:
            session.close()

    
    def get_Mask_data(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            return session.query(MaskTable).all()

        finally:
            session.close()

    def get_Component_data(self):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            return session.query(ComponentTable).all()

        finally:
            session.close()

    def get_MappingJSON_data(self):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            return session.query(MappingJSON).all()

        finally:
            session.close()

    def get_deleted_MappingJSON(self,component):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            return session.query(MappingJSON).all()

        finally:
            session.close()
            
            
    def authenticate_user(self,username, password):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        user = session.query(User).filter_by(username=username).first()
        if user and user.password == password:  # You should use hash comparison here for security!
            return user
        return None

    

    def add_data(self, data):
        Session = sessionmaker(bind=self.engine)
        session = None
        #print('data',data)
        try:
            session = Session()
            for mask, components in data.items():
                try:
                    mask_record = session.query(MaskTable).filter_by(mask=mask).first()
                    if not mask_record:
                        mask_record = MaskTable(mask=mask)
                        session.add(mask_record)
                    session.flush()
    
                    mask_id = mask_record.mask
                    #print("componentss",components)
                    for value , component_description in components.items():
                        try:
                            component_record = session.query(ComponentTable).filter_by(description=component_description).first()
                            if not component_record:
                                pass
                            #print('values',value)
                            
                            try:
                                mapping_json_record = session.query(MappingJSON).filter_by(
                                    mask_index=mask_id,
                                    component_value=value
                                    ).first()
                                if mapping_json_record:
                                    mapping_json_record.component_index=component_record.component
                                    mapping_json_record.component_value = value

                                else:
                                    mapping_json_record = MappingJSON(
                                        mask_index=mask_id,
                                        component_index=component_record.component,
                                        component_value=value
                                    )
                                    session.add(mapping_json_record)
                            except IntegrityError as e:
                                    session.rollback()
                                    error_info = e.orig.args[0]
                                    if 'UNIQUE constraint failed' in error_info:
                                        print("Error: Duplicate entry. The combination of mask, component, and value must be unique.")
                                    else:   
                                        print(f"Error: {e}")
                                    continue
                        except IntegrityError as e:
                                    session.rollback()
                                    error_info = e.orig.args[0]
                                    if 'UNIQUE constraint failed' in error_info:
                                        print("Error: Duplicate entry. The combination of mask, component, and value must be unique.")
                                    else:   
                                        print(f"Error: {e}")
                                    continue
                except IntegrityError as e:
                            session.rollback()
                            error_info = e.orig.args[0]
                            if 'UNIQUE constraint failed' in error_info:
                                print("Error: Duplicate entry. The combination of mask, component, and value must be unique.")
                            else:   
                                print(f"Error: {e}")
                            continue
                
            session.commit()

        except IntegrityError as e:
            error_info = e.orig.args[0]
            if 'UNIQUE constraint failed' in error_info:
                print("Error: Duplicate entry. The combination of mask, component, and value must be unique.")
                duplicate_data = []
                for mask, components in data.items():
                    duplicate_data.append({mask: components})
                with open('duplicate_data.json', 'a') as file:
                    json.dump(duplicate_data, file)
                    file.write('\n')
                print("Duplicate Dictionaries are added to the file")
            else:
                print(f"Error: {e}")
            
        finally:
            if session is not None:
                session.close()


    def update_component_descriptions_interactively(self):
            try:
                Session = sessionmaker(bind=self.engine)
                session = Session()

                components = session.query(ComponentTable).all()

                for component in components:
                    current_description = component.description
                    new_description = input(f"Enter new description for component {component.component} (current: {current_description}): ")

                    if new_description:
                        component.description = new_description
                        print(f"Description updated for component {component.component}")
                    else:
                        print(f"Description for component {component.component} unchanged.")

                # Commit the changes
                session.commit()

            finally:
                if session is not None:
                    session.close()
    def Delete_records(self, component):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            
            component_record = session.query(ComponentTable).filter_by(component=component).first()
            
            if component_record:
                # Fetch all mask indices associated with the component
                linked_masks = session.query(MappingJSON).filter_by(component=component_record.component).all()
                
                # Delete records in the MappingJSON table first
                for mask in linked_masks:
                    session.query(MappingJSON).filter_by(component_index=component_record.component).delete()
                
                # Fetch masks associated with the component and delete them from MaskTable
                for mask in linked_masks:
                    mask_record = session.query(MaskTable).filter_by(mask=mask.mask).first()
                    if mask_record:
                        session.delete(mask_record)
                
                # Finally, delete the component from ComponentTable
                session.delete(component_record)
                session.commit()
            
        finally:
            session.close()

    def add_mapCreation(self, data, excdata, app):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            # Check for existing records in MapCreationTable and ExceptionTable for the same mask
            existing_map = session.query(MapCreationTable).filter_by(Mask=data["Mask"]).first()

            if existing_map:
                # Delete related exceptions in ExceptionTable
                session.query(ExceptionTable).filter_by(MapCreation_Index=existing_map.Mask).delete()

                # Delete the map record in MapCreationTable
                session.delete(existing_map)
                session.commit()
                app.logger.info(f"Existing records for Mask {data['Mask']} deleted successfully.")

            # Add the new map creation entry
            mapdata = MapCreationTable(Name_Input=data["Name Input"], Mask=data["Mask"])
            session.add(mapdata)
            session.commit()  # Commit to generate the ID for `mapdata.Mask`

            # Prepare and add new exceptions
            exc_entries = [
                ExceptionTable(
                    UserName=excdata["Username"],
                    Timestamp=excdata["Timestamp"],
                    Run=excdata["Run"],
                    Name_ID=excdata["Record ID"],
                    Component=i[1],
                    Token=i[0],
                    Mask_Token=i[2],
                    Component_index=index,
                    MapCreation_Index=mapdata.Mask
                )
                for index, i in enumerate(excdata["data"], start=1)
            ]

            session.bulk_save_objects(exc_entries)
            session.commit()
            app.logger.info(f"New map creation and exceptions added successfully for Mask: {data['Mask']}.")

        except Exception as e:
            session.rollback()  # Rollback changes on any error
            app.logger.error(f"Error in add_mapCreation: {e}")
            raise  # Re-raise the exception for visibility

        finally:
            session.close()  # Ensure the session is closed


            
    
# database_url = 'sqlite:///KnowledgeBase_TestDummy.db'
# db_operations = DB_Operations(database_url)
# db_operations.Delete_records('USAD_SFX')
