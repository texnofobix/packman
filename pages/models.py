import uuid

from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField

from .managers import ContentBlockManager


class Page(models.Model):
    """
    Base model used to define a web page. Used by Dynamic and Static pages.
    """
    HOME = 'HOME'
    ABOUT = 'ABOUT'
    HISTORY = 'HISTORY'
    SIGNUP = 'SIGNUP'
    PAGE_CHOICES = (
        (HOME, _("Home")),
        (ABOUT, _("About Us")),
        (HISTORY, _("History")),
        (SIGNUP, _("Join Us")),
    )
    page = models.CharField(
        max_length=8,
        choices=PAGE_CHOICES,
        unique=True,
        blank=True,
        null=True,
    )
    title = models.CharField(
        max_length=64,
    )

    include_in_nav = models.BooleanField(
        _("Include in navigation"),
        default=False,
        help_text=_(
            "Checking this option will add this page to the site's menu bar."),
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
    )

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        indexes = [models.Index(fields=['title'])]
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.page == self._meta.model.HOME:
            return reverse_lazy('pages:home')
        elif self.page == self._meta.model.ABOUT:
            return reverse_lazy('pages:about')
        elif self.page == self._meta.model.HISTORY:
            return reverse_lazy('pages:history')
        elif self.page == self._meta.model.SIGNUP:
            return reverse_lazy('pages:signup')
        else:
            return reverse_lazy('pages:detail', kwargs={'slug': self.slug})


class ContentBlock(models.Model):
    """
    Pages can contain any number of content blocks. Each block has its own
    visibility, allowing for different content to be displayed based on whether
    a user is logged in and has permission.
    """
    PUBLIC = 'P'
    PRIVATE = 'S'
    ANONYMOUS = 'A'
    VISIBILITY_CHOICES = [
        (PUBLIC, _("Public")),
        (PRIVATE, _("Private")),
        (ANONYMOUS, _("Anonymous"))
    ]

    title = models.CharField(
        max_length=256,
        blank=True,
        default="",
    )
    visibility = models.CharField(
        max_length=1,
        choices=VISIBILITY_CHOICES,
        default=PRIVATE,
        help_text=(
            "Private content will only be viewable to active members or "
            "contributors. Public content is viewable by anyone on the "
            "website, including applicants, alumni, and anonymous visitors. "
            "Anonymous content will be displayed if no user is logged-in."),
    )
    body = HTMLField()
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='content_blocks',
    )

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        blank=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )
    published_on = models.DateTimeField(
        default=timezone.now,
        blank=True,
        null=True,
    )

    objects = ContentBlockManager()

    class Meta:
        indexes = [models.Index(fields=['title', 'published_on'])]
        ordering = ['-published_on']
        verbose_name = _("Content Block")
        verbose_name_plural = _("Content Blocks")

    def __str__(self):
        if self.title:
            return self.title
        else:
            return f"{strip_tags(self.body)[:25]}..."
