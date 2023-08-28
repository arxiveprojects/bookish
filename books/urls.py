from django.urls import path
from .views import *

urlpatterns = [
    path('',BookListView.as_view(),name='book_list'),
    path('more_books/',more_books,name='more_books'),
    path('books/<uuid:pk>/',BookDetailView.as_view(),name='book_detail'),
    path('books/<uuid:pk>/ask_question/',ask_question,name='ask_question'),
    path('books/<uuid:pk>/delete/',BookDeleteView.as_view(),name='book_delete'),
    path('books/<uuid:pk>/update/',BookUpdateView.as_view(),name='book_edit'),
    path('books/<uuid:pk>/update_visibility/',update_visibility,name='book_visibility'),
    path('books/<uuid:pk>/images/',get_book_images,name='get_book_images'),
    path('books/create/',BookCreateView.as_view(),name='add_book'),
    path('books/<uuid:pk>/like/', book_like, name='like'),
    path('profile/',profile,name= 'profile'),
    path('profile/<int:user_pk>/',profile,name= 'profile'),
    path('search/',SearchResultsListView.as_view(),name='book_search'),
]
