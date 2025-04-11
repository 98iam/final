from django.db import models
from django.contrib.auth.models import User

class SupabaseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    supabase_uid = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.user.username