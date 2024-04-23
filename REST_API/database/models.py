from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    additional_info = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="contacts")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    refresh_token = Column(String(255), nullable=True)

    contacts = relationship("Contact", back_populates="owner")
