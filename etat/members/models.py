from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from mptt.fields import TreeForeignKey
from django_countries import CountryField

from sorl.thumbnail import ImageField

class Member(models.Model):
    GENDER_CHOICES = (
        ('f', _('female')),
        ('m', _('male')),
    )

    scout_name = models.CharField(_('scout name'), max_length=100, blank=True)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)

    portrait = ImageField(_('portrait'), upload_to='members',
        null=True, blank=True)

    gender = models.CharField(_('gender'), max_length=2, choices=GENDER_CHOICES,
        default='m')
    birthday = models.DateField(_('birthday'), null=True, blank=True)

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

    @property
    def address(self):
        try:
            return self.addresses.get(main=True)
        except:
            return None

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
    department = TreeForeignKey('departments.Department')
    type = models.ForeignKey(RoleType)

    start = models.DateField(_('start'))
    end = models.DateField(_('end'), null=True, blank=True)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def clean(self):
        if self.start and self.end and self.start >= self.end:
            raise ValidationError(_('Start data has to be before end date!'))

    def __unicode__(self):
        return _('%(type)s at %(department)s') % {
            'type': self.type,
            'department': self.department
        }

    @property
    def active(self):
        return self.end is None or now().date() < self.end


class Address(models.Model):

    member = models.ForeignKey(Member, related_name='addresses')

    street = models.CharField(_('street'), max_length=100)
    postal_code = models.PositiveIntegerField(_('post code'))
    city = models.CharField(_('city'), max_length=100)
    country = CountryField(_('country'), default='CH')
    main = models.BooleanField(_('main address'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def save(self, *args, **kwargs):
        if self.main:
            my_id = getattr(self, 'id', None)
            self.member.addresses.exclude(pk=my_id).update(main=False)
        super(Address, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s, %s %s' % (self.street, self.postal_code, self.city)

class Reachability(models.Model):

    TYPE_CHOICES = (
        ('email',       _('Email')),
        ('phone',      _('Phone')),
        ('skype',       _('Skype')),
        ('facebook',    _('Facebook')),
        ('twitter',     _('Twitter')),
    )

    KIND_CHOICES = (
        ('private', _('Private')),
        ('work',    _('Work')),
        ('scout',   _('Scout')),
        ('other',   _('Other')),
    )

    member = models.ForeignKey(Member, related_name='reachabilities')

    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES)
    kind = models.CharField(_('kind'), max_length=20, choices=KIND_CHOICES,
        blank=True)

    value = models.CharField(_('value'), max_length=100)

    class Meta:
        verbose_name = _('Reachability')
        verbose_name_plural = _('Reachabilities')

    def __unicode__(self):
        return u'%s %s' % (self.type, self.value)

    icons = {
        'email': 'icon-envelope',
        'phone': 'icon-phone',
        'skype': 'icon-skype',
        'facebook': 'icon-facebook',
        'twitter': 'icon-twitter',
    }

    def icon_class(self):
        return self.icons.get(self.type, 'icon-envelope')


class EducationType(models.Model):
    title = models.CharField(_('title'), max_length=100)
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Education type')
        verbose_name_plural = _('Education types')
        ordering = ('order',)

    def __unicode__(self):
        return self.title


class Education(models.Model):
    member = models.ForeignKey(Member, related_name='educations')
    type = models.ForeignKey(EducationType)

    date = models.DateField(_('date'), null=True, blank=True)

    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Educations')
        unique_together = ('member', 'type')

    def __unicode__(self):
        return self.type.title
