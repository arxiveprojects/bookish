from django.urls import path
from .views import *

urlpatterns = [
    path('',BookListView.as_view(),name='book_list'),
    path('<uuid:pk>/',BookDetailView.as_view(),name='book_detail'),
    path('<uuid:pk>/ask_question/',ask_question,name='ask_question'),
    path('<uuid:pk>/delete/',BookDeleteView.as_view(),name='book_delete'),
    path('<uuid:pk>/update/',BookUpdateView.as_view(),name='book_edit'),
    path('<uuid:pk>/update_visibility/',update_visibility,name='book_visibility'),
    path('create/',BookCreateView.as_view(),name='add_book'),
    path('<uuid:pk>/save_book/',save_book,name='save_book'),
    path('saved/',saved_book_list,name='saved_books'),
    path('profile/',MyProfileListView.as_view(),name= 'my_profile'),
    path('search/',SearchResultsListView.as_view(),name='book_search'),
    path('<str:username>/',ProfileListView.as_view(),name='user_profile'),
]
