import os

from Bio.PDB import PDBList
from django.conf import settings

from molecules.models import Complex

pdb_list = PDBList()
complexes = Complex.objects.all()


def download_complex_file():
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'complexes')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'complexes'))

    for complex_ in complexes:
        if not complex_.file:
            pdb_list.retrieve_pdb_file(complex_.pdb_id, pdir=os.path.join(settings.MEDIA_ROOT, 'complexes'),
                                       file_format='pdb')
