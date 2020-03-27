from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone

class Photo(models.Model):
  title = models.CharField(null=True, blank=True, max_length=150)
  content = models.TextField(null=True, blank=True,max_length=500)
  photo = models.ImageField(upload_to = 'photos')
  created_at = models.DateTimeField(default=timezone.now)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  like_num = models.IntegerField(default=0)


  def __str__(self):
    return self.title 

class Comment(models.Model):
  comment = models.TextField(null=True, blank=True,max_length=300)
  created_at = models.DateTimeField(default=timezone.now)
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

  def __str__(self):
    return self.comment 

class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='like_user')
  photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
  date_created = models.DateTimeField(auto_now_add=True)


