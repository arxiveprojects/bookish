from typing import Any, Dict
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DeleteView, UpdateView, CreateView,DetailView
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from .models import Book, Genre, Saved, SavedBook
from .forms import BookCreationForm, BookUpdateForm
from .ask_pdf import ask_pdf,create_vectorstore
from django.contrib.auth import get_user_model
import fitz

User = get_user_model()

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
    

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        genre_slug = self.kwargs.get("genre_slug")
        if genre_slug:
            return Book.publics.filter(genre__slug=genre_slug).order_by('-posted_at').select_related('user')
        return Book.publics.order_by('-posted_at').select_related('user')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        genre_slug = self.kwargs.get("genre_slug")
        if genre_slug:
            context["genre"] = get_object_or_404(Genre, slug=genre_slug)
        context['genres'] = Genre.objects.all()

        return context
class BookDetailView(DetailView):
    model= Book
    template_name='books/book_detail.html'
    context_object_name= 'book'


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'books/book_form.html'
    form_class= BookCreationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        BOOK = form.instance.pdf
        pdf=BOOK.read()

        if form.instance.title == '' or form.instance.title is None:
            name = form.instance.pdf.name
            form.instance.title = str(name).replace('book/pdfs/','').replace('.pdf','')
        form.instance.title = str(form.instance.title).title()
        
        try:
            vectorstore = create_vectorstore(BOOK)
            form.instance.summary = ask_pdf("summarize each chapter of the book. if you don't know then write None. Summary:",vectorstore)["answer"]
            form.instance.author = ask_pdf("what is the author name of this document? if you don't know the name then just write None. Name:",vectorstore)["answer"]
            form.instance.pages = pages(pdf)
            form.instance.cover.save(f'{form.instance.title}.png',ContentFile(cover(pdf)))
        except Exception as e:
            return super().form_invalid(form)
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    template_name = "books/book_form.html"
    form_class= BookUpdateForm
    success_url = reverse_lazy('profile')

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.user:
            return True
        return False


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('profile')
    template_name = 'books/delete_book.html'

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.user:
            return True
        return False


class SearchResultsListView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        query = query.strip()
        return Book.publics.filter(title__icontains=query).order_by('-posted_at').select_related('user')
      

def ask_question(request,pk):
    question = request.POST.get('question')
    book = Book.objects.get(id=pk)
    vectorstore = create_vectorstore(book.pdf.path)
    answer =ask_pdf(question,vectorstore)["answer"]
    return render(request,"partial/answer.html",{"answer":answer})
 
def update_visibility(request,pk):
    book = Book.objects.get(id=pk)
    book.public = not book.public
    book.save()
    visibility = "Private" if book.public else "Public"
    return render(request,'partial/visibility.html',{"visibility":visibility})


def profile(request,user_pk=None):
    if not user_pk:
        user = request.user
        books = user.book.all()
    else:
        user = get_object_or_404(User, pk=user_pk)
        books = user.book.filter(public = True)
    return render(request,"profile/profile.html",{"user":user,"books":books})

@login_required
def saved_book_list(request):
    saved_books = Saved.objects.get(user=request.user)
    books = [ saved_book.book for saved_book in saved_books.saved_book.all()]
    return render(request, 'books/saved.html', {'books': books})

@login_required
def save_book(request, pk):
    saved = Saved.objects.get(user=request.user)
    try:
        fav_book = SavedBook.objects.get(saved=saved, book_id=pk)
        fav_book.delete()
    except SavedBook.DoesNotExist:
        SavedBook.objects.create(saved=saved, book_id=pk)
    return redirect("saved_books")

