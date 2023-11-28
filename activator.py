from enum import StrEnum
import os
import re


class BotState(StrEnum):
    ACTIVE = r"(.*)\.py$"
    INACTIVE = r"(.*)\.py_$"


class Directories(StrEnum):
    BOTS = "bots"


def get_bot_files():
    return os.listdir(Directories.BOTS)


def filter_on_regex(strings, pattern: re.Pattern):
    for string in strings:
        match = pattern.match(string)
        if match is not None:
            yield match.group(1)


def filter_active_bots():
    pattern = re.compile(BotState.ACTIVE)
    return filter_on_regex(get_bot_files(), pattern)


def filter_inactive_bots():
    pattern = re.compile(BotState.INACTIVE)
    return filter_on_regex(get_bot_files(), pattern)


def bot_is_active(name):
    return any(bot == name for bot in filter_active_bots())


def bot_is_inactive(name):
    return any(bot == name for bot in filter_inactive_bots())


def change_file_extension(file, new_ext):
    old_path = os.path.abspath(file)
    name, _ = os.path.splitext(old_path)
    new_path = os.path.join(os.path.dirname(old_path), f"{name}.{new_ext}")
    os.rename(old_path, new_path)


def activate_bot(name):
    if bot_is_active(name):
        raise ValueError(f"{name} is already active")

    if bot_is_inactive(name):
        active_name = f"{name}.py"
        inactive_name = f"{name}.py_"
        os.rename(inactive_name, active_name)

    raise ValueError(f"Bot with name: {name} does not exist")


def deactivate_bot(name):
    if bot_is_inactive(name):
        raise ValueError(f"{name} is already inactive")

    if bot_is_active(name):
        active_name = f"{name}.py"
        inactive_name = f"{name}.py_"
        os.rename(active_name, inactive_name)

    raise ValueError(f"Bot with name: {name} does not exist")


def activate_bots(bots):
    for bot in bots:
        activate_bot(bot)


def deactivate_bots(bots):
    for bot in bots:
        deactivate_bot(bot)


def activate_all_bots():
    activate_bots(filter_inactive_bots())


def deactivate_all_bots():
    deactivate_bots(filter_active_bots())
