from django.contrib import admin
from .models import ContactMessage


# Register your models here.
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message", "status")
    list_filter = ("status",)
    actions = ["accept_complaint", "decline_complaint"]

    def accept_complaint(self, request, queryset):
        queryset.update(status="Accepted")

    def decline_complaint(self, request, queryset):
        queryset.update(status="Declined")

    accept_complaint.short_description = "Mark selected complaints as Accepted"
    decline_complaint.short_description = "Mark selected complaints as Declined"
