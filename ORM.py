# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:09:42 2023

@author: Salman Khan
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import PrimaryKeyConstraint
import bcrypt
import uuid

Base = declarative_base()

engine = create_engine('sqlite:///KnowledgeBase.db')

Session = sessionmaker(bind=engine)
session = Session()

class MaskTable(Base):
    __tablename__ = 'maskTable'
    mask = Column(String, primary_key=True)
    # index = Column(Integer, unique=True)
    
    mapping_json = relationship('MappingJSON', back_populates='mask', cascade='all, delete-orphan', single_parent=True)

class ComponentTable(Base):
    __tablename__ = 'componentTable'
    # id = Column(Integer, primary_key=True)
    component = Column(String, primary_key=True)
    # index = Column(Integer, unique=True)
    description = Column(String)
    
    mapping_json = relationship('MappingJSON', back_populates='component', cascade='all, delete-orphan', single_parent=True)
    exceptions = relationship('ExceptionTable', back_populates='component', cascade='all, delete-orphan', single_parent=True)

class MappingJSON(Base):
    __tablename__ = 'mappingJSON'
    # id = Column(Integer, primary_key=True)
    mask_index = Column(String, ForeignKey('maskTable.mask'))
    component_index = Column(String, ForeignKey('componentTable.component'))
    component_value = Column(Integer)

    mask = relationship('MaskTable', foreign_keys=[mask_index], back_populates='mapping_json')
    component = relationship('ComponentTable', foreign_keys=[component_index], back_populates='mapping_json')
    
    __table_args__ = (
        PrimaryKeyConstraint('mask_index','component_value'),
    )
    
    def __eq__(self, other):
        if isinstance(other, MappingJSON):
            return (
                self.mask_index == other.mask_index and
                self.component_index == other.component_index and
                self.component_value == other.component_value
            )
        return NotImplemented


class ExceptionTable(Base):
    __tablename__ = 'exceptionTable'
    UserName = Column(String, ForeignKey('usersTable.UserName'))
    Timestamp = Column(String)
    Run = Column(String)
    Name_ID = Column(Integer) 
    Component = Column(String, ForeignKey('componentTable.component'))
    Token = Column(String)
    Mask_Token = Column(String)
    Component_index = Column(Integer)
    MapCreation_Index = Column(Integer, ForeignKey('mapCreationTable.Mask'))
    
    
    user = relationship('User', foreign_keys=[UserName], back_populates='exception_Table')
    component = relationship('ComponentTable', foreign_keys=[Component], back_populates='exceptions')
    mask_index = relationship('MapCreationTable', foreign_keys=[MapCreation_Index], back_populates='map_creation')

    __table_args__ = (
        PrimaryKeyConstraint('UserName','Timestamp','Run', 'Name_ID', 'Component', 'Component_index'),
    )

class MapCreationTable(Base):
    __tablename__ = 'mapCreationTable'
    # ID = Column(String, primary_key = True, default = lambda: uuid.uuid4().hex) 
    Mask = Column(String, primary_key = True)
    Name_Input = Column(String)

    map_creation = relationship('ExceptionTable', back_populates='mask_index', cascade='all', single_parent=True)


class ClueTable(Base):
    __tablename__ = 'clueTable'
    component_desc = Column(String, primary_key=True)
    token = Column(String)

class UserRole(Base):
    __tablename__ = 'rolesTable'
    RoleName = Column(String, primary_key=True)

    def __repr__(self):
        return f"<UserRole(name='{self.RoleName}')>"

class User(Base):
    __tablename__ = 'usersTable'
    id = Column(Integer, primary_key=True)
    FullName = Column(String)
    UserName = Column(String, unique=True)
    Email = Column(String, unique=True)
    Password = Column(String(60))
    Role = Column(String, ForeignKey('rolesTable.RoleName'))
    # Status = Column(String)

    role = relationship("UserRole")
    exception_Table = relationship('ExceptionTable', back_populates='user', cascade='all', single_parent=True)


    def __repr__(self):
        return f"<User(username='{self.UserName}', role_id={self.Role})>"

# Base.metadata.create_all(engine)