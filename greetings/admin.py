from django.contrib import admin
from .models import VisitTracking, GameInteraction, DiyaLightTracking

# Register your models here.

@admin.register(VisitTracking)
class VisitTrackingAdmin(admin.ModelAdmin):
    list_display = ['contact', 'visited_at', 'device_type', 'ip_address']
    list_filter = ['device_type', 'visited_at']
    search_fields = ['contact__contact_name', 'contact__greeting_name', 'ip_address']
    readonly_fields = ['visited_at', 'ip_address', 'user_agent', 'device_type']
    date_hierarchy = 'visited_at'
    
    def has_add_permission(self, request):
        return False


@admin.register(GameInteraction)
class GameInteractionAdmin(admin.ModelAdmin):
    list_display = ['contact', 'event_type', 'is_completed', 'score', 'diyas_lit', 'time_taken_seconds', 'started_at', 'device_type']
    list_filter = ['event_type', 'is_completed', 'device_type', 'started_at']
    search_fields = ['contact__contact_name', 'contact__greeting_name']
    readonly_fields = ['started_at', 'completed_at', 'ip_address', 'device_type', 'score']
    date_hierarchy = 'started_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('contact', 'event_type')
        }),
        ('Game Progress', {
            'fields': ('diyas_lit', 'total_diyas', 'is_completed', 'score')
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'time_taken_seconds')
        }),
        ('Device Information', {
            'fields': ('device_type', 'ip_address')
        }),
    )
    
    def has_add_permission(self, request):
        return False


@admin.register(DiyaLightTracking)
class DiyaLightTrackingAdmin(admin.ModelAdmin):
    list_display = ['game_interaction', 'diya_number', 'lit_at', 'time_from_start']
    list_filter = ['lit_at']
    search_fields = ['game_interaction__contact__contact_name']
    readonly_fields = ['lit_at', 'time_from_start']
    date_hierarchy = 'lit_at'
    
    def has_add_permission(self, request):
        return False
