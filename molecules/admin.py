from django.contrib import admin

from molecules.models import Protein, Complex, Ligand

admin.site.register(Protein)
admin.site.register(Ligand)
admin.site.register(Complex)
