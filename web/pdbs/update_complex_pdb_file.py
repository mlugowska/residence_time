import os

from django.conf import settings

from molecules.models import Complex
from pdbs.download_complex_pdb_files import download_complex_file
from pdbs.parse_complexes_filenames import change_complex_filename

DIR = 'complexes'
PATH = os.path.join(settings.MEDIA_ROOT, DIR)


def remove_chains(complex_file, complex):
    with open(complex_file, "r") as f:
        lines = f.readlines()

    with open(complex_file, "w") as f:
        for line in lines:
            if line[0:4] not in ['ATOM', 'TER ', 'HETA', 'CONE']:
                f.write(line)
            if line[0:4] in ['ATOM', 'TER ']:
                if line[21:22] == 'A':
                    f.write(line)
            if line[17:20] in [complex.ligand.code, 'HOH']:
                if line[21:22] == 'A':
                    f.write(line)


def update_complex_file():
    download_complex_file()
    change_complex_filename()
    os.chdir(PATH)
    files = os.listdir(PATH)

    for file in files:
        pdb_id, dot, format = file.rpartition('.')
        instance = Complex.objects.get(pdb_id=pdb_id.upper())

        remove_chains(file, instance)

        if not instance.file:
            instance.file = os.path.join(settings.MEDIA_ROOT, DIR, file)
            instance.save()
