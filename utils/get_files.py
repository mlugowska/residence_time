import os
import shutil

from django.conf import settings
from django.http import FileResponse
from utils.filename_parsers import parse_filename


def download_file(instance):
    file_handle = instance.file.open()
    response = FileResponse(file_handle, content_type='whatever')
    response['Content-Length'] = instance.file.size
    response['Content-Disposition'] = \
        f'attachment; filename={parse_filename(instance=instance)}'
    return response


def copy_files_to_current_dir(files):
    for file in files:
        shutil.copy(os.path.join(settings.MEDIA_ROOT, file.name), os.getcwd())


def create_dir_with_structure_files(queryset):
    os.mkdir(os.path.join(settings.MEDIA_ROOT, 'structures'))

    for name in queryset.values_list('pdb_id', flat=True):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, 'structures', name))
        os.chdir(os.path.join(settings.MEDIA_ROOT, 'structures', name))

        instance = queryset.get(pdb_id=name)

        files = [instance.file, instance.protein.file, instance.ligand.file]
        copy_files_to_current_dir(files)


