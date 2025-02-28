from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator


from app_common.models import BaseModel


class PostsModel(BaseModel):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="posts")
    image = models.ImageField(upload_to='profiles',validators=[FileExtensionValidator(allowed_extensions=['png','jpg','heic'])])
    slug = models.SlugField(unique=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
