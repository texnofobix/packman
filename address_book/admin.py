from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Address, PhoneNumber, Venue, Category, DistributionList


class PhoneNumberInline(admin.TabularInline):
    exclude = ['member', 'date_added', 'published', 'type']
    extra = 0
    model = PhoneNumber


class AddressInline(admin.StackedInline):
    exclude = ['member', 'date_added', 'published', 'type']
    model = Address


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    inlines = [AddressInline, PhoneNumberInline]
    list_filter = ('categories', )
    list_display = ('name', "get_category_list")
    search_fields = ('name', )

    def get_category_list(self, obj):
        return ", ".join(category.name for category in obj.categories.all())

    get_category_list.short_description = _("categories")


@admin.register(DistributionList)
class DistributionListAdmin(admin.ModelAdmin):
    filter_horizontal = ("committees", "dens")
    list_display = (
        "name",
        "email",
        "is_all",
        "get_den_list",
        "get_committee_list",
        "contact_us",
    )
    list_filter = ["contact_us"]

    def get_den_list(self, obj):
        return ", ".join(str(den.number) for den in obj.dens.all())

    get_den_list.short_description = _("dens")

    def get_committee_list(self, obj):
        return ", ".join(committee.name for committee in obj.committees.all())

    get_committee_list.short_description = _("committees")


admin.site.register(Category)
