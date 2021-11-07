from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from userauth.models import UserInfo


class UserDetail(DetailView):
    model = UserInfo
    queryset = UserInfo.objects.select_related('user').all()
    slug_url_kwarg = 'user.username'
    slug_field = 'user.username'

    # TODO добавить
    #   превью скиллов
    #   кнопку, чтобы перейти в полный список скиллов
    #   фото, друзей, ачивки
    #   update about
    # queryset = Book.objects.filter(title__icontains='war')[:5]   -- как ограничить кол-во показываемых скиллов https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Generic_views
    # https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/


class UserCreateView(CreateView):
    model = User
    success_url = reverse_lazy('main-page')
    form_class = UserCreationForm
