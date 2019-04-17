from django.contrib.auth.models import User
from django.db import models

from utils.filename_parsers import upper_filename_before_dot


class Ligand(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    file = models.FileField(upload_to='ligands/', blank=True, null=True)
    inchi = models.CharField(max_length=250, blank=True, null=True)
    smiles = models.CharField(max_length=250, blank=True, null=True)
    formula = models.CharField(max_length=250, blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        super().delete(using=None, keep_parents=False)


class Protein(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    organism = models.CharField(max_length=250, blank=True, null=True)
    file = models.FileField(upload_to='proteins/', blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        super().delete(using=None, keep_parents=False)


class Complex(models.Model):
    protein = models.OneToOneField(Protein, related_name='complex', on_delete=models.CASCADE, null=True)
    ligand = models.OneToOneField(Ligand, related_name='complex', on_delete=models.CASCADE, null=True)
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

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        self.ligand.delete()
        self.protein.delete()
        super().delete(using=None, keep_parents=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.file:
            self.file.name = upper_filename_before_dot(self.file)
        if self.pdb_id:
            self.pdb_id = self.pdb_id.upper()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
