from django.shortcuts import render

from userprofile.models import UserSkillProfile


def index_view(request):
    user_skills_profiles = UserSkillProfile.objects.all()
    return render(request,
                  'userprofile/index.html',
                  {'user_skills_profiles': user_skills_profiles})