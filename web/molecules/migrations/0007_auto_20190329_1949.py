# Generated by Django 2.1.7 on 2019-03-29 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('molecules', '0006_auto_20190319_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ligand',
            name='pdb_id',
            field=models.CharField(default='', max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name='protein',
            name='pdb_id',
            field=models.CharField(default='', max_length=4, unique=True),
        ),
    ]