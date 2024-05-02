from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView

from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class MyProfileView(ListView):
    template_name = 'myprofile_view.html'
    model = CustomUser
