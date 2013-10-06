
from django import forms
from django.forms.models import inlineformset_factory

from .models import Member, Address

from etat.utils.widgets import ImageWidget

class MemberForm(forms.ModelForm):
    portrait = forms.ImageField(widget=ImageWidget, required=False)

    class Meta:
        model = Member
        exclude = ('departments',)

AddressFormSet = inlineformset_factory(
    Member,
    Address,
    extra=1,
)