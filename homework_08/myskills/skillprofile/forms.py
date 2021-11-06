from django.forms import ModelForm
from skillprofile import models


class SkillCreateForm(ModelForm):
    class Meta:
        model = models.Skill
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
