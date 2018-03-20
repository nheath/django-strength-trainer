from django import forms
from .models import user_model
from django.core.validators import validate_email, validate_slug, MinValueValidator, MaxValueValidator 
