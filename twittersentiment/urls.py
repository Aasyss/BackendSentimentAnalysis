from django.contrib import admin
from django.urls import path

from twittersentiment import views

urlpatterns = [
    path('textanalyzer/', views.textanalyzer),
    path('gettweets/', views.gettweets)
]
