#!/usr/bin/env python3
"""Console Module"""
from models.engine.file_storage import FileStorage
import cmd
import models
from shlex import split


# Create an instance of FileStorage
storage = FileStorage()
# Load data from JSON file into memory
storage.reload()


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = '(hbnb) '

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
        if not arg:
            print("** class name missing **")
            return
        args = split(arg)
        try:
            new_instance = models.classes[args[0]]()
            new_instance.save()
            print(new_instance.id)
        except KeyError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
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
            print(models.storage.all()[key])
        except KeyError:
            print("** no instance found **")

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
