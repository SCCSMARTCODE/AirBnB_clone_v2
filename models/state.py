#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete-orphan")

    @property
    def cities(self):
        from models import storage

        city_inst = [inst for inst in storage.all().values()
                if isinstance(inst, City)]
        result = [cities for cities in city_inst if cities.state_id == self.id]
        return result
