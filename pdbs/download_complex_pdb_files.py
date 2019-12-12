from Bio.PDB import PDBList

from molecules.models import Complex

pdb_list = PDBList()
complexes = Complex.objects.all()


def download_complex_file():
    for complex_ in complexes:
        if not complex_.file:
            pdb_list.retrieve_pdb_file(complex_.pdb_id, pdir='media/complexes', file_format='pdb')
