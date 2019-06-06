"""
This file sets up and configures the database using SQLAlchemy

SQLAlchemy
- There are 4 components to creating a database in SQLAlchemy
  1. Configuration - used to import all necessary modules
  2. Class - used to represent data in Python
  3. Table - represents specific table in the database
  4. Mapper - connects columns of the table to the class that represents it

Configuration
- Generally shouldn't change from project to project
- There are 2 parts
  - Beginning of File
    - imports all modules needed
    - creates instance of declarative base
  - End of File
    - creates (connects) the database and adds tables and columns

Class
- Representation of table as a Python class
- Extends the Base class
- Table and Mapper code nested inside

Table
- Representation of table inside the database
- Syntax:
    __tablename__ = 'some_table'

Mapper
- Maps python objects to columns in the database
- Syntax:
    column_name = Column(attributes, ...)
- Example attributes
  - String(250) - a string with max length 250 characters
  - Integer - for storing whole number values
  - relationship(Class) - tells SQLAlchemy the relationship between tables
  - nullable = False - 'False' indicates the column entry must have a value
  - primary_key = True - indicates a value we can use to uniquely identify each
        row of the database table
  - ForeignKey('some_table.id') - used to reference a row in a different table
        (provided a relationship exists between the two)
"""
# CONFIGURATION
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# this is used to create foreign key relationship
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# declarative_base() lets SQLAlchemy know our classes are special SQLAlchemy
# classes that correspond to tables in our database
Base = declarative_base()


# Create User able in order to implement local permission system
class User(Base):
    __tablename__ = 'user'

    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    id = Column(Integer, primary_key=True)


# CLASS
class Genre(Base):
    # TABLE
    __tablename__ = 'genre'
    # MAPPER
    # Name must be filled out to create a new Category row
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        '''
            Return object data in easily serializeable format
        '''
        return {
            'name': self.name,
            'id': self.id
        }


class Movie(Base):
    __tablename__ = 'movie'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    # Establish relationship between Item and Category
    # This line says to look inside 'category' table and retrieve the id number
    # whenever asking for category_id
    genre_id = Column(Integer, ForeignKey('genre.id'))
    # This line establishes the relationship
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        '''
            Return object data in easily serializeable format
        '''
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'genre': self.genre.name
        }


# KEEP this AT the END OF FILE
engine = create_engine('sqlite:///catalog.db')
# This goes into the database and adds the classes we've created as new tables
Base.metadata.create_all(engine)
