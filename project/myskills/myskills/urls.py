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
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

import skillprofile.views
from myskills.settings import DEBUG
from userauth.views import UserCreateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='skillprofile/index.html'), name='main-page'),
    path('about/', TemplateView.as_view(template_name='skillprofile/index.html'), name='about'),

    path('admin/', admin.site.urls),

    # auth
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/registration/', UserCreateView.as_view(), name='user-registration'),

    # user about
    # path('<username>/details', userauth.views.UserDetail.as_view(), name='user-detail'),
    # path('<username>'/update/', userauth.views.

    # skills list & details
    path('skills/', skillprofile.views.SkillList.as_view(), name='all-skills'),
    path('skills/create/', skillprofile.views.SkillCreate.as_view(), name='skill-create'),
    url(r'^skills/(?P<slug>[\w.-]+)/details/$', skillprofile.views.SkillDetail.as_view(), name='skill-detail'),
    url(r'^skills/(?P<slug>[\w.-]+)/update/$', skillprofile.views.SkillUpdate.as_view(), name='skill-update'),

    # user skills list & details
    path('<username>/skills/', skillprofile.views.UserSkillList.as_view(), name='user-skills'),
    url(r'^(?P<username>[\w.-]+)/skills/(?P<slug>[\w.-]+)/details/$', skillprofile.views.UserSkillDetail.as_view(),
        name='user-skill-detail'),

]

if DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
