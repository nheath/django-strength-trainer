from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email, validate_slug, MinValueValidator, MaxValueValidator 
from django.template.defaultfilters import mark_safe
from django.contrib.auth.models import User
from django import forms

# addapted from https://stackoverflow.com/questions/10332865/how-to-customize-django-form-label?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
class NewWorkoutForm(forms.Form):
    max_squat = forms.IntegerField(
        min_value=0,
        max_value=9999,
        label = mark_safe('<strong>Back Squat 1 RM</strong>'
        )
    )
    max_bench = forms.IntegerField(
        min_value=0,
        max_value=9999,
        label = mark_safe('<strong>Bench Press 1 RM</strong>')
    )
    max_deadlift = forms.IntegerField(
        min_value=0,
        max_value=9999,
        label = mark_safe('<strong>Deadlift 1 RM</strong>')
    )
    max_overhead = forms.IntegerField(
        min_value=0,
        max_value=9999,
        label = mark_safe('<strong>Overhead Press 1 RM</strong>')
    )

class LoginForm(AuthenticationForm):
    username=forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(attrs={
            'name':'username'
        })
    )
    password=forms.CharField(
        label="Password",
        max_length=32,
        widget=forms.PasswordInput()
    )

class registration_form(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
        )

    class Meta:
        model = User
        fields = ("username", "email",
            "password1", "password2")

    def save(self, commit=True):
        user=super(registration_form,self).save(commit=False)
        user.email=self.cleaned_data["email"]
        if commit:
            user.save()
        return user