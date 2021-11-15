import string
import random

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from slugify import slugify as py_slugify
from django.utils.translation import gettext
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from skillprofile.models import Skill, SkillTag


def random_slug(length: int):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


class SkillTagList(ListView):
    model = SkillTag


class SkillTagCreate(LoginRequiredMixin, CreateView):
    model = SkillTag
    fields = ('name',)
    success_url = reverse_lazy('all-skill-tags')

    def form_valid(self, form):
        form.instance.author_user = self.request.user
        form.instance.slug = py_slugify(form.instance.name + random_slug(3))
        return super().form_valid(form)


class SkillTagUpdate(UserPassesTestMixin, UpdateView):
    model = SkillTag
    fields = ('name',)
    success_url = reverse_lazy('all-skill-tags')

    def form_valid(self, form):
        form.instance.author_user = self.request.user
        if not self.kwargs['slug']:
            form.instance.slug = py_slugify(form.instance.name + "-" + random_slug(3))
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.has_perm('skillprofile.change_skilltag')

# TODO skill tag delete


class SkillList(ListView):
    model = Skill
    queryset = Skill.objects.only('name', 'slug')#.distinct('name')

    # TODO добавить кнопку "хочу изучать" с добавлением скилла в UserSkill пересылающую на user-skill-create
    # TODO вывести теги в ряд
    # TODO на PG попробовать distinct


class SkillDetail(DetailView):
    """ General skill info """
    model = Skill

    def get_tags(self):
        self.tags = SkillTag.objects.filter(skill__slug=self.kwargs['slug']).only('name')
        return self.tags

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.get_tags()
        return context

    # TODO добавить кнопку "хочу изучать" рядом с не моими скиллами
    # TODO вывести теги в ряд
    # TODO напротив скиллов, которые юзер уже изучает тег "learning"


class SkillCreate(LoginRequiredMixin, CreateView):
    model = Skill
    fields = ('name', 'status', 'description', 'tag')

    def form_valid(self, form):
        form.instance.author_user = self.request.user
        form.instance.slug = py_slugify(form.instance.name + "-" + random_slug(3))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user-skill-detail', kwargs={'slug': self.object.slug, 'username': self.request.user.username})


class SkillUpdate(UserPassesTestMixin, UpdateView):
    model = Skill
    fields = ('name', 'status', 'description', 'tag')

    def get_success_url(self):
        return reverse('user-skill-detail', kwargs={'slug': self.object.slug, 'username': self.request.user})

    def form_valid(self, form):
        form.instance.author_user = self.request.user
        if not self.object.slug:
            form.instance.slug = py_slugify(form.instance.name + "-" + random_slug(3))
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.username == self.kwargs['username'] \
               or self.request.user.has_perm('skillprofile.change_skill')


class SkillDelete(UserPassesTestMixin, DeleteView):
    model = Skill

    def get_success_url(self):
        return reverse('all-user-skills', kwargs={'username': self.request.user})

    def test_func(self):
        return self.request.user.username == self.kwargs['username'] \
               or self.request.user.has_perm('skillprofile.delete_skill')


class UserSkillList(ListView):
    """ Skill info for a particular user """
    model = Skill
    template_name = 'skillprofile/userskill_list.html'

    def get_queryset(self):
        self.username = get_object_or_404(User, username=self.kwargs['username'])
        user_skills = Skill.objects.select_related('author_user').filter(author_user__username=self.username)
        return user_skills

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = str(self.username)
        return context


class UserSkillDetail(DetailView):
    """ Full skill info for a user """
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

    def get_tags(self):
        self.tags = SkillTag.objects.filter(skill__slug=self.kwargs['slug']).only('name')
        return self.tags

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = str(self.username)
        context['tags'] = self.get_tags()
        return context


