from django.contrib import admin

from .models import LegalReason, LegalReasonGroup, PrivacyEvent, PrivacyLog
from .forms import LegalReasonGroupForm


class NoPermissionMixin(object):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PrivacyEventInline(NoPermissionMixin, admin.StackedInline):
    extra = 0
    model = PrivacyEvent


class PrivacyLogAdmin(NoPermissionMixin, admin.ModelAdmin):
    fields = ("get_generic_fk", "created")
    readonly_fields = ("get_generic_fk", "created")
    inlines = [PrivacyEventInline]

    def get_generic_fk(self, obj):
        return obj.content_object

    get_generic_fk.short_description = "Related object"


class LegalReasonInline(admin.StackedInline):
    extra = 1
    model = LegalReason


class LegalReasonGroupAdmin(admin.ModelAdmin):
    inlines = [LegalReasonInline]
    form = LegalReasonGroupForm


admin.site.register(LegalReason)
admin.site.register(LegalReasonGroup, LegalReasonGroupAdmin)
admin.site.register(PrivacyLog, PrivacyLogAdmin)
