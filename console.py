#!/usr/bin/env python3
"""Console Module"""
from models.engine.file_storage import FileStorage
import cmd
import models
from models.base_model import BaseModel
from shlex import split
from models.user import User
from models import storage


User.set_storage(storage)

# Create an instance of FileStorage
storage = FileStorage()
# Load data from JSON file into memory
storage.reload()


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = '(hbnb) '
    classes = {
            "BaseModel": BaseModel,
            "User": User
            }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Called when an empty line + ENTER is entered"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id"""
        try:
            if not arg:
                raise SyntaxError()
            my_list = arg.split(" ")

            kwargs = {}
            for i in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                # obj = eval(my_list[0])(storage)
                obj = eval(my_list[0])(storage=storage)
            else:
                # obj = eval(my_list[0])(storage, **kwargs)
                obj = eval(my_list[0])(storage=storage, **kwargs)
                storage.new(obj)
            print(obj.id)
            # print(f"Object created: {obj}")  # debug print
            # print(f"Object ID: {obj.id}")  # debug print
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        try:
            if args[0] not in models.classes:
                print("** class doesn't exist **")
                return
            if len(args) < 2:
                print("** instance id missing **")
                return
            obj_id = args[1]
            class_name = args[0]
            key = "{}.{}".format(class_name, obj_id)
            all_instances = models.storage.all()
            for instance_key, instance in all_instances.items():
                if key == instance_key:
                    print(instance)
                    return
                print("** no instance found **")
        except Exception as e:
            print(e)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        args = split(arg)
        try:
            if args[0] not in models.classes:
                raise KeyError
            if len(args) < 2:
                print("** instance id missing **")
                return
            key = "{}.{}".format(args[0], args[1])
            del models.storage.all()[key]
            models.storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        if not arg:
            print([str(obj) for obj in models.storage.all().values()])
        else:
            args = split(arg)
            if args[0] not in models.classes:
                print("** class doesn't exist **")
                return
            print([str(obj) for key, obj in models.storage.all().items()
                   if key.split('.')[0] == args[0]])

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        args = split(arg)
        try:
            if args[0] not in models.classes:
                raise KeyError
            if len(args) < 2:
                print("** instance id missing **")
                return
            key = "{}.{}".format(args[0], args[1])
            if key not in models.storage.all():
                print("** no instance found **")
                return
            if len(args) < 3:
                print("** attribute name missing **")
                return
            if len(args) < 4:
                print("** value missing **")
                return
            obj = models.storage.all()[key]
            setattr(obj, args[2], args[3].strip('"'))
            obj.save()
        except KeyError:
            print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
