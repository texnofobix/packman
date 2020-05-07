from django.contrib.auth.models import UserManager
from django.db import models

from dens.models import Rank
from pack_calendar.models import PackYear


class MemberManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Custom user model manager where email is the unique identifiers for
        authentication instead of usernames. All other code is shamelessly
        ripped off directly from Django's own UserManager
        https://github.com/django/django/blob/master/django/contrib/auth/models.py
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class ScoutQuerySet(models.QuerySet):
    def active(self):
        return self.filter(
            den__year_assigned=PackYear.get_current_pack_year(),
            status=4,  # Scout.ACTIVE
        )

    def bobcats(self):
        return self.active().filter(
            den__den__rank__rank=Rank.BOBCAT
        )

    def tigers(self):
        return self.active().filter(
            den__den__rank__rank=Rank.TIGER
        )

    def wolves(self):
        return self.active().filter(
            den__den__rank__rank=Rank.WOLF
        )

    def bears(self):
        return self.active().filter(
            den__den__rank__rank=Rank.BEAR
        )

    def jr_webes(self):
        return self.active().filter(
            den__den__rank__rank=Rank.JR_WEBE
        )

    def sr_webes(self):
        return self.active().filter(
            den__den__rank__rank=Rank.SR_WEBE
        )

    def arrows_of_light(self):
        return self.active().filter(
            den__den__rank__rank=Rank.ARROW
        )

    def animal_ranks(self):
        return self.active().filter(
            den__den__rank__rank__lte=Rank.BEAR
        )

    def webelo_ranks(self):
        return self.active().filter(
            den__den__rank__rank__gte=Rank.JR_WEBE
        )


class ScoutManager(models.Manager):
    def get_queryset(self):
        return ScoutQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def bobcats(self):
        return self.get_queryset().bobcats()

    def tigers(self):
        return self.get_queryset().tigers()

    def wolves(self):
        return self.get_queryset().wolves()

    def bears(self):
        return self.get_queryset().bears()

    def jr_webes(self):
        return self.get_queryset().jr_webes()

    def sr_webes(self):
        return self.get_queryset().sr_webes()

    def arrows_of_lights(self):
        return self.get_queryset().arrows_of_light()

    def animal_ranks(self):
        return self.get_queryset().animal_ranks()

    def webelo_ranks(self):
        return self.get_queryset().webelo_ranks()
