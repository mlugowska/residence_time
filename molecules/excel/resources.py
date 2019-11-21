from import_export import resources, widgets
from import_export.fields import Field

from molecules.models import Complex, Ligand, Protein


class ComplexResource(resources.ModelResource):
    ligand_name = Field(attribute='name', column_name='Ligand Name', widget=widgets.ForeignKeyWidget(Ligand, 'name'))
    ligand_inchi = Field(attribute='inchi', column_name='Ligand Inchi',
                         widget=widgets.ForeignKeyWidget(Ligand, 'inchi'))
    ligand_smiles = Field(attribute='smiles', column_name='Ligand SMILES',
                          widget=widgets.ForeignKeyWidget(Ligand, 'smiles'))
    ligand_formula = Field(attribute='formula', column_name='Ligand Formula',
                           widget=widgets.ForeignKeyWidget(Ligand, 'formula'))

    protein_name = Field(attribute='name', column_name='Protein Name', widget=widgets.ForeignKeyWidget(Protein, 'name'))
    protein_organism = Field(attribute='organism', column_name='Protein Organism',
                             widget=widgets.ForeignKeyWidget(Protein, 'organism'))

    pdb_id = Field(column_name='PDB ID', attribute='pdb_id')
    residence_time = Field(column_name='Residence Time', attribute='residence_time')
    name = Field(column_name='Complex Name', attribute='name')
    release_year = Field(column_name='Release year', attribute='release_year')
    residence_time_plus_minus = Field(column_name='Residence Time Plus Minus', attribute='residence_time_plus_minus')
    ki = Field(column_name='Ki', attribute='ki')
    ki_plus_minus = Field(column_name='Ki Plus Minus', attribute='ki_plus_minus')
    kon = Field(column_name='Kon', attribute='kon')
    kon_plus_minus = Field(column_name='Kon Plus Minus', attribute='kon_plus_minus')
    kon_ten_to_power = Field(column_name='Kon 10^', attribute='kon_ten_to_power')
    koff = Field(column_name='Koff', attribute='koff')
    koff_plus_minus = Field(column_name='Koff Plus Minus', attribute='koff_plus_minus')
    primary_reference = Field(column_name='Reference', attribute='primary reference')

    class Meta:
        model = Complex
        fields = ('ligand_name', 'ligand_inchi', 'ligand_smiles', 'ligand_formula', 'protein_name', 'protein_organism',
                  'name', 'pdb_id', 'release_year', 'primary_reference', 'residence_time', 'residence_time_plus_minus',
                  'ki', 'kon', 'koff', 'ki_plus_minus', 'koff_plus_minus', 'kon_ten_to_power',)
        export_order = ('pdb_id', 'residence_time', 'residence_time_plus_minus',)
        import_id_fields = ('pdb_id',)
        import_id_field = 'pdb_id'
        skip_unchanged = True
        report_skipped = True

    def import_field(self, field, obj, data, is_m2m=False):
        ligand = Ligand.objects.get_or_create(complex=obj)[0]
        protein = Protein.objects.get_or_create(complex=obj)[0]

        if field.column_name == 'Ligand Name' in data:
            ligand.name = data.get('Ligand Name')
            data.pop('Ligand Name')
        elif field.column_name == 'Ligand Inchi' in data:
            ligand.inchi = data.get('Ligand Inchi')
            data.pop('Ligand Inchi')
        elif field.column_name == 'Ligand SMILES' in data:
            ligand.smiles = data.get('Ligand SMILES')
            data.pop('Ligand SMILES')
        elif field.column_name == 'Ligand Formula' in data:
            ligand.formula = data.get('Ligand Formula')
            data.pop('Ligand Formula')
        elif field.column_name == 'Protein Name' in data:
            protein.name = data.get('Protein Name')
            data.pop('Protein Name')
        elif field.column_name == 'Protein Organism' in data:
            protein.organism = data.get('Protein Organism')
            data.pop('Protein Organism')

        ligand.save()
        protein.save()

        obj.ligand = ligand
        obj.protein = protein
        obj.save()

        super().import_field(field, obj, data, is_m2m=False)

    def get_instance(self, instance_loader, row):
        row['PDB ID'] = row['PDB ID'].upper()
        return instance_loader.get_instance(row)

    def dehydrate_ligand_name(self, complex):
        return complex.ligand.name

    def dehydrate_ligand_inchi(self, complex):
        return complex.ligand.inchi

    def dehydrate_ligand_smiles(self, complex):
        return complex.ligand.smiles

    def dehydrate_ligand_formula(self, complex):
        return complex.ligand.formula

    def dehydrate_protein_name(self, complex):
        return complex.protein.name

    def dehydrate_protein_organism(self, complex):
        return complex.protein.organism
