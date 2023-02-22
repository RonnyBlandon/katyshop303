from django import views
from django.urls import path
from . import views

app_name = "home_app"

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('points-rules/', views.PointsRulesView.as_view(), name='points_rules'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
]