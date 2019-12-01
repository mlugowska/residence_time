import os

from django.conf import settings

from molecules.models import Complex

COMPLEX_DIR = 'complexes'
PATH = os.path.join(settings.MEDIA_ROOT, COMPLEX_DIR)


def create_ligand_file(file, complex_file, complex):
    if not complex.ligand.file:
        ligand_lines = [line for line in complex_file if line[0:6] == 'HETATM' and line[17:20] != 'HOH']
        ligand_filename = os.path.join(settings.MEDIA_ROOT, 'ligands', f'{os.path.splitext(file)[0]}_ligand.sdf')
        with open(ligand_filename, 'w') as ligand_file:
            ligand_file.writelines(ligand_lines)

        complex.ligand.file = ligand_filename
        complex.ligand.save()


def create_protein_file(file, complex_file, complex):
    if not complex.protein.file:
        protein_lines = [line for line in complex_file if line[0:6] == 'ATOM']
        protein_filename = os.path.join(settings.MEDIA_ROOT, 'proteins', f'{os.path.splitext(file)[0]}_protein.pdb')
        with open(protein_filename, 'w') as ligand_file:
            ligand_file.writelines(protein_lines)

        complex.protein.file = protein_filename
        complex.protein.save()


def split_complex_file():
    files = os.listdir(PATH)
    os.chdir(PATH)

    for file in files:
        complex = Complex.objects.get(pdb_id=os.path.splitext(file)[0])
        with open(file, 'r') as complex_file:
            create_ligand_file(file, complex_file, complex)
            create_protein_file(file, complex_file, complex)
