import os

from django.conf import settings

from molecules.models import Complex
import openbabel

COMPLEX_DIR = 'complexes'
PATH = os.path.join(settings.MEDIA_ROOT, COMPLEX_DIR)


def create_ligand_file(file, complex_file, complex):
    if not complex.ligand.file:
        ligand_lines = [line for line in complex_file if complex.ligand.code in line]
        ligand_filename = f'{os.path.splitext(file)[0]}_ligand'
        ligand_pdb_file = os.path.join(settings.MEDIA_ROOT, 'ligands', f'{ligand_filename}.pdb')
        with open(ligand_pdb_file, 'w+') as ligand_pdb:
            ligand_pdb.writelines(ligand_lines)

        obConversion = openbabel.OBConversion()
        obConversion.SetInAndOutFormats('pdb', 'sdf')

        mol = openbabel.OBMol()
        obConversion.ReadFile(mol, ligand_pdb_file)
        os.remove(os.path.join(settings.MEDIA_ROOT, 'ligands', f'{ligand_filename}.pdb'))
        ligand_sdf_file = f'{os.path.join(settings.MEDIA_ROOT, "ligands", f"{ligand_filename}.sdf")}'
        obConversion.WriteFile(mol, f'{ligand_sdf_file}')

        complex.ligand.file = ligand_sdf_file
        complex.ligand.save()


def create_protein_file(file, complex_file, complex):
    if not complex.protein.file:
        protein_lines = [line for line in complex_file if line[0:4] == 'ATOM']
        protein_filename = os.path.join(settings.MEDIA_ROOT, 'proteins', f'{os.path.splitext(file)[0]}_protein.pdb')
        with open(protein_filename, 'w+') as protein_file:
            protein_file.writelines(protein_lines)

        complex.protein.file = protein_filename
        complex.protein.save()


def split_complex_file():
    os.chdir(PATH)
    files = os.listdir(PATH)

    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'ligands')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'ligands'))

    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'proteins')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'proteins'))

    for file in files:
        complex = Complex.objects.get(pdb_id=os.path.splitext(file)[0])
        with open(file, 'r') as complex_file:
            create_protein_file(file, complex_file, complex)

        with open(file, 'r') as complex_file:
            create_ligand_file(file, complex_file, complex)
