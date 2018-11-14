from .interact import function_connect, State
import importlib
from . import command_plugins

def run():
    #command_plugins = importlib.import_module('')
    state = State()
    while(True):  # console
        print('$ ', end = '')
        try:
            in_str = input()
            state = function_connect(state, in_str)
        except EOFError:
            break