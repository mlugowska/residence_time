from typing import Dict

from rest_framework import serializers

from molecules.models import Ligand, Protein, Complex


class LigandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ligand
        fields = '__all__'


class ProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = '__all__'


class ComplexSerializer(serializers.ModelSerializer):
    ligand_name = serializers.CharField(source='ligand.name', required=False)
    ligand_inchi = serializers.CharField(source='ligand.inchi', required=False)
    ligand_smiles = serializers.CharField(source='ligand.smiles', required=False)
    ligand_formula = serializers.CharField(source='ligand.formula', required=False)
    ligand_file = serializers.FileField(source='ligand.file', required=False)
    ligand_code = serializers.CharField(source='ligand.code', required=False)

    protein_name = serializers.CharField(source='protein.name', required=False)
    protein_organism = serializers.CharField(source='protein.organism', required=False)
    protein_file = serializers.FileField(source='protein.file', required=False)

    class Meta:
        model = Complex
        fields = ('ligand_name', 'ligand_inchi', 'ligand_smiles', 'ligand_formula', 'ligand_file', 'ligand_code',
                  'protein_name', 'protein_organism', 'protein_file', 'name', 'pdb_id', 'file',
                  'release_year', 'primary_reference', 'residence_time', 'residence_time_plus_minus', 'ki', 'kon',
                  'koff', 'ki_plus_minus', 'koff_plus_minus', 'kon_ten_to_power', 'pubmed_id',
                  'is_calculated_from_koff',)

    @staticmethod
    def _create_ligand(ligand_data: Dict):
        return Ligand.objects.create(**ligand_data)

    @staticmethod
    def _create_protein(protein_data: Dict):
        return Protein.objects.create(**protein_data)

    def create(self, validated_data: Dict):
        ligand = None
        protein = None
        if validated_data.get('ligand'):
            ligand_data = validated_data.pop('ligand')
            ligand = self._create_ligand(ligand_data)
        if validated_data.get('protein'):
            protein_data = validated_data.pop('protein')
            protein = self._create_protein(protein_data)

        return Complex.objects.create(ligand=ligand, protein=protein, **validated_data)
