from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from molecules.models import Protein, Complex, Ligand


class ComplexAdmin(ImportExportActionModelAdmin):
    pass


admin.site.register(Protein)
admin.site.register(Ligand)
admin.site.register(Complex, ComplexAdmin)
