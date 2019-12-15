import pybel
import os

LIGANDS_DIR = 'ligands'
PATH = os.path.join(os.getcwd(), 'media', LIGANDS_DIR)
os.chdir(PATH)
files = [f for f in os.listdir(PATH) if f.endswith('.pdb')]


def convert_pdb_to_sdf(file):
    mol = pybel.readfile('pdb', os.path.join(PATH, file)).next()
    pybelmol = pybel.Molecule(mol)
    pybelmol.write('sdf', os.path.join(PATH, '%s.sdf' % (os.path.splitext(file)[0])))

    os.remove(file)


for file in files:
    convert_pdb_to_sdf(file)
