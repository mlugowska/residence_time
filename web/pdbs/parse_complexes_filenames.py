import os

from django.conf import settings

DIR = 'complexes'
PATH = os.path.join(settings.MEDIA_ROOT, DIR)


def change_complex_filename():
    files = os.listdir(PATH)

    for file in files:
        if not file.endswith('.pdb'):
            name, dot, format = file.rpartition('.')
            os.rename(os.path.join(PATH, file), os.path.join(PATH, f'{name[3:].upper()}{dot}{name[:3]}'))
