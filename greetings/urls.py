from django.urls import path
from . import views

urlpatterns = [
    path('', views.greet_contact_general, name='home'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('api/track-diya/', views.track_diya_light, name='track_diya_light'),
    path('<str:unique_id>/', views.greet_contact, name='greet_contact'),
    path('<str:unique_id>/interactive/', views.interactive_page, name='interactive_page'),
]
