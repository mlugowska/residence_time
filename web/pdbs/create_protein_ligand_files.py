import os
from subprocess import call

from django.conf import settings

from molecules.models import Complex

COMPLEX_DIR = 'complexes'
PATH = os.path.join(settings.MEDIA_ROOT, COMPLEX_DIR)


def split_ligand_ab_conf(ligand_lines, complex_, ligand_file_a, ligand_file_b):
    with open(ligand_file_a, 'w+') as f_a:
        for line in ligand_lines:
            if f'A{complex_.ligand.code}' in line:
                f_a.writelines(line)

    with open(ligand_file_b, 'w+') as f_b:
        for line in ligand_lines:
            if f'B{complex_.ligand.code}' in line:
                f_b.writelines(line)


def convert(ligand_pdb: str, output_filename: str):
    cmd = ['babel', '-ipdb', f'{ligand_pdb}', '-osdf', f'{output_filename}']
    call(cmd)


def create_ligand_file(file, complex_file, complex_):
    if not complex_.ligand.file:
        ligand_lines = [line for line in complex_file if complex_.ligand.code in line]
        ligand_filename = f'{os.path.splitext(file)[0]}_ligand'
        ab_conformations = ['6EYA', '5UGS', '5LNZ', '6DJ1', '2YKJ', '5J2X']

        if complex_.pdb_id in ab_conformations:
            ligand_file_a = os.path.join(settings.MEDIA_ROOT, 'ligands', f'{ligand_filename}_a.pdb')
            ligand_file_b = os.path.join(settings.MEDIA_ROOT, 'ligands', f'{ligand_filename}_b.pdb')

            split_ligand_ab_conf(ligand_lines, complex_, ligand_file_a, ligand_file_b)

            ligand_sdf_a = f'{os.path.join(settings.MEDIA_ROOT, "ligands", f"{ligand_filename}_a.sdf")}'
            ligand_sdf_b = f'{os.path.join(settings.MEDIA_ROOT, "ligands", f"{ligand_filename}_b.sdf")}'
            print(complex_.pdb_id)
            convert(ligand_pdb=ligand_file_a, output_filename=ligand_sdf_a)
            convert(ligand_pdb=ligand_file_b, output_filename=ligand_sdf_b)
            complex_.ligand.file = ligand_file_a
            complex_.ligand.save()
        else:
            ligand_pdb_file = os.path.join(settings.MEDIA_ROOT, 'ligands', f'{ligand_filename}.pdb')
            with open(ligand_pdb_file, 'w+') as ligand_pdb:
                ligand_pdb.writelines(ligand_lines)

            ligand_sdf_file = f'{os.path.join(settings.MEDIA_ROOT, "ligands", f"{ligand_filename}.sdf")}'
            print(complex_.pdb_id)

            convert(ligand_pdb=ligand_pdb_file, output_filename=ligand_sdf_file)

            complex_.ligand.file = ligand_sdf_file
            complex_.ligand.save()


def create_protein_file(file, complex_file, complex_):
    if not complex_.protein.file:
        protein_lines = [line for line in complex_file if line[0:4] == 'ATOM']
        protein_filename = os.path.join(settings.MEDIA_ROOT, 'proteins', f'{os.path.splitext(file)[0]}_protein.pdb')
        with open(protein_filename, 'w+') as protein_file:
            protein_file.writelines(protein_lines)

        complex_.protein.file = protein_filename
        complex_.protein.save()


def split_complex_file():
    os.chdir(PATH)
    files = os.listdir(PATH)

    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'ligands')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'ligands'))

    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'proteins')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'proteins'))

    for file in files:
        complex_ = Complex.objects.get(pdb_id=os.path.splitext(file)[0])
        with open(file, 'r') as complex_file:
            create_protein_file(file, complex_file, complex_)

        with open(file, 'r') as complex_file:
            create_ligand_file(file, complex_file, complex_)
