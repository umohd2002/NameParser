# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 03:07:38 2024

@author: skhan2
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import bcrypt

Base = declarative_base()
engine = create_engine('sqlite:///KnowledgeBase_Test.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

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
    Status = Column(String)

    role = relationship("UserRole")
    exceptionTable = relationship('exceptionTable', back_populates='UserName', cascade='all', single_parent=True)


    def __repr__(self):
        return f"<User(username='{self.UserName}', role_id={self.Role})>"


# Base.metadata.create_all(engine)

# Assuming your existing code is here

# Create instances
# new_roles = [
#     UserRole(RoleName='Admin'),
#     UserRole(RoleName='Committee Member'),
#     UserRole(RoleName='General User')
# ]

# admin_role = session.query(UserRole).filter_by(RoleName='Admin').one_or_none()
# committee_role = session.query(UserRole).filter_by(RoleName='Committee Member').one_or_none()
# general_user_role = session.query(UserRole).filter_by(RoleName='General User').one_or_none()

# # Check if roles exist and then create User instances
# if admin_role and committee_role and general_user_role:
    # new_users = [
    #     User(FullName='Admin', UserName='admin', Email='admin@gmail.com', Password='123', Status='Active', Role=admin_role.RoleName),
    #     User(FullName='Committee Member 1', UserName='committee1', Email='committee1@gmail.com', Password='123', Status='Inactive', Role=committee_role.RoleName),
    #     User(FullName='Committee Member 2', UserName='committee2', Email='committee2@gmail.com', Password='123', Status='Inactive', Role=committee_role.RoleName),
    #     User(FullName='General', UserName='general', Email='general@gmail.com', Password='123', Status='Inactive', Role=general_user_role.RoleName)
    # ]
# new_user = User(FullName='Admin', UserName='admin', Email='admin@gmail.com', Password='123', Status='Active', Role=admin_role.RoleName)

#     session.add_all(new_users)
#     session.commit()
# else:
#     print("One or more roles not found in database.")
# Add instances to the session
# session.add(new_user)
# # session.add_all(new_roles)
# session.commit()
# session.add_all(new_users)
# session.commit()
# Commit the session

# def hash_password(password):
#     """ Hash a password using bcrypt """
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(password.encode(), salt)

# def update_passwords():
#     try:
#         # Fetch all users
#         users = session.query(User).all()
#         for user in users:
#             # Hash each user's password
#             hashed_password = hash_password(user.Password)
#             user.Password = hashed_password
#             session.add(user)

#         # Commit changes
#         session.commit()
#         print("Passwords updated successfully.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         session.rollback()

# # # Call the function to update passwords
# update_passwords()

# # # Close the session
# session.close()