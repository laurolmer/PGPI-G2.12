from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'w-full py-4 px-6 rounded-xl'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'w-full py-4 px-6 rounded-xl'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)
    

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid email/password.")
        if not user.check_password(password):
            raise forms.ValidationError("Invalid email/password.")
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.")
        
        # Set user_cache after successful authentication
        self.user_cache = user

        return self.cleaned_data

    def get_user(self):
        return self.user_cache 
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario','class': 'w-full py-4 px-6 rounded-xl'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Tu email','class': 'w-full py-4 px-6 rounded-xl'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña','class': 'w-full py-4 px-6 rounded-xl'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repite contraseña','class': 'w-full py-4 px-6 rounded-xl'}))
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('id','username','email','password')
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario','class': 'w-full py-4 px-6 rounded-xl'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Tu email','class': 'w-full py-4 px-6 rounded-xl'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña','class': 'w-full py-4 px-6 rounded-xl'}))
 