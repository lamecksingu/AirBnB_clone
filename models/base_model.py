# models/base_model.py
import uuid
from datetime import datetime


class BaseModel:
    def __init__(self, *args, **kwargs):
        """Initialize BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key,
                            datetime.strptime(
                                value,
                                '%Y-%m-%dT%H:%M:%S.%f'))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Return string representation of BaseModel instance."""
        return "[{}] ({}) {}".format(
                self.__class__.__name__,
                self.id,
                self.__dict__
                )

    def save(self):
        """Update the public instance attribute updated_at
        with the current datetime."""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Return a dictionary representation of BaseModel instance."""
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict

    @classmethod
    def from_dict(cls, adict):
        """Create an instance from a dictionary representation."""
        # Remove '__class__' from the dictionary if it exists
        class_name = adict.pop('__class__', None)
        # Convert 'created_at' and 'updated_at' from string to datetime objects
        cls = globals().get(class_name)
        if cls is None:
            raise ValueError(f"Class '{class_name}' not found")
        #Convert to date time object
        adict['created_at'] = datetime.strptime(
            adict['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
        adict['updated_at'] = datetime.strptime(
            adict['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
        # Create a new instance of the class using the modified dictionary
        return cls(**adict)
