from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from molecules.excel.resources import ComplexResource
from molecules.models import Protein, Complex, Ligand

admin.site.register(Protein)
admin.site.register(Ligand)
admin.site.register(Complex)


class ComplexAdmin(ImportExportModelAdmin):
    resource_class = ComplexResource
