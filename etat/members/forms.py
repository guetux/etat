
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from mptt.fields import TreeNodeChoiceField

from etat.departments.models import Department
from etat.utils.widgets import ImageWidget

from .models import Member, Address, Role


class MemberForm(forms.ModelForm):
    portrait = forms.ImageField(widget=ImageWidget, required=False)

    class Meta:
        model = Member
        exclude = ('departments',)
        widgets = {
            'gender': forms.RadioSelect(
                attrs={'class':'btn-group'}
            ),
        }


class RoleInlineForm(forms.ModelForm):
    department = TreeNodeChoiceField(queryset=Department.objects.all(),
        level_indicator=mark_safe(u'&nbsp;&nbsp;'))

    class Meta:
        model = Role
        widgets = {
            'start': forms.DateInput(attrs={'class': 'date'}),
            'end': forms.DateInput(attrs={'class': 'date'}),
        }

class OneRequiredFormset(BaseInlineFormSet):
    def clean(self):
        super(OneRequiredFormset, self).clean()
        if self.is_valid():
            self.saved_forms = []
            initial = self.initial_form_count()
            new = len(self.save_new_objects(commit=False))
            deleted = len(self.deleted_forms)
            if initial + new - deleted == 0:
                msg = _(u'%(parent)s must have at least one %(child)s!') % {
                    'parent': self.instance._meta.verbose_name,
                    'child': self.model._meta.verbose_name
                }
                raise ValidationError(msg)


AddressFormSet = inlineformset_factory(
    Member,
    Address,
    extra=1,
    formset=OneRequiredFormset
)

RoleFormSet = inlineformset_factory(
    Member,
    Role,
    extra=1,
    form=RoleInlineForm,
    formset=OneRequiredFormset
)