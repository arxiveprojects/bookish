from .views import SignupPageView,ProfileUpdateView,follow
from django.urls import path

urlpatterns = [
    path('signup/',SignupPageView.as_view(),name='signup'),
    path('<int:pk>/edit/',ProfileUpdateView.as_view(),name='edit_profile'),
    path('<int:pk>/follow/',follow,name='follow'),
]

