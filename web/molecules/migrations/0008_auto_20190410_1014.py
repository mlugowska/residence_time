# Generated by Django 2.1.7 on 2019-04-10 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('molecules', '0007_auto_20190329_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ligand',
            name='pdb_id',
        ),
        migrations.RemoveField(
            model_name='protein',
            name='pdb_id',
        ),
    ]
