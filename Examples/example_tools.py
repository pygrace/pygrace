import os

slash = os.path.sep
PYGRACE_PATH = slash.join(os.path.abspath(__file__).split(slash)[:-3])

def output_name(path, extension='agr'):
    filename = os.path.abspath(path)
    try:
        base, oldExtension = filename.rsplit('.', 1)
    except ValueError:
        base = filename
    return '.'.join((base, extension))
