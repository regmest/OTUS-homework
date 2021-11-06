from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView


class UserCreateView(CreateView):
    model = User
    success_url = reverse_lazy('main-page')
    form_class = UserCreationForm
