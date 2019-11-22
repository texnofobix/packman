import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from versatileimagefield.fields import PPOIField, VersatileImageField

from .managers import AccountManager


def headshot_upload_location(instance, filename):
    return 'avatars/{0}/{1}'.format(instance.id, filename)


class Account(AbstractBaseUser, PermissionsMixin):
    """
    An e-mail based user account, used to log into the website
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        if self.profile.full_name != '':
            return '{} ({})'.format(self.email, self.profile.full_name())
        else:
            return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Sends an email to this User """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Headshot(models.Model):
    image = VersatileImageField(upload_to=headshot_upload_location, ppoi_field='ppoi', width_field='width', height_field='height', )

    ppoi = PPOIField('Image PPOI')

    class Meta:
        verbose_name = _('Headshot')
        verbose_name_plural = _('Headshots')

    def __str__(self):
        return self.image


class Member(models.Model):
    """
    The member profile used to store additional information about the member
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Prefer not to say'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32)
    nickname = models.CharField(max_length=32, blank=True, null=True,
                                help_text=_('If there is another name you prefer go by, tell us what it is we will use '
                                            'that on the website.'))
    avatar = models.OneToOneField(Headshot, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    date_added = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _('All Members')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.full_name()

    def get_absolute_url(self):
        if hasattr(self, 'parent'):
            return reverse('parent_detail', args=[str(self.id)])
        elif hasattr(self, 'scout'):
            return reverse('scout_detail', args=[str(self.id)])
        else:
            return None

    def full_name(self):
        """ Return the member's first and last name, replacing first name with a nickname if one has been given """
        return "{} {}".format(self.short_name(), self.last_name)

    def short_name(self):
        """ Return the member's nickname, if given, or first name if nickname isn't specified """
        if self.nickname:
            return self.nickname
        else:
            return self.first_name

    def thumbnail(self):
        """ Reduce the size of the member's avatar to fit in the detail card """
        pass


class Scout(Member):
    """
    Cub scouts use this model to store profile details
    """
    STATUS_CHOICES = (
        ('W', 'Applied'),
        ('P', 'Approved'),
        ('D', 'Denied'),
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('G', 'Graduated'),
    )

    birthday = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='I')

    def age(self):
        """ Calculates the cub scout's age when a birthday is specified """
        if not self.birthday:
            return None
        today = timezone.now()
        return today.year - self.birthday.year - (
                (today.month, today.day) < (self.birthday.month, self.birthday.day))

    def get_parents(self):
        """ Return a list of all parents associated with this scout """
        return self.parents.all()

    def get_siblings(self):
        """ Return a list of other Scouts who share the same parent(s) """
        return Scout.objects.filter(~Q(id=self.id), Q(parents__in=self.parents.all())).distinct()


class Parent(Member):
    """
    Any adult member such as a parent, guardian, or other use this model
    """
    ROLE_CHOICES = (
        ('P', 'Parent/Guardian'),
        ('C', 'Contributor'),
    )
    children = models.ManyToManyField(Scout, related_name='parents', through='Relationship', blank=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='P')
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile', verbose_name='email')


    def email(self):
        return self.account.email

    def get_active_scouts(self):
        """ Return a list of all currently active scouts associated with this member. """
        return self.children.filter(status__exact='A')

    @property
    def is_active(self):
        """ If member has active scouts, then they should also be considered active in the pack. """
        if self.get_active_scouts():
            return True
        else:
            return False


class Relationship(models.Model):
    """ Track the relationship a member has with a scout """
    RELATIONSHIP_CHOICES = (
        ('M', 'Mom'),
        ('F', 'Dad'),
        ('GM', 'Grandmother'),
        ('GF', 'Grandfather'),
        ('A', 'Aunt'),
        ('U', 'Uncle'),
        ('G', 'Guardian'),
        ('FF', 'Friend of the Family'),
        ('O', 'Other/Undefined')
    )
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Scout, on_delete=models.CASCADE)
    relationship_to_child = models.CharField(max_length=2, choices=RELATIONSHIP_CHOICES, default='O')

    def __str__(self):
        return self.child.full_name()
