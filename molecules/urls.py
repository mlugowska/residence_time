from django.urls import path, re_path
from molecules import views
from django.contrib.auth import views as auth_views
from django.contrib import admin


app_name = 'molecules'
urlpatterns = [
    path('', views.index, name='index'),
    path('database/', views.sources, name='sources'),
    path('signup/', views.signup, name='signup'),
    path('add_form/', views.add_to_db, name='add_form'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('login/', auth_views.LoginView.as_view(template_name='molecules/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/molecules/'), name='logout'),
    path('csv/', views.export_database_csv, name='export_database_csv'),
    path('admin/', admin.site.urls),
    re_path(r'^details/([a-zA-Z0-9]{4})/$', views.details, name='details'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
]