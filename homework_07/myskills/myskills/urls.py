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

import userprofile.views
from myskills.settings import DEBUG

urlpatterns = [
    path('', TemplateView.as_view(template_name='userprofile/index.html'), name='main_page'),
    path('about/', TemplateView.as_view(template_name='userprofile/index.html'), name='about'),
    path('admin/', admin.site.urls),
    # path('<username>/', userprofile.views.UserDetail.as_view(), name='user-detail'),

    path('skills/', userprofile.views.SkillList.as_view(), name='all-skills'),
    path('skills/create/', userprofile.views.SkillCreate.as_view(), name='skill-create'),
    url(r'^skills/(?P<slug>[\w.-]+)/details/$', userprofile.views.SkillDetail.as_view(), name='skill-detail'),
    url(r'^skills/(?P<slug>[\w.-]+)/update/$', userprofile.views.SkillUpdate.as_view(), name='skill-update'),

    path('<username>/skills/', userprofile.views.UserSkillList.as_view(), name='user-skills'),
    url(r'^(?P<username>[\w.-]+)/skills/(?P<slug>[\w.-]+)/details/$', userprofile.views.UserSkillDetail.as_view(),
        name='user-skill-detail'),

    # на будущее
    # path('<user>/<skill>/diary/', userprofile.views. .as_view()),  # список
    # path('<user>/<skill>/diary/create', userprofile.views. .as_view()),
    # path('<user>/<skill>/diary/<id>/update', userprofile.views. .as_view()), # апдейт отдельной записи

]

if DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
