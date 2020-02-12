from django.db import models

from utils.filename_parsers import upper_filename_before_dot


class Ligand(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='ligands/', blank=True, null=True)
    inchi = models.CharField(max_length=1000, blank=True, null=True)
    smiles = models.CharField(max_length=1000, blank=True, null=True)
    formula = models.CharField(max_length=1000, blank=True, null=True)
    code = models.CharField(max_length=5, blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        super().delete(using=None, keep_parents=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.formula:
            SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
            self.formula = self.formula.translate(SUB)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Protein(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    organism = models.CharField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='proteins/', blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        super().delete(using=None, keep_parents=False)


class Complex(models.Model):
    protein = models.OneToOneField(Protein, related_name='complex', on_delete=models.CASCADE, null=True)
    ligand = models.OneToOneField(Ligand, related_name='complex', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    pdb_id = models.CharField(max_length=4, unique=True)
    file = models.FileField(upload_to='complexes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    release_year = models.IntegerField(blank=True, null=True)
    primary_reference = models.CharField(max_length=1000, blank=True, null=True)

    residence_time = models.FloatField(default=0)
    residence_time_plus_minus = models.FloatField(null=True, blank=True)

    ki = models.FloatField(default=0)
    kon = models.FloatField(default=0)
    koff = models.FloatField(default=0)
    ki_plus_minus = models.FloatField(default=0)
    koff_plus_minus = models.FloatField(default=0)
    kon_plus_minus = models.FloatField(default=0)
    kon_ten_to_power = models.FloatField(default=0)

    def delete(self, using=None, keep_parents=False):
        if self.file:
            self.file.delete()
        if self.ligand:
            self.ligand.delete()
        if self.protein:
            self.protein.delete()
        super().delete(using=None, keep_parents=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.file:
            self.file.name = upper_filename_before_dot(self.file)
        if self.pdb_id:
            self.pdb_id = self.pdb_id.upper()
        super(Complex, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
