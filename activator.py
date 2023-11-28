from enum import StrEnum
import os
import pathlib


class FileExt(StrEnum):
    ACTIVE = ".py"
    INACTIVE = ".py_"


class BotFile:
    def __init__(self, path: pathlib.Path):
        self.path = path
        name, ext = os.path.splitext(os.path.basename(path))
        self.name = name
        if ext not in FileExt:
            raise ValueError(f"{path} doesn't have a valid file extension")

    def activate(self):
        if self.is_active():
            raise ValueError(f"{self.name} is already active")

        new_path = self.path.with_suffix(FileExt.ACTIVE)
        self.path.rename(new_path)
        self.path = new_path

    def deactivate(self):
        if not self.is_active():
            raise ValueError(f"{self.name} is already inactive")

        new_path = self.path.with_suffix(FileExt.INACTIVE)
        self.path.rename(new_path)
        self.path = new_path

    def is_active(self):
        _, ext = os.path.splitext(self.path)
        return ext == FileExt.ACTIVE


class BotsDir:
    def __init__(self, dir_name):
        dir_path = pathlib.Path(dir_name)
        self.bot_files: dict[str, BotFile] = {}
        python_files = []
        for ext in FileExt:
            for python_file in dir_path.glob(f"*{ext}"):
                python_files.append(python_file)

        for python_file in python_files:
            bot_file = BotFile(python_file)
            self.bot_files[bot_file.name] = bot_file

    def activate_bot(self, bot_name):
        self.bot_files[bot_name].activate()

    def deactivate_bot(self, bot_name):
        self.bot_files[bot_name].deactivate()

    def get_active_bots(self):
        active_bots = []
        for name, bot_file in self.bot_files.items():
            if bot_file.is_active():
                active_bots.append(name)

        return active_bots

    def get_inactive_bots(self):
        inactive_bots = []
        for name, bot_file in self.bot_files.items():
            if not bot_file.is_active():
                inactive_bots.append(name)

        return inactive_bots

    def activate_bots(self, bots):
        for bot in bots:
            self.activate_bot(bot)

    def deactivate_bots(self, bots):
        for bot in bots:
            self.deactivate_bot(bot)

    def activate_all_bots(self):
        self.activate_bots(self.get_inactive_bots())

    def deactivate_all_bots(self):
        self.deactivate_bots(self.get_active_bots())
