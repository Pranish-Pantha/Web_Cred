from django.urls import path
from .views import HomeView, JobListingView, ArticlesView
app_name = 'webCred'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('jobListings', JobListingView.as_view(), name='job-listings'),
    path('articles', ArticlesView.as_view(), name='articles')
]
