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
        if match:
            yield string


def filter_active_bots():
    pattern = re.compile(BotState.ACTIVE)
    return filter_on_regex(get_bot_files(), pattern)


def filter_inactive_bots():
    pattern = re.compile(BotState.ACTIVE)
    return filter_on_regex(get_bot_files(), pattern)


def bot_is_active(name):
    return any(bot == name for bot in filter_active_bots())


def bot_is_inactive(name):
    return any(bot == name for bot in filter_inactive_bots())


def activate_bot(name):
    if bot_is_active(name):
        raise ValueError(f"{name} is already active")

    if bot_is_inactive(name):
        active_name = f"{name}.py"
        inactive_name = f"{name}.py_"
        os.rename(inactive_name, active_name)

    raise ValueError(f"{name} does not exist")


def deactivate_bot(name):
    if bot_is_inactive(name):
        raise ValueError(f"{name} is already inactive")

    if bot_is_active(name):
        active_name = f"{name}.py"
        inactive_name = f"{name}.py_"
        os.rename(active_name, inactive_name)

    raise ValueError(f"{name} does not exist")
