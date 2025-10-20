from django.db import models
from contact.models import Contact
from django.utils import timezone

# Create your models here.

class VisitTracking(models.Model):
    """Track when users visit the landing page"""
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='visits')
    visited_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=50, blank=True)  # mobile, tablet, desktop
    
    class Meta:
        ordering = ['-visited_at']
        verbose_name = 'Visit Tracking'
        verbose_name_plural = 'Visit Trackings'
    
    def __str__(self):
        return f"{self.contact.contact_name} - {self.visited_at.strftime('%Y-%m-%d %H:%M')}"


class GameInteraction(models.Model):
    """Track user interactions with the game"""
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='game_interactions')
    event_type = models.CharField(max_length=20)  # diwali, newyear, bhaidooj
    
    # Interaction details
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    # Diwali-specific tracking
    diyas_lit = models.IntegerField(default=0)
    total_diyas = models.IntegerField(default=7)
    time_taken_seconds = models.IntegerField(null=True, blank=True)  # Time to complete
    
    # Score tracking
    score = models.IntegerField(default=0)
    
    # Device info
    device_type = models.CharField(max_length=50, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Game Interaction'
        verbose_name_plural = 'Game Interactions'
    
    def __str__(self):
        status = "Completed" if self.is_completed else "In Progress"
        return f"{self.contact.contact_name} - {self.event_type} - {status}"
    
    def calculate_score(self):
        """Calculate score based on completion and time"""
        if not self.is_completed:
            return self.diyas_lit * 10
        
        base_score = 100
        time_bonus = max(0, 300 - (self.time_taken_seconds or 0)) if self.time_taken_seconds else 0
        return base_score + time_bonus
    
    def completion_percentage(self):
        """Get completion percentage"""
        if self.total_diyas == 0:
            return 0
        return int((self.diyas_lit / self.total_diyas) * 100)


class DiyaLightTracking(models.Model):
    """Track individual diya lighting events"""
    game_interaction = models.ForeignKey(GameInteraction, on_delete=models.CASCADE, related_name='diya_events')
    diya_number = models.IntegerField()
    lit_at = models.DateTimeField(auto_now_add=True)
    time_from_start = models.FloatField()  # Seconds from game start
    
    class Meta:
        ordering = ['lit_at']
        verbose_name = 'Diya Light Event'
        verbose_name_plural = 'Diya Light Events'
    
    def __str__(self):
        return f"Diya {self.diya_number} - {self.game_interaction.contact.contact_name}"
