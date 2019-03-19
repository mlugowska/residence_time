from django.contrib.auth.models import User
from django.db import models

from utils.upper_pdb_filename import upper_filename_before_dot


class Ligand(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    file = models.FileField(upload_to='ligands/', blank=True, null=True)
    pdb_id = models.CharField(max_length=4, unique=True, null=True)
    inchi = models.CharField(max_length=250, blank=True, null=True)
    smiles = models.CharField(max_length=250, blank=True, null=True)
    formula = models.CharField(max_length=250, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pdb_id:
            self.pdb_id = self.pdb_id.upper()
        if self.file:
            self.file.name = upper_filename_before_dot(self.file)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Protein(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    organism = models.CharField(max_length=250, blank=True, null=True)
    file = models.FileField(upload_to='proteins/', blank=True, null=True)
    pdb_id = models.CharField(max_length=4, unique=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pdb_id:
            self.pdb_id = self.pdb_id.upper()
        if self.file:
            self.file.name = upper_filename_before_dot(self.file)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Complex(models.Model):
    protein = models.ForeignKey(Protein, related_name='complexes', on_delete=models.CASCADE, null=True)
    ligand = models.ForeignKey(Ligand, related_name='complexes', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    pdb_id = models.CharField(max_length=4, unique=True)
    file = models.FileField(upload_to='complexes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    release_year = models.CharField(max_length=4, blank=True, null=True)
    primary_reference = models.CharField(max_length=250, blank=True, null=True)

    residence_time = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    residence_time_plus_minus = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)

    ki = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    kon = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    koff = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    ki_plus_minus = models.DecimalField(max_digits=12, decimal_places=6, default=0.0)
    koff_plus_minus = models.DecimalField(max_digits=10, decimal_places=5, default=0.0)
    kon_ten_to_power = models.DecimalField(max_digits=2, decimal_places=0, default=0)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.file:
            self.file.name = upper_filename_before_dot(self.file)
        self.pdb_id = self.pdb_id.upper()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
