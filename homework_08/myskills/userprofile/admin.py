from django.contrib import admin
from .models import UserInfo, UserSkillProfile, Skill, Direction


class UserSkillProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = UserSkillProfile
    list_display = ('user', 'skill', 'get_directions', 'parent_skill', 'status', 'progress_percent')


admin.site.register(UserSkillProfile, UserSkillProfileAdmin)

admin.site.register(UserInfo)
admin.site.register(Skill)
admin.site.register(Direction)
