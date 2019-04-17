def upper_filename_before_dot(file):
    name, dot, format = file.name.rpartition('.')
    return f'{name.upper()}{dot}{format}'


def parse_filename(instance):
    dir, slash, name = instance.file.name.rpartition('/')
    name, dot, format = name.rpartition('.')
    return f'{name}{dot}{format}'
