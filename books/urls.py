from django.urls import path
from .views import *

urlpatterns = [
    path('',BookListView.as_view(),name='book_list'),
    path('more_books/',more_books,name='more_books'),
    path('books/<slug:genre_slug>',BookListView.as_view(),name='books_by_genre'),
    path('books/<uuid:pk>/',BookDetailView.as_view(),name='book_detail'),
    path('books/<uuid:pk>/ask_question/',ask_question,name='ask_question'),
    path('books/<uuid:pk>/delete/',BookDeleteView.as_view(),name='book_delete'),
    path('books/<uuid:pk>/update/',BookUpdateView.as_view(),name='book_edit'),
    path('books/<uuid:pk>/update_visibility/',update_visibility,name='book_visibility'),
    path('books/create/',BookCreateView.as_view(),name='add_book'),
    path('books/<uuid:pk>/save_book/',save_book,name='save_book'),
    path('books/<uuid:pk>/like/', book_like, name='like'),
    path('saved/',saved_book_list,name='saved_books'),
    path('profile/',profile,name= 'profile'),
    path('profile/<int:user_pk>/',profile,name= 'profile'),
    path('search/',SearchResultsListView.as_view(),name='book_search'),
]
