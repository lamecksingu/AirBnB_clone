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
