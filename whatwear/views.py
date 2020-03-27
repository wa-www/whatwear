from django.shortcuts import render,redirect

# Create your views here.
from allauth.account.decorators import verified_email_required
# from .forms import PhotoForm


def index(request):
  return render(request,'photosend/index')

