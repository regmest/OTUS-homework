from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.template.defaultfilters import slugify

from skillprofile import models


class SkillCreateForm(ModelForm):
    class Meta:
        model = models.Skill
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
