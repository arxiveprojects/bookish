from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DeleteView, UpdateView, CreateView,DetailView
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from .models import Book, Saved, SavedBook
from .forms import BookCreationForm, BookUpdateForm
from .ask_pdf import ask_pdf,create_vectorstore
import fitz



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
    question = request.POST.get('question')
    book = Book.objects.get(id=pk)
    vectorstore = create_vectorstore(book.pdf.path)
    answer =ask_pdf(question,vectorstore)["answer"]
    return render(request,"partial/answer.html",{"answer":answer})
 
def update_visibility(request,pk):
    book = Book.objects.get(id=pk)
    book.is_visible = not book.is_visible
    book.save()
    print(f"visibility of {pk}:",book.is_visible)
    visibility = "Private" if book.is_visible else "Public"
    return render(request,'partial/visibility.html',{"visibility":visibility})




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
        pdf=BOOK.read()

        try:
            form.instance.cover.save(f'{form.instance.title}.png',ContentFile(cover(pdf)))
            form.instance.pages = pages(pdf)

            vectorstore = create_vectorstore(BOOK)
            form.instance.summary = ask_pdf("summarize each chapter of the book.",vectorstore)["answer"]
            form.instance.author = ask_pdf("get the author name from the book, write in less than 5 words.",vectorstore)["answer"]
            form.instance.genre = ask_pdf("get genre name from the book, write in less than 5 words.",vectorstore)["answer"]
            
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


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('my_profile')
    template_name = 'books/delete_book.html'

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.user:
            return True
        return False



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
        return Book.objects.filter(Q(title__icontains=query) & Q(is_visible=True)).order_by('-posted_at').select_related('user')
      