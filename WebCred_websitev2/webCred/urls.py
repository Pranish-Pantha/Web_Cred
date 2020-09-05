from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='webCred-home'),
    path('jobListings', views.jobListings, name='webCred-jobListings'),
    path('articles', views.articles, name='webCred-Articles')
]
