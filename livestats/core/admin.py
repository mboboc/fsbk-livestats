from django.contrib import admin
from django.utils.html import mark_safe
from datetime import date

from .models import FSTeam, FSTeamMember, FSTimeResult
from admin_auto_filters.filters import AutocompleteFilterFactory



@admin.register(FSTeam)
class FSTeamAdmin(admin.ModelAdmin):
    list_display = ("name", "flag", "logo_image")
    search_fields = ("name", "fsbk_id")

    def logo_image(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="50" height="50" />')
        return "-"

    logo_image.short_description = "Logo"


@admin.register(FSTeamMember)
class FSTeamMemberAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name", "nickname", "team__name", "fsbk_id")
    list_display = ("team", "fsbk_id", "first_name", "last_name", "nickname", "is_driver", "driver_image")

    def driver_image(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" />')
        return "-"

    driver_image.short_description = "Driver Photo"


class EventDayFilter(admin.SimpleListFilter):
    title = 'Event Day'
    parameter_name = 'event_day'

    # Map dates to aliases
    DAY_ALIASES = {
        # date(2025, 7, 28): 'Day 1',
        # date(2025, 7, 29): 'Day 2',
        # date(2025, 7, 30): 'Day 3',
        date(2025, 7, 31): 'Day 4 - Thursday',
        date(2025, 8, 1): 'Day 5 - Friday',
        date(2025, 8, 2): 'Day 6 - Saturday',
    }

    def lookups(self, request, model_admin):
        return [(d.isoformat(), alias) for d, alias in self.DAY_ALIASES.items()]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            try:
                day = date.fromisoformat(value)
                return queryset.filter(created_at__date=day)
            except ValueError:
                return queryset.none()
        return queryset


@admin.register(FSTimeResult)
class FSTimeResultAdmin(admin.ModelAdmin):
    list_display = ("driver", "event", "time_result", "created_at")
    readonly_fields = ("created_at",)
    fields = ("driver", "event", "time_result", "created_at")
    autocomplete_fields = ("driver",)

    list_filter = (
        AutocompleteFilterFactory("Team", "driver__team"),
        AutocompleteFilterFactory("Driver", "driver"),
        EventDayFilter
    )
    search_fields = ("driver__first_name",)
