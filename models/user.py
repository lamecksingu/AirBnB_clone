# models/user.py
from models.base_model import BaseModel


class User(BaseModel):
    """User class that inherits from BaseModel."""

    def __init__(self, *args, **kwargs):
        """Initialize User instance."""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')

    def __str__(self):
        """Return string representation of User instance."""
        return "[{}] ({}) {} {}".format(
                self.__class__.__name__,
                self.id,
                self.first_name,
                self.last_name
                )

    def to_dict(self):
        """Return a dictionary representation of User instance."""
        user_dict = super().to_dict()
        user_dict.update({
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name
        })
        return user_dict

    @classmethod
    def from_dict(cls, adict):
        """Create an instance from a dictionary representation."""
        # Remove attributes specific to User
        email = adict.pop('email', '')
        password = adict.pop('password', '')
        first_name = adict.pop('first_name', '')
        last_name = adict.pop('last_name', '')
        # Create a new instance of User using the modified dictionary
        return cls(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name, **adict)
