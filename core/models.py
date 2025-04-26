from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create a UserProfile automatically when a User is created
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):
    USER_ROLES = (
        ('regular', 'Regular User'),
        ('admin', 'Administrator'),
        ('superuser', 'Superuser'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=USER_ROLES, default='regular')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class UserReport(models.Model):
    DIFFICULTIES = (
                        ('easy', "Easy"),
                        ('medium', 'Medium'), 
                        ('hard', 'Hard')
    )
    #TYPES = (
    #            ('quiz', 'Quiz'),
    #            ('training','Training')
    #)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTIES)
    #report_type = models.CharField(max_length=20, choices=TYPES)
    responses = models.JSONField(null=True, blank=True)
    num_questions = models.IntegerField(null=True, blank=True)
    score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    time_stamp = models.DateTimeField(default=timezone.now)

class FrequentQuestions(models.Model):
    question = models.CharField(max_length=500, null=True, blank=True)
    times_asked = models.IntegerField(default=1)
