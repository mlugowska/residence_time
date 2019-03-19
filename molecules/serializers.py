from django import forms
from django.forms import ModelForm
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

    def update(self, instance, validated_data):
        if validated_data.get('ligand'):
            ligand_data = validated_data.pop('ligand')
            Ligand.objects.filter(pk=instance.ligand.pk).update(**ligand_data)

        if validated_data.get('protein'):
            protein_data = validated_data.pop('protein')
            Protein.objects.filter(pk=instance.protein.pk).update(**protein_data)
        return super().update(instance, validated_data)
