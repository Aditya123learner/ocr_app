from . import api
def get_module(modulename):
    print("Trying to load module:", modulename)  # Add this line
    return importlib.import_module(modulename)
