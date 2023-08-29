from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DeleteView, UpdateView, CreateView,DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.urls import reverse_lazy
from .models import Book
from .forms import BookCreationForm, BookUpdateForm
from .ask_pdf import ask_pdf,create_vectorstore
from django.contrib.auth import get_user_model
import fitz

User = get_user_model()
    
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
    paginate_by = 3

    def get_queryset(self):
       return Book.publics.order_by('-posted_at').select_related('user').prefetch_related("users_like")


class BookDetailView(DetailView):
    model= Book
    template_name='books/book_detail.html'
    context_object_name= 'book'

    def get_queryset(self):
       return Book.objects.all().select_related('user')

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
            form.instance.pages = pages(pdf)
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
        return Book.publics.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')

      

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

def more_books(request):
    offset = int(request.GET.get("offset"))
    books = Book.publics.order_by('-posted_at').prefetch_related("users_like")[offset:offset+3]
    context = {'results': books, 'offset': offset+3}
    return render(request, 'partial/more_books.html', context)

def get_book_images(request,pk):
    offset = int(request.GET.get("offset","0"))
    book:Book = Book.objects.get(pk=pk)
    images = book.get_images(offset)
    context ={"images":images,"book":book,"offset":offset+4}
    return render(request, 'partial/more_images.html', context)

def profile(request,user_pk=None):
    if not user_pk:
        user = request.user
        books = user.book.all().select_related("users_like")
    else:
        user = get_object_or_404(User, pk=user_pk)
        books = user.book.filter(public = True).prefetch_related("users_like")
    return render(request,"profile/profile.html",{"profile_user":user,"books":books})


@login_required
def book_like(request,pk):
    book = Book.objects.get(pk=pk)  
    users_like =  book.users_like
    if request.user in users_like.all():
        book.users_like.remove(request.user)
    else:
        book.users_like.add(request.user)    
    return render(request,"partial/like.html",{"book":book})


