from .views import SignupPageView,ProfileUpdateView,follow
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path


urlpatterns = [
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # path('login/', LoginView.as_view(), name='logout'),
    path('signup/',SignupPageView.as_view(),name='signup'),
    path('<int:pk>/edit/',ProfileUpdateView.as_view(),name='edit_profile'),
    path('<int:pk>/follow/',follow,name='follow'),
]

