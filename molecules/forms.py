from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from molecules.models import Complex


class SearchForm(forms.Form):
    pdb_id = forms.CharField(widget=forms.Textarea(), label='PDB ID', max_length=4, help_text="PDB ID")


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required first name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required last name')
    email = forms.EmailField(max_length=254, required=True, help_text='Required email address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class AddToDbForm(forms.ModelForm):
    class Meta:
        model = Complex
        fields = ('pdb_file', 'pdb_id', 'complex_type', 'protein_name', 'ligand_name',
                  'residence_time', 'residence_time_plus_minus', 'release_year', 'primary_reference', 'added_by',
                  'ki_value', 'ki_plus_minus', 'kon_value', 'kon_ten_to_power', 'koff_value',
                  'koff_plus_minus',)
