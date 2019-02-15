from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# class Ligand(models.Model):
#     name = models.CharField(max_length=20, blank=True, null=True)
#     ki = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
#     kon = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
#     koff = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
#     added_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


# class Protein(models.Model):
#     name = models.CharField(max_length=20, blank=True, null=True)
#     ec_number = models.CharField(max_length=20, blank=True, null=True)
#     resolution = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
from molecules.storage import OverwriteStorage



class Complex(models.Model):
    """
    pdbid - pdbid
    ctype - complex type
    pname - protein name
    lname - ligand name
    ecnum - EC number
    resol - resolution
    btime - binding time
    ryear - Release year
    forla - ligand formula
    mowei - molecular weight
    exmas - Exact Mass
    noato - No. of atoms
    nobon - No. of bonds
    psuae - Polar surface area
    smile - Canonical SMILES
    inchi - International Chemical Identifier
    files - PDB file
    """
    PROTLIG = 'Protein-ligand'
    MULTIPROT = 'Multiprotein'
    CTYPE = ((PROTLIG, 'Protein-ligand'),
             (MULTIPROT, 'Multiprotein'),)

    complex_type = models.CharField(max_length=22, choices=CTYPE, default=PROTLIG)
    protein_name = models.CharField(max_length=20, blank=True, null=True)
    ligand_name = models.CharField(max_length=20, blank=True, null=True)
    ec_number = models.CharField(max_length=20, blank=True, null=True)
    resolution = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    residence_time = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    residence_time_plus_minus = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    release_year = models.DecimalField(max_digits=4, decimal_places=0, default=1900)
    primary_reference = models.TextField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    added_by = models.ForeignKey(User, on_delete=None)

    ki_value = models.DecimalField(max_digits=12, decimal_places=4, default=0.0)
    ki_plus_minus = models.DecimalField(max_digits=12, decimal_places=6, default=0.0)
    kon_value = models.DecimalField(max_digits=9, decimal_places=2, default=0.0)
    kon_ten_to_power = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    koff_value = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    koff_plus_minus = models.DecimalField(max_digits=10, decimal_places=5, default=0.0)

    pdb_id = models.CharField(max_length=4, default='', unique=True)
    pdb_file = models.FileField(blank=True, null=True, unique=True, upload_to='./media/pdb/', storage=OverwriteStorage())


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
