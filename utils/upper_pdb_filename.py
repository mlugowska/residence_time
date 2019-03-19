def upper_filename_before_dot(file):
    name, dot, format = file.name.rpartition('.')
    return f'{name.upper()}{dot}{format}'
