from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DeleteView, UpdateView, CreateView,DetailView
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from .models import Book, Favorite, FavoriteBook
from .forms import BookCreationForm, BookUpdateForm
from .ask_pdf import ask_pdf
import fitz

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        return Book.objects.filter(is_visible=True).order_by('-posted_at').select_related('user')


class BookDetailView(DetailView):
    model= Book
    template_name='books/book_detail.html'
    context_object_name= 'book'


def cover(pdf):
    with fitz.Document(stream = pdf, filetype='pdf') as pdf:
        image = pdf.get_page_pixmap(0)
        stream = image.tobytes(output="png")
        return stream
    
def pages(pdf):
    try:
        with fitz.Document(stream = pdf, filetype='pdf') as pdf:
            return pdf.page_count
    except:
        return 1
    
   
def ask_question(request,pk):
    question = request.GET.get('q')
    book = Book.objects.get(id=pk)
    answer = ask_pdf(question,book.pdf.path)
    return render(request, 'books/book_detail.html', {"book": book, "answer":answer})

    


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'books/book_form.html'
    form_class= BookCreationForm
    success_url = reverse_lazy('my_profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        BOOK = form.instance.pdf
        if form.instance.title == '' or form.instance.title is None:
            name = form.instance.pdf.name
            form.instance.title = str(name).replace('book/pdfs/','').replace('.pdf','')
        form.instance.title = str(form.instance.title).title()
        form.instance.summary = ask_pdf("summarize each chapter of the book.",BOOK)
        form.instance.author = ask_pdf("get the author name from the book, write in less than 5 words.",BOOK)
        form.instance.genre = ask_pdf("get genre name from the book, write in less than 5 words.",BOOK)
        pdf=BOOK.read()
        try:
            form.instance.cover.save(f'{form.instance.title}.png',ContentFile(cover(pdf)))
            form.instance.pages = pages(pdf)
        except Exception as e:
            return super().form_invalid(form)
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    template_name = "books/book_form.html"
    form_class= BookUpdateForm
    success_url = reverse_lazy('my_profile')

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.user:
            return True
        return False


class BookVisibilityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    template_name = "books/book_form.html"
    fields = ['is_visible']
    success_url = reverse_lazy('my_profile')

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.user:
            return True
        return False


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('my_profile')
    template_name = 'books/delete_book.html'

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.user:
            return True
        return False


def get_favorite(request):
    user = request.user if request.user.is_authenticated else None
    if request.user.is_authenticated:
        try:
            fav = Favorite.objects.get(user=user)
        except:
            fav = None
    else:
        try:
            fav = Favorite.objects.get(
                id=request.session.get('fav_uuid', None))
        except:
            fav = None
    if not fav:
        fav = Favorite.objects.create(user=user)
        request.session['fav_uuid'] = str(fav.id)
    return fav


def get_fav_book_list(request):
    fav = get_favorite(request)
    fav_books = FavoriteBook.objects.filter(
        favorite=fav).only('book').select_related('book__user')
    books = []
    for fav_book in fav_books:
        books.append(fav_book.book)
    return render(request, 'books/fav.html', {'books': books})


def add_book_to_fav(request, pk):
    fav = get_favorite(request)

    try:
        fav_book = FavoriteBook.objects.get(favorite=fav, book_id=pk)
        fav_book.delete()
    except FavoriteBook.DoesNotExist:
        FavoriteBook.objects.create(favorite=fav, book_id=pk)
    return redirect('book_list')


class ProfileListView(ListView):
    model = Book
    template_name = 'profile/profile.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(
            get_user_model(), username=self.kwargs.get('username'))
        return context

    def get_queryset(self):
        user = get_object_or_404(
            get_user_model(), username=self.kwargs.get('username'))
        return Book.objects.filter(Q(user=user) & Q(is_visible=True)).order_by('-posted_at').select_related('user')


class MyProfileListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'profile/my_profile.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None
        return Book.objects.filter(user=user).order_by('-posted_at').select_related('user')


class SearchResultsListView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        query = query.strip()
        search_for = self.request.GET.get('f')
        user = self.request.GET.get('user')
        if search_for == 'book_list':
            return Book.objects.filter(Q(title__icontains=query) & Q(is_visible=True)).order_by('-posted_at').select_related('user')
        elif search_for == 'my_profile':
            return Book.objects.filter(Q(title__icontains=query) & Q(user__username=user)).order_by('-posted_at').select_related('user')
        elif search_for == 'profile':
            return Book.objects.filter(Q(title__icontains=query) & Q(is_visible=True) & Q(user__username=user)).order_by('-posted_at').select_related('user')
