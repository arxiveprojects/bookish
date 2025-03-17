from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DeleteView, UpdateView, CreateView,DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.urls import reverse_lazy
from .models import Book, Message
from .forms import BookCreationForm, BookUpdateForm
from .ask_pdf import ask_pdf, process_file
from django.contrib.auth import get_user_model
import fitz, os
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
       return Book.publics.order_by('-posted_at').select_related('user').prefetch_related("users_like").prefetch_related("messages")

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects.select_related('user').prefetch_related('users_like').prefetch_related("messages")


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'books/book_form.html'
    form_class = BookCreationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        # Set the user before saving
        form.instance.user = self.request.user
        
        # Handle file upload
        pdf_file = form.cleaned_data['pdf']
        
        # Auto-generate title if not provided
        if not form.instance.title:
            filename = os.path.basename(pdf_file.name)
            form.instance.title = os.path.splitext(filename)[0].title()
        else:
            form.instance.title = form.instance.title.title()
        
        # Save the form to get the file path
        response = super().form_valid(form)
        
        # Now that the model is saved, we have access to the file path
        try:
            # Get page count
            with fitz.Document(filename=form.instance.pdf.path, filetype='pdf') as pdf_doc:
                form.instance.pages = pdf_doc.page_count
            
            # Process the file with the actual file path
            process_file(form.instance.pdf.path, form.instance.title)
            form.instance.save()  # Save again to update the page count
            
        except Exception as e:
            # Log the error
            # logger.error(f"Error processing PDF: {e}")
            # Delete the created object
            form.instance.delete()
            # Re-add the error to the form
            form.add_error('pdf', f"Could not process PDF file: {e}")
            return self.form_invalid(form)
            
        return response


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
        return Book.publics.filter(title__icontains=query)#.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')

      
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
        books = user.book.select_related('user').prefetch_related("users_like", "messages")
    else:
        user = get_object_or_404(User.objects.prefetch_related("followers").only("id", "username", "bio", "image"), pk=user_pk)
        books = user.book.filter(public = True).select_related('user').prefetch_related("users_like").prefetch_related("messages")
    is_following = request.user.following.filter(id=user.id).exists() if request.user.is_authenticated else False

    return render(request,"profile/profile.html",
                  {"profile_user":user,"books":books,   
                   "total_books": books.count(),
                   "total_followers": user.followers.count(),
                   "total_following": user.following.count(),
                   "is_following":is_following})


@login_required
def book_like(request,pk):
    book = Book.objects.get(pk=pk)
    users_like =  book.users_like
    if request.user in users_like.all():
        book.users_like.remove(request.user)
    else:
        book.users_like.add(request.user)    
    return render(request,"partial/like.html",{"book":book})


@login_required
def get_messages(request,pk):
    messages = Message.objects.filter(book_id=pk,user_id=request.user).order_by('-timestamp')[:10]
    return render(request,"partial/messages.html",{'messages':messages})


@login_required
@require_POST
def post_message(request,pk):
    if request.method == "POST":
        book = get_object_or_404(Book, id=pk)
        query = request.POST.get("query")

        response = ask_pdf(query,book.title)

        message = Message.objects.create(
            book=book, user=request.user, query=query, response=response
        )
        return render(request,"partial/message.html",{'message':message})


@login_required
def delete_message(request,pk):
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return HttpResponse("message Deleted")