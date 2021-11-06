import string
import random

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from slugify import slugify as py_slugify
from django.utils.translation import gettext
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from skillprofile.models import Skill


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))


class SkillList(ListView):
    model = Skill
    queryset = Skill.objects.only('name', 'slug')#.distinct('name')

    # TODO добавить кнопку "хочу изучать" с добавлением скилла в UserSkill пересылающую на user-skill-create
    # TODO вывести теги в ряд
    # TODO на PG попробовать distinct


class SkillDetail(DetailView):
    """ General skill info """
    model = Skill
    # TODO добавить кнопку "хочу изучать" рядом с не моими скиллами
    # TODO вывести теги в ряд
    # TODO напротив скиллов, которые юзер уже изучает тег "learning"


class SkillCreate(CreateView):
    model = Skill
    success_url = reverse_lazy('all-skills')  # TODO возвращать туда, откуда create вызывался (all-skills/user-skills)
    fields = ('name', 'status', 'description', 'tag')

    def form_valid(self, form):
        form.instance.author_user = self.request.user
        form.instance.slug = py_slugify(form.instance.name + "-" + rand_slug())
        return super().form_valid(form)


class SkillUpdate(UpdateView):
    model = Skill
    fields = ('name', 'status', 'description', 'tag')

    def get_success_url(self):
        return reverse('user-skill-detail', kwargs={'slug': self.kwargs['slug'], 'username': self.request.user})

    def form_valid(self, form):
        form.instance.author_user = self.request.user
        if not self.kwargs['slug']:
            form.instance.slug = py_slugify(form.instance.name + "-" + rand_slug())
        return super().form_valid(form)


class UserSkillList(ListView):
    """ Skill info for particular user """
    model = Skill
    template_name = 'skillprofile/userskill_list.html'
    # TODO добавить кнопку Edit

    def get_queryset(self):
        # показываем скиллы определенного в урле юзера
        # https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/
        self.username = get_object_or_404(User, username=self.kwargs['username'])
        user_skills = Skill.objects.select_related('author_user').filter(author_user__username=self.username)
        # TODO проверить на наличие лишних запросов, оптимизировать
        return user_skills

    def get_context_data(self, **kwargs):
        # https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/
        context = super().get_context_data(**kwargs)
        context['username'] = self.username
        return context


class UserSkillDetail(DetailView):
    """ Full skill info for user """
    # TODO diary
    model = Skill
    template_name = 'skillprofile/userskill_detail.html'

    def get_queryset(self):
        self.username = get_object_or_404(User, username=self.kwargs['username'])
        return Skill.objects.filter(author_user__username=self.username)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        if slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(gettext("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.username
        return context


