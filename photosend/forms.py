from django.forms import ModelForm
from .models import Photo
from .models import Comment

class PhotoForm(ModelForm):
  class Meta:
    model=Photo
    fields=['title','content','photo']

class CommentForm(ModelForm):
  class Meta:
    model=Comment
    fields=['comment']
