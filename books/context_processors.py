from .models import Saved

def saved_books(request):
    if request.user.is_authenticated:
        return {'saved_books': Saved.objects.get_or_create(user=request.user)[0].saved_book.all()}
    else: return {'saved_books':[]}