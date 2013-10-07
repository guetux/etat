
from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe

from mptt.fields import TreeNodeChoiceField

from etat.departments.models import Department
from etat.utils.widgets import ImageWidget

from .models import Member, Address, Role


class MemberForm(forms.ModelForm):
    portrait = forms.ImageField(widget=ImageWidget, required=False)

    class Meta:
        model = Member
        exclude = ('departments',)


class RoleInlineForm(forms.ModelForm):
    department = TreeNodeChoiceField(queryset=Department.objects.all(),
        level_indicator=mark_safe(u'&nbsp;&nbsp;'))

    class Meta:
        model = Role
        widgets = {
            'start': forms.DateInput(attrs={'class': 'input-sm datepicker'}),
            'end': forms.DateInput(attrs={'class': 'input-sm datepicker'}),
        }


AddressFormSet = inlineformset_factory(
    Member,
    Address,
    extra=1,
)

RoleFormSet = inlineformset_factory(
    Member,
    Role,
    extra=1,
    form=RoleInlineForm,
)