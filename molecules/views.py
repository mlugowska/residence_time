import csv

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .filters import DatabaseFilter
from .forms import SearchForm, SignUpForm, AddToDbForm
from .models import Complex
from .token import account_activation_token


def index(request):
    return render(request, 'molecules/index.html')


def details(request, file_id):
    try:
        protein = Complex.objects.get(pdb_id=file_id)
    except Complex.DoesNotExist:
        raise Http404("There is no connected protein")
    return render(request, 'molecules/details.html', {'protein': protein})


def sources(request):
    proteins_list = Complex.objects.all()
    proteins_filter = DatabaseFilter(request.GET, queryset=proteins_list)
    return render(request, 'molecules/sources.html', {'filter': proteins_filter})


def download(request):
    return HttpResponse()


def get_pdbid(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            return render(request, 'molecules/details.html')
        else:
            form = SearchForm()

        return render(request, 'molecules/details.html', {'form': form})


def add_to_db(request):
    if request.method == 'POST':
        form = AddToDbForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "molecules/index.html")
    else:
        form = AddToDbForm()
    return render(request, 'molecules/add_form.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('molecules/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('/molecules/account_activation_sent')
    else:
        form = SignUpForm()

    return render(request, 'molecules/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'molecules/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/molecules/')
    return render(request, 'molecules/account_activation_invalid.html')


def export_database_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="database.csv"'

    writer = csv.writer(response)
    writer.writerow(['PDB ID, complex_type, protein name, ligand name, resolution, residence time, '
                     'residence time plus minus, '
                     'release year, ligand formula, molecular weight, exact mass, no of atoms, no of bonds, '
                     'polar surface area, smile, inchi, ki value, ki plus minus, kon value, kon 10 to power, '
                     'koff value, koff plus minus'])
    protligs = Complex.objects.all().values_list('pdb_id', 'complex_type', 'protein_name', 'ligand_name', 'resolution',
                                                 'residence_time', 'residence_time_plus_minus', 'release_year',
                                                 'ligand_formula', 'molecular_weight', 'exact_mass', 'no_of_atoms',
                                                 'no_of_bonds', 'polar_surface_area', 'smile', 'inchi', 'ki_value',
                                                 'ki_plus_minus', 'kon_value', 'kon_ten_to_power', 'koff_value',
                                                 'koff_plus_minus', )
    for protlig in protligs:
        writer.writerow(protlig)

    return response
