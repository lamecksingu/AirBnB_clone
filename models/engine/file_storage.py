# models/engine/file_storage.py
import json
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        if obj.__class__.__name__ == 'BaseModel':
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        with open(self.__file_path, "w") as file:
            obj_dict = {}
            for key, obj in FileStorage.__objects.items():
                # only include instances of basemodel
                if isinstance(obj, BaseModel):
                    obj_dict[key] = obj.to_dict()
            json.dump(obj_dict, file, default=lambda o: o.__dict__, indent=4)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, "r") as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    class_name, obj_id = key.split(".")

                    # dynamically import the appropriate class
                    # based on class_name
                    cls = globals().get(class_name, None)
                    if cls and (
                            issubclass(cls, BaseModel
                                or
                                cls.__name__ == "User")):
                        # obj = eval(class_name)(**value)
                        obj = cls(**value)
                        self.__objects[key] = obj

        except FileNotFoundError:
            self.__objects = {}
            pass
        except json.JSONDecodeError:
            self.__objects = {}
            pass
