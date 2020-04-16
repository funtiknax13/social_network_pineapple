from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'gender', 'city', 'birth_date')
