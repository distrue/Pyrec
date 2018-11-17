from .interact import function_connect, State
import importlib


def run():
    state = State()
    from . import command_plugins
    #command_plugins = importlib.import_module('')
    while(True):  # console
        print('$ ', end = '')
        try:
            in_str = input()
            state = function_connect(state, in_str)
        except EOFError:
            break