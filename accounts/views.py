from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from accounts.models import Contact
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

User = get_user_model()

class SignupPageView(generic.CreateView):
    form_class= CustomUserCreationForm
    success_url= reverse_lazy('login')
    template_name= 'registration/signup.html'

class ProfileUpdateView(LoginRequiredMixin,UserPassesTestMixin, generic.UpdateView):
    model= User
    fields= ('email', 'username', 'image', 'bio',)
    success_url= reverse_lazy('profile')
    template_name= 'registration/edit_profile.html'


    def test_func(self):
        user= self.get_object()
        if self.request.user == user:
            return True
        return False
    
@login_required
@require_POST
def follow(request, pk):
    user = get_object_or_404(User,pk=pk)
    following = False
    try:
        contact = Contact.objects.get(user_to=user,user_from=request.user)
        contact.delete()
    except Contact.DoesNotExist:
        following = True
        Contact.objects.create(user_to=user,user_from=request.user)
    print("count",user.followers.all().count())
    return render(request,"partial/follow.html",{"following":following})