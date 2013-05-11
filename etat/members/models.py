from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries import CountryField


class Member(models.Model):
    GENDER_CHOICES = (
        ('f', _('female')),
        ('m', _('male')),
    )

    scout_name = models.CharField(_('scout name'), max_length=100, blank=True)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)

    portrait = models.ImageField(_('portrait'), upload_to='members',
        null=True, blank=True)

    gender = models.CharField(_('gender'), max_length=2, choices=GENDER_CHOICES)
    birthday = models.DateField(_('birthday'), null=True, blank=True)

    mobile = models.CharField(_('Mobile'), max_length=30, blank=True)
    phone = models.CharField(_('Phone'), max_length=30, blank=True)

    notes = models.TextField(_('notes'), blank=True)

    departments = models.ManyToManyField('departments.Department',
        through='Role', related_name='members')

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')

    def __unicode__(self):
        return self.fullname

    @property
    def fullname(self):
        return u'%s %s' % (self.first_name, self.last_name)


class RoleType(models.Model):

    name = models.CharField(_('name'), max_length=100)
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Role type')
        verbose_name_plural = _('Role types')
        ordering = ('order',)

    def __unicode__(self):
        return self.name


class Role(models.Model):
    member = models.ForeignKey(Member, related_name='roles')
    department = models.ForeignKey('departments.Department')
    type = models.ForeignKey(RoleType)

    start = models.DateField(_('start'))
    end = models.DateField(_('end'), null=True, blank=True)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def clean(self):
        if self.end and self.start >= self.end:
            raise ValidationError(_('Start data has to be before end date!'))

    def __unicode__(self):
        return _('%s at %s') % (self.type, self.department)


class Address(models.Model):

    member = models.ForeignKey(Member, related_name='addresses')

    street = models.CharField(_('street'), max_length=100)
    addition = models.CharField(_('addition'), max_length=100, blank=True)

    postal_code = models.PositiveIntegerField(_('Postal Code'))
    city = models.CharField(_('city'), max_length=100)

    country = CountryField(_('country'), default='CH')

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __unicode__(self):
        return u'%s' % self.member
