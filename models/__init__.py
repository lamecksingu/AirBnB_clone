# models/__init__.py
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User

classes = {
        "BaseModel": BaseModel,
        "User": User
        }
storage = FileStorage()
storage.reload()

print("Type of Storage before setting:", type(storage))
print("Storage before setting:", storage)

# Pass storage instance to User class
User.set_storage(storage)

print("Type of storage after setting:", type(User.get_storage()))
print("Storage after setting:", User.get_storage())
