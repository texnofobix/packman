import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases

from .managers import MemberManager


def get_headshot_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/headshots/user_slug/<filename>
    return f'headshots/{slugify(instance.get_full_name())}/{filename}'


def two_years_ago():
    """
    Calculate the year two years before the current year.
    Used by the Scout model to provide a sane default for when they start school.
    """
    return timezone.now().year - 2


class Member(models.Model):
    """
    An abstract base class implementing the details we would want to capture for any person on the site.
    Used by the later models, Adult and Scout, to populate common fields used in those models.
    """

    # Define static options for gender
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (OTHER, _('Prefer not to say'))
    )

    # Personal information
    first_name = models.CharField(_('First Name'), max_length=30)
    middle_name = models.CharField(_('Middle Name'), max_length=32, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=150)
    suffix = models.CharField(_('Suffix'), max_length=8, blank=True, null=True)
    nickname = models.CharField(_('Nickname'), max_length=32, blank=True, null=True, help_text=_(
        "If there is another name you prefer to be called, tell us what it is we will use that on the website."))
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES, default=None, blank=False, null=True)
    photo = ThumbnailerImageField(_('Headshot Photo'), upload_to=get_headshot_path, blank=True, null=True, help_text=_(
        "We use member photos on the website to help match names with faces."))

    # Administrative
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True, null=True)
    date_added = models.DateTimeField(_('Date Joined'), default=timezone.now, blank=True)
    last_updated = models.DateTimeField(_('Last Updated'), auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['first_name', 'middle_name', 'nickname', 'last_name', 'gender'])]
        ordering = ['last_name', 'nickname', 'first_name']

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        # if not self.family:
        #     self.family = Family.objects.create()
        if not self.slug:
            # TODO: Make this more robust. We have three passes to get a unique slug before giving up.
            if not Member.objects.filter(slug__exact=slugify(self.get_full_name())):
                self.slug = slugify(self.get_full_name())
            elif not Member.objects.filter(
                    slug__exact=slugify(f'{self.first_name} {self.last_name} {self.suffix}')):
                self.slug = slugify(
                    f'{self.first_name} {self.last_name} {self.suffix}'
                )
            elif not Member.objects.filter(
                    slug__exact=slugify(f'{self.first_name} {self.middle_name} {self.last_name} {self.suffix}')):
                self.slug = slugify(
                    f'{self.first_name} {self.middle_name} {self.last_name} {self.suffix}'
                )
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        if hasattr(self, 'adultmember'):
            return reverse('parent_detail', args=[str(self.id)])
        elif hasattr(self, 'childmember'):
            return reverse('scout_detail', args=[str(self.id)])
        else:
            return None

    def get_full_name(self):
        """
        Return the short name, either first_name or nickname, plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.get_short_name(), self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        if self.nickname:
            return self.nickname
        else:
            return self.first_name


class Family(models.Model):
    """
    Members who are related are tracked by this model
    """
    name = models.CharField(max_length=64, blank=True, null=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    legacy_id = models.PositiveSmallIntegerField(unique=True, blank=True, null=True)
    date_added = models.DateField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]
        ordering = ['date_added']
        verbose_name = _('Family')
        verbose_name_plural = _('Families')

    def __str__(self):
        if self.name:
            return self.name

    def save(self, *args, **kwargs):
        last_names = []
        for parent in self.adults.filter(role__exact=AdultMember.PARENT):
            if parent.last_name not in last_names:
                last_names.append(parent.last_name)
        self.name = '-'.join(last_names) + ' Family'
        return super().save(*args, **kwargs)


class AdultMember(AbstractBaseUser, PermissionsMixin, Member):
    """
    Any adult member such as a parent, guardian, or other use this model. Being an adult gives you access to the
    website with an e-mail address and password.
    """

    # Define the various roles an adult member can have within the Pack
    PARENT = 'P'
    GUARDIAN = 'G'
    CONTRIBUTOR = 'C'
    ROLE_CHOICES = (
        (PARENT, _('Parent')),
        (GUARDIAN, _('Guardian')),
        (CONTRIBUTOR, _('Friend of the Pack')),
    )

    email = models.EmailField(_('Email Address'), unique=True)
    is_published = models.BooleanField(_('Published'), default=True, help_text=_(
        "Do you want to publish this address in the Pack directory so that other members can contact you directly?"
    ))

    role = models.CharField(_('Role'), max_length=1, choices=ROLE_CHOICES, default=PARENT)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='adults', blank=True, null=True)

    objects = MemberManager()
    is_staff = models.BooleanField(
        _('Staff'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        indexes = [models.Index(fields=['role', 'email', 'family'])]
        verbose_name = _('Adult')
        verbose_name_plural = _('Adults')

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_active_scouts(self):
        """ Return a list of all currently active scouts associated with this member. """
        if self.family:
            return self.family.children.filter(status__exact=ChildMember.ACTIVE)

    def get_partners(self):
        """ Return a list of other parents who share the same scout(s) """
        if self.family:
            return self.family.adults.exclude(id=self.id)

    @property
    def active(self):
        """ If member has scouts who are currently, then they should also be considered active in the Pack. """
        if self.get_active_scouts():
            return True
        else:
            return False


class ChildMember(Member):
    """
    Cub scouts use this model to store profile details
    """

    # Define the various statuses a Scout can be. Are the a currently active member, new applicant, or even graduated?
    APPLIED = 1
    DENIED = 2
    APPROVED = 3
    INACTIVE = 4
    ACTIVE = 5
    GRADUATED = 6
    STATUS_CHOICES = (
        (APPLIED, _('Applied')),
        (DENIED, _('Denied')),
        (APPROVED, _('Approved')),
        (INACTIVE, _('Inactive')),
        (ACTIVE, _('Active')),
        (GRADUATED, _('Graduated')),
    )

    school = models.ForeignKey('address_book.Venue', on_delete=models.CASCADE, blank=True, null=True,
                               limit_choices_to={'type__type__icontains': 'School'}, help_text=_(
        "Tell us what school your child attends. If your school isn't listed, tell us in the comments section."))

    # Give parents an opportunity to add more detail to their application
    reference = models.CharField(_('Referral(s)'), max_length=128, blank=True, null=True, help_text=_(
        "If you know someone who is already in the pack, you can tell us their name."))
    member_comments = models.TextField(_('Comments'), blank=True, null=True, help_text=_(
        "What other information should we consider when reviewing your application?"))

    # These fields should be managed by the person(s) in charge of membership
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    pack_comments = models.TextField(_('Pack Comments'), blank=True, null=True, help_text=_(
        "Used by pack leadership to keep notes about a specific member."
        "This information is not generally disclosed to the member unless they are granted access to Membership."
    ))
    status = models.PositiveSmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=APPLIED, help_text=(
        "What is the Cub's current status? A new cub who has not been reviewed will start as 'Applied'."
        "Membership can choose then to approve or decline the application, or make them active."
        "Once a Cub is no longer active in the pack, either through graduation or attrition, note that status here."
        "Any adult member connected to this Cub will get access only once the Cub's status is 'Active' or 'Approved'."
    ))
    den = models.ForeignKey('dens.Den', on_delete=models.CASCADE, related_name='scouts', blank=True, null=True)

    # Important dates
    date_of_birth = models.DateField(_('Birthday'), blank=True, null=True)
    started_school = models.PositiveSmallIntegerField(_('year started school'), default=two_years_ago, null=True, help_text=_(
        "What year did your child start kindergarten? We use this to assign your child to an appropriate den."))
    started_pack = models.DateField(_('Date Started'), blank=True, null=True, help_text=_(
        "When does this cub join their first activity with the pack?"
    ))

    class Meta:
        indexes = [models.Index(fields=['school', 'family', 'status', 'den', 'date_of_birth', 'started_school'])]
        verbose_name = _('Cub')
        verbose_name_plural = _('Cubs')

    @property
    def age(self):
        """ Calculates the cub scout's age when a birthday is specified """
        if not self.date_of_birth:
            return None
        today = timezone.now()
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def get_siblings(self):
        """ Return a list of other Scouts who share the same parent(s) """
        if self.family:
            return self.family.children.exclude(id=self.id)

    @property
    def grade(self):
        """ Based on when this cub started school, what grade should they be in now? """
        if self.started_school:
            this_year = timezone.now().year
            if timezone.now().month < 9:  # assumes that a school year begins in September
                this_year -= 1

            calculated_grade = this_year - self.started_school
            if calculated_grade < 0:
                # this Scout hasn't started Kindergarten yet
                return None
            elif calculated_grade == 0:
                # this Scout is a kindergartner
                return 'K'
            elif calculated_grade <= 12:
                return calculated_grade
            else:
                # this Scout isn't in grade school anymore
                return None

    @property
    def rank(self):
        """ A cub's rank is derived from the den they are a member of. """
        return self.den.rank


saved_file.connect(generate_aliases)
