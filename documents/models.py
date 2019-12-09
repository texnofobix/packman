from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


def document_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/category_slug/<filename>
    return 'documents/{0}/{1}'.format(slugify(instance.category), filename)


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Document(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(help_text=_('Brief description of what the document is.'), blank=True, null=True)
    file = models.FileField(upload_to=document_upload_path)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='documents')
    display_in_repository = models.BooleanField(help_text=_('Make this document visible in the Document Repository'), default=True)

    date_added = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name', ]
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def get_file_type(self):
        extension = self.file.file.split('.')[-1]
        if extension == 'txt':
            return _('text document')
        if extension == 'pdf':
            return _('PDF')
        if extension == 'doc' or 'docx':
            return _('Microsoft Word Document')
        if extension == 'xls' or 'xlsx':
            return _('Microsoft Excel Spreadsheet')
        if extension == 'ppt' or 'pptx':
            return _('Microsoft Powerpoint Presentation')
        if extension == 'jpg' or 'jpeg' or 'gif' or 'png':
            return _('Image')
