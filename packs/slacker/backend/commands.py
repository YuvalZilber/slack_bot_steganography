import functools
from typing import Callable, Any

from mypy_extensions import KwArg

from packs.slacker.backend.response import Response, make_response

_allowed_commands: dict[str, Callable[[KwArg(Any)], Response]] = {}


def allowed_commands():
    return _allowed_commands


# note to self:
# it was decorator vs inheritance

# *** inheritance advantages:
# 1. known return type (at type-checking time & IDE static analyze)
# 2. modularity for more complex commands without the need of creating a new class
# 3. can list with metaclass

# *big* disadvantage: need to import (most likely unused import) all subclasses in order to list them.
#                     if those are not defined by interpreter, they will execute code to list them

# *** decorator advantages:
# 1. dynamic parameter types (each function takes only what it needs), validated runtime though...
# 2. easier listing with (relatively) easy to read code
# 3. showing off my control over another aspect of python


def bot_command(cmd: Callable[[KwArg(Any)], Response] | str):
    def _bot_command(name: str):
        def add_command(f: Callable[[KwArg(Any)], Response]):
            @functools.wraps(f)
            def wrapper(**kwargs):
                # noinspection PyUnresolvedReferences
                arg_names = f.__code__.co_varnames
                args = {key: value for key, value in kwargs.items() if key in arg_names}
                return f(**args)

            _allowed_commands[name] = wrapper
            return wrapper

        return add_command

    normal_decorator = _bot_command(cmd.__name__) if callable(cmd) else _bot_command
    return normal_decorator(cmd)


@bot_command("help")
def help_menu() -> Response:
    """Show this menu. Format: '\\help'"""
    result = [""]
    for cmd_name, cmd in allowed_commands().items():
        result.append(f"\\{cmd_name} - {cmd.__doc__ or 'empty __doc__'}")
    return make_response(text="\n".join(result))
