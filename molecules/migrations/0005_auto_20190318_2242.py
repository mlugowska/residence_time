# Generated by Django 2.1.7 on 2019-03-18 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('molecules', '0004_auto_20190318_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ligand',
            name='pdb_id',
            field=models.CharField(max_length=4, null=True, unique=True),
        ),
    ]
