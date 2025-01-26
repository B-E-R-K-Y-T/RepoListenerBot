from typing import NamedTuple, Callable, Optional, List, Union

from telebot import State


class Ignore:
    pass


class Handler(NamedTuple):
    callback: Union[Callable, Ignore]
    commands: Optional[Union[List[str], Ignore]] = None
    pass_bot: Union[bool, Ignore] = False
    check_admin: Union[bool, Ignore] = True
    state: Optional[Union[State, Ignore]] = None
    check_login: Union[bool, Ignore] = True
