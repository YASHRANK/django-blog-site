from django import forms    
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post , Comment
from tinymce.widgets import TinyMCE




class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class':'form-control','placeholder':'Firstname'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control','placeholder':'Lastname'})
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'})
        self.fields['email'].widget.attrs.update({'class':'form-control', 'placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({'class':'form-control','placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'class':'form-control','placeholder':'Confirm Password'})
        
            
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']


class CreatPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tags'].widget.attrs.update({'placeholder':'enter tags'})

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'tags']
        widgets = {
        'content': TinyMCE(),
        }
    
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['body']
