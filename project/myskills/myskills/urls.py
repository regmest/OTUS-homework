"""myskills URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

import skillprofile.views
import userauth.views
from myskills.settings import DEBUG
from userauth.views import UserCreateView


# TODO
#   на странице пользователя возможность заполнить about
#   на странице пользователя карточки с скиллами по статусам


urlpatterns = [
    # main
    path('', TemplateView.as_view(template_name='skillprofile/index.html'), name='main-page'),
    path('about/', TemplateView.as_view(template_name='skillprofile/index.html'), name='about'),
    path('admin/', admin.site.urls),

    # auth
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path('accounts/registration/', UserCreateView.as_view(), name='user-registration'),
    path('accounts/password-change/', PasswordChangeView.as_view(
        template_name='registration/custom_password_change_form.html',
        success_url=reverse_lazy("password-change-done"),
    ), name="password-change"),
    path('accounts/password-change/done', PasswordChangeDoneView.as_view(
        template_name='registration/custom_password_change_done.html'), name="password-change-done"),

    # user about
    url(r'^accounts/(?P<username>[\w.-]+)/$', userauth.views.UserDetail.as_view(), name='user-detail'),
    url(r'^accounts/(?P<username>[\w.-]+)/update/$', userauth.views.UserUpdate.as_view(), name='user-update'),

    # skills
    path('skills/', skillprofile.views.SkillList.as_view(), name='all-skills'),
    path('skills/create/', skillprofile.views.SkillCreate.as_view(), name='skill-create'),
    url(r'^skills/(?P<slug>[\w.-]+)/details/$', skillprofile.views.SkillDetail.as_view(), name='skill-detail'),

    # skill tags
    path('skills/tags/', skillprofile.views.SkillTagList.as_view(), name='all-skill-tags'),
    path('skills/tags/create/', skillprofile.views.SkillTagCreate.as_view(), name='skill-tag-create'),
    url(r'^skills/tags/(?P<slug>[\w.-]+)/update/$', skillprofile.views.SkillTagUpdate.as_view(), name='skill-tag-update'),

    # user skills
    path('<username>/skills/', skillprofile.views.UserSkillList.as_view(), name='all-user-skills'),
    url(r'^accounts/(?P<username>[\w.-]+)/skills/(?P<slug>[\w.-]+)/details/$', skillprofile.views.UserSkillDetail.as_view(),
        name='user-skill-detail'),
    url(r'^accounts/(?P<username>[\w.-]+)/skills/(?P<slug>[\w.-]+)/update/$', skillprofile.views.SkillUpdate.as_view(),
        name='user-skill-update'),
    url(r'^accounts/(?P<username>[\w.-]+)/skills/(?P<slug>[\w.-]+)/delete/$', skillprofile.views.SkillDelete.as_view(),
        name='user-skill-delete'),

]

if DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
