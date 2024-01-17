#!/usr/bin/python3
""" serialization and deserialization of instances to & from json"""
import json
import os
import shlex


class FileStorage():
    """ class FileStorage"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            dictionary = self.__objects
            for key in dictionary:
                partition = key.replace('.', ' ')
                partition = shlex.split(partition)
                if (partition[0] == cls.__name__):
                    dic[key] = self.__objects[key]
            return (dic)
        else:
            return self.__objects

    def new(self, obj):
        """ assigns objects """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """ save objects to json file """
        dic = {}
        for key, obj in self.__objects.items():
            dic[key] = obj.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(dic, file)

    def reload(self):
        """ loads objects from existing file.jason """
        # This import is uses here to prevent circular import
        from models.base_model import BaseModel
        from models.user import User
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.state import State
        from models.review import Review

        # a class mapping dictionary to get the class

        cls_dic = {'BaseModel': BaseModel, 'User': User,
                   'Amenity': Amenity, 'City': City,
                   'Place': Place, 'State': State,
                   'Review': Review}

        j_file = os.path.exists(self.__file_path)
        if j_file:
            with open(self.__file_path, 'r') as file:
                new = json.load(file)
                for key, obj_dict in new.items():
                    get_class = obj_dict.get('__class__')
                    # get_class = get_class.strip()
                    # obj_class = cls_dic[get_class]
                    # obj = obj_class(**obj_dict)
                    # self.new(obj)
                    if get_class:
                        get_class = get_class.strip()
                        obj_class = cls_dic.get(get_class)
                        if obj_class:
                            obj = obj_class(**obj_dict)
                            self.new(obj)
                        else:
                            print("Class not found in cls_dic for key: {}"
                                  .format(get_class))
                    else:
                        print("'__class__' key not found in obj_dict")

    def delete(self, obj=None):
        """ delete an existing element
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]
