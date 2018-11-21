from .interact import function_connect, State
import importlib
import os
script_path = ''

def run(_script_path):
    state = State()
    global script_path
    script_path = os.path.dirname(_script_path)
    from . import command_plugins
    #command_plugins = importlib.import_module('')
    while(True):  # console
        print('$ ', end = '')
        try:
            in_str = input()
            state = function_connect(state, in_str)
        except SystemExit:
            break
