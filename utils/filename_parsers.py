def upper_filename_before_dot(file):
    name, dot, format = file.name.rpartition('.')
    if len(name) > 4:
        return f'{name[:-5]}/{name[-4:].upper()}{dot}{format}'
    return f'{name.upper()}{dot}{format}'


def parse_filename(instance):
    dir, slash, name = instance.file.name.rpartition('/')
    name, dot, format = name.rpartition('.')
    return f'{name}{dot}{format}'
