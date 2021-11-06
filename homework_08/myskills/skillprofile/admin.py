from django.contrib import admin
from .models import Skill, SkillTag


class SkillAdmin(admin.ModelAdmin):
    class Meta:
        model = Skill
    list_display = ('author_user', 'name', 'status', 'description', 'tags', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Skill, SkillAdmin)

admin.site.register(SkillTag)
