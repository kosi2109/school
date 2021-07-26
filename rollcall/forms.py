from .models import UserNew,ClassRoom,PostArticle
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from ckeditor.fields import RichTextField

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
		exclude = ('name','qr_code','can_join','teacher',)
		widgets = {
			'major': forms.Select(attrs={'class':'form-control'}),
			'year': forms.Select(attrs={'class':'form-control'}),
			'subject': forms.Select(attrs={'class':'form-control'}),
			'password': forms.TextInput(attrs={'class':'form-control','type':'password'}),
		}

class PostForm(forms.ModelForm):
  	
    class Meta:
        model  = PostArticle
        fields = ('content','post',)
        widgets = {
        	'post': forms.TextInput(attrs={'id':'po', 'value':'','type':'hidden'}),
        }