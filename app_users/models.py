# bu app_users dagi models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from app_common.models import BaseModel

class ProfileModel(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profiles/', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'heic'])
    ])
    bio = models.TextField(blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

