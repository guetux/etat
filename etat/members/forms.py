
from django import forms

from .models import Member

from etat.utils.widgets import ImageWidget

class MemberForm(forms.ModelForm):
    portrait = forms.ImageField(widget=ImageWidget, required=False)

    class Meta:
        model = Member
        exclude = ('departments',)