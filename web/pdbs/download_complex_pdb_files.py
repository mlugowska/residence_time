import os
import sys
import urllib

from django.conf import settings

from molecules.models import Complex

complexes = Complex.objects.all()


def download(pdbcode, datadir, downloadurl="https://files.rcsb.org/download/"):
    """
    Downloads a PDB file from the Internet and saves it in a data directory.
    :param pdbcode: The standard PDB ID e.g. '3ICB' or '3icb'
    :param datadir: The directory where the downloaded file will be saved
    :param downloadurl: The base PDB download URL, cf.
        `https://www.rcsb.org/pages/download/http#structures` for details
    :return: the full path to the downloaded PDB file or None if something went wrong
    """
    pdbfn = pdbcode + ".pdb"
    url = downloadurl + pdbfn
    outfnm = os.path.join(datadir, pdbfn)
    try:
        urllib.request.urlretrieve(url, outfnm)
        return outfnm
    except Exception as err:
        print(str(err), file=sys.stderr)
        return None


def download_complex_file():
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'complexes')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'complexes'))

    for complex_ in complexes:
        print(complex_.pdb_id)
        if not complex_.file:
            download(pdbcode=complex_.pdb_id, datadir=os.path.join(settings.MEDIA_ROOT, 'complexes'))
