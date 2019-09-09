from django.urls import path
from upload import views

urlpatterns = [
        path('', views.home, name='home'), 
        path('load/status_table', views.load_status_table, name='load_status_table'),
]