import os

from django.conf import settings

from molecules.models import Complex
from pdbs.download_complex_pdb_files import download_complex_file
from pdbs.parse_complexes_filenames import change_complex_filename

DIR = 'complexes'
PATH = os.path.join(settings.MEDIA_ROOT, DIR)


def update_complex_file():
    download_complex_file()
    change_complex_filename()
    files = os.listdir(PATH)

    for file in files:
        pdb_id, dot, format = file.rpartition('.')
        instance = Complex.objects.get(pdb_id=pdb_id.upper())

        if not instance.file:
            instance.file = os.path.join(settings.MEDIA_ROOT, DIR, file)
            instance.save()
