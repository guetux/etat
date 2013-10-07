
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

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


class RequireRoleFormset(BaseInlineFormSet):
    def clean(self):
        super(RequireRoleFormset, self).clean()
        if self.is_valid():
            self.saved_forms = []
            initial = self.initial_form_count()
            new = len(self.save_new_objects(commit=False))
            deleted = len(self.deleted_forms)
            if initial + new - deleted == 0:
                raise ValidationError(_('Member must have at least one Role!'))


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
    formset=RequireRoleFormset
)