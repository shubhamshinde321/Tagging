from django.urls import path
from . import views

urlpatterns = [
        path('', views.process, name='process'),
        path('load_button/', views.load_button, name='load_button'),
        path('load_button/exact/', views.load_exact, name="load_exact"),
        path('load_button/variance/', views.load_variance, name="load_variance"),
        path('load_button/industry/', views.load_industry, name="load_industry"),
        path('load/autocomplete', views.load_autocomplete, name='load_autocomplete'),
        path('load/variance_code', views.load_variance_code, name='load_variance_code'),
        path('load/page', views.load_page, name='load_page'),
        path('load/exact_page', views.load_exact_page, name='load_exact_page'),
        path('load/industry_page', views.load_industry_page, name='load_industry_page'),
]