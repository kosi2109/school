from .models import UserNew,ClassRoom
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = UserNew
        fields = ('username','is_student','is_teacher')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = UserNew
        fields = ('username','is_student','is_teacher')


class RoomForm(forms.ModelForm):
	class Meta:
		model = ClassRoom
		exclude = '__all__'

