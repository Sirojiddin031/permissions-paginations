from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from app_users.models import ProfileModel
from app_users.utils import generate_verification_code, send_verification_email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Yangi foydalanuvchi yaratilganda avtomatik profil yaratish"""
    if created:
        verification_code = generate_verification_code()
        profile = ProfileModel.objects.create(user=instance, verification_code=verification_code)

        send_verification_email(instance.email, verification_code)
