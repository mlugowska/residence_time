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
    ligand = LigandSerializer()
    protein = ProteinSerializer()

    class Meta:
        model = Complex
        fields = '__all__'

    def create(self, validated_data):
        ligand, created = Ligand.objects.get_or_create(**validated_data.pop('ligand'))
        protein, created = Protein.objects.get_or_create(**validated_data.pop('protein'))
        return Complex.objects.create(ligand=ligand, protein=protein, **validated_data)
