import traceback
from copy import deepcopy
from venv import logger

from django.core.exceptions import ValidationError
from django.db.transaction import TransactionManagementError
from django.utils.encoding import force_text
from import_export import resources, widgets
from import_export.fields import Field
from import_export.results import RowResult

from molecules.models import Complex, Ligand, Protein


class ComplexResource(resources.ModelResource):
    ligand_name = Field(attribute='name', column_name='Ligand Name', widget=widgets.ForeignKeyWidget(Ligand, 'name'))
    ligand_inchi = Field(attribute='inchi', column_name='Ligand Inchi',
                         widget=widgets.ForeignKeyWidget(Ligand, 'inchi'))
    ligand_smiles = Field(attribute='smiles', column_name='Ligand SMILES',
                          widget=widgets.ForeignKeyWidget(Ligand, 'smiles'))
    ligand_formula = Field(attribute='formula', column_name='Ligand Formula',
                           widget=widgets.ForeignKeyWidget(Ligand, 'formula'))
    ligand_code = Field(attribute='code', column_name='Ligand Code',
                        widget=widgets.ForeignKeyWidget(Ligand, 'code'))

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
        fields = ('ligand_name', 'ligand_inchi', 'ligand_smiles', 'ligand_formula', 'ligand_code', 'protein_name',
                  'protein_organism', 'name', 'pdb_id', 'release_year', 'primary_reference', 'residence_time',
                  'residence_time_plus_minus', 'ki', 'kon', 'koff', 'ki_plus_minus', 'koff_plus_minus',
                  'kon_ten_to_power')
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
        elif field.column_name == 'Ligand Code' in data:
            ligand.code = data.get('Ligand Code')
            data.pop('Ligand Code')
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

    def import_row(self, row, instance_loader, using_transactions=True, dry_run=False, **kwargs):
        """
        Imports data from ``tablib.Dataset``. Refer to :doc:`import_workflow`
        for a more complete description of the whole import process.

        :param row: A ``dict`` of the row to import

        :param instance_loader: The instance loader to be used to load the row

        :param using_transactions: If ``using_transactions`` is set, a transaction
            is being used to wrap the import

        :param dry_run: If ``dry_run`` is set, or error occurs, transaction
            will be rolled back.
        """
        row_result = self.get_row_result_class()()
        try:
            self.before_import_row(row, **kwargs)
            instance, new = self.get_or_init_instance(instance_loader, row)
            self.after_import_instance(instance, new, **kwargs)
            if new:
                row_result.import_type = RowResult.IMPORT_TYPE_NEW
            else:
                row_result.import_type = RowResult.IMPORT_TYPE_UPDATE
            row_result.new_record = new
            original = deepcopy(instance)
            import_validation_errors = {}
            try:
                self.import_obj(instance, row, dry_run)
            except ValidationError as e:
                # Validation errors from import_obj() are passed on to
                # validate_instance(), where they can be combined with model
                # instance validation errors if necessary
                import_validation_errors = e.update_error_dict(import_validation_errors)
            if self.skip_row(instance, original):
                row_result.import_type = RowResult.IMPORT_TYPE_SKIP
            else:
                self.validate_instance(instance, import_validation_errors)
                self.save_instance(instance, using_transactions, dry_run)
                self.save_m2m(instance, row, using_transactions, dry_run)
                # Add object info to RowResult for LogEntry
                row_result.object_id = instance.pk
                row_result.object_repr = force_text(instance)

            self.after_import_row(row, row_result, **kwargs)

        except ValidationError as e:
            row_result.import_type = RowResult.IMPORT_TYPE_INVALID
            row_result.validation_error = e
        except Exception as e:
            row_result.import_type = RowResult.IMPORT_TYPE_ERROR
            # There is no point logging a transaction error for each row
            # when only the original error is likely to be relevant
            if not isinstance(e, TransactionManagementError):
                logger.debug(e, exc_info=e)
            tb_info = traceback.format_exc()
            row_result.errors.append(self.get_error_result_class()(e, tb_info, row))
        return row_result

    def dehydrate_ligand_name(self, complex):
        return complex.ligand.name

    def dehydrate_ligand_inchi(self, complex):
        return complex.ligand.inchi

    def dehydrate_ligand_smiles(self, complex):
        return complex.ligand.smiles

    def dehydrate_ligand_formula(self, complex):
        return complex.ligand.formula

    def dehydrate_ligand_code(self, complex):
        return complex.ligand.code

    def dehydrate_protein_name(self, complex):
        return complex.protein.name

    def dehydrate_protein_organism(self, complex):
        return complex.protein.organism
