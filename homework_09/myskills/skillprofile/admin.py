from django.contrib import admin
from .models import Skill, SkillTag


class SkillAdmin(admin.ModelAdmin):
    class Meta:
        model = Skill
    list_display = ('created_at', 'author_user', 'name', 'status', 'description', 'tags', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Skill, SkillAdmin)


class SkillTagAdmin(admin.ModelAdmin):
    class Meta:
        model = SkillTag
    list_display = ('created_at', 'author_user', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(SkillTag, SkillTagAdmin)
