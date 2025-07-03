from django.db import models

class SelfAssessment(models.Model):
    USER_TYPE_CHOICES = [
        ('self', 'Self'),
        ('student', 'Student'),
    ]

    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    age_group = models.CharField(max_length=10)  # e.g., '10-15', '16-20'
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    score = models.PositiveIntegerField()
    
    # Contact info to be filled later via follow-up form
    contact_info = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment #{self.id} - Score: {self.score}"
