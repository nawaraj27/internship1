from django.contrib import admin
from django.urls import path, include
from expenses.views import api_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('expenses.urls')), 
    path('', api_home, name='home'),         
]
