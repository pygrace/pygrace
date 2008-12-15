import os

def output_name(path, extension='out.agr'):
    filename = os.path.abspath(path)
    try:
        base, oldExtension = filename.rsplit('.', 1)
    except ValueError:
        base = filename
    return '.'.join((base, extension))
