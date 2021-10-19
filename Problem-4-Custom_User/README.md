<h1>Custom User Model</h1>
<h3>models.py</h3>
<pre>
<code>
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self,full_name,phonenumber,email,password=None,admin=False,active=False):
        if not full_name:
            raise ValueError(_("Please Enter Full Name !."))
        if not phonenumber:
            raise ValueError(_("Please Enter Mobile Number !."))
        if not email:
            raise ValueError(_("Please Enter Email !."))
        if not password:
            raise ValueError(_("Please Enter Password !."))
        user=self.model(email=self.normalize_email(email),
                        full_name=full_name,
                        phonenumber=phonenumber,
                        admin=admin,
                        active=active,
                        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,full_name,phonenumber,email,password=None,admin=True,active=True):
        user=self.create_user(full_name,phonenumber,email,password,admin,active)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    full_name=models.CharField(max_length=255,verbose_name="Full Name")
    email=models.EmailField(unique=True,max_length=255,verbose_name="Email")
    phonenumber=models.CharField(max_length=255,verbose_name="Mobile Number",unique=True)
    admin=models.BooleanField(default=False)
    active=models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)
  

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['full_name','phonenumber']
    objects=MyUserManager()

    def __str__(self):
        return str(self.phonenumber)
    
    def is_active(self):
        return self.active

    def is_staff(self):
        return self.admin
    
    def is_admin(self):
        return self.admin

    def is_superuser(self):
        return self.admin
    
    def has_perm(self,perm,obj=None):
        return True
        
    def has_perms(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True
</code>
</pre>
<hr>
<h3>forms.py</h3>
<pre>
	<code>
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    phonenumber=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['phonenumber'].widget.attrs['class'] ='input'
        self.fields['password'].widget.attrs['class'] ='input'
    
    def clean_phonenumber(self):
        phone=self.cleaned_data.get('phonenumber',False)
        if(phone and len(str(phone))==10 and phone.isnumeric()):
            try:
                User.objects.get(phonenumber=phone)
            except:
                raise forms.ValidationError("Mobile Number Not Registered.!")
        else:
            raise forms.ValidationError("Please Enter Valid Mobile Number .!")
        return phone
    
    def clean_password(self):
        password=self.cleaned_data.get('password',False)
        if(password and len(password)>1):
            pass
        else:
            raise forms.ValidationError("Please Enter Password Correctly .!")
        return password

    def clean(self):
        cleaned_data=super().clean()
        phonenumber_=cleaned_data.get('phonenumber',None)
        password_=cleaned_data.get('password',None)
        if phonenumber_ and password_:
            pass
        else:
            raise forms.ValidationError("Please Enter Valid Details .!")




    

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','full_name','phonenumber')
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['full_name'].widget.attrs['id'] = 'full_name'
        self.fields['phonenumber'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['phonenumber'].widget.attrs['id'] = 'phonenumber'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].widget.attrs['id'] = 'email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['id'] = 'password1'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['id'] = 'password2'
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already taken .!")
        return email
    
    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
        if(len(str(phonenumber)) != 10):
            raise forms.ValidationError("Enter Valid Phonenumber .!") 
        qs = User.objects.filter(phonenumber=phonenumber)
        if qs.exists():
            raise forms.ValidationError("Phonenumber is Already taken .!")
        return phonenumber

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if not password1 or len(str(password1))<5:
            raise forms.ValidationError("Enter Valid Password.!")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        if not password2 or len(str(password2))<5:
            raise forms.ValidationError("Enter Valid Password.!")
        return password2
    
    
    def clean(self):
        cleaned_data=super().clean()
        password2 = self.cleaned_data.get("password2")
        password1 = self.cleaned_data.get("password1")
        if(password1 and password2):
            if(password1!=password2):
                raise forms.ValidationError("Password Not Matched .!")
        else:
            raise forms.ValidationError("Enter Passwrods .!")


class UserAdminCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','full_name','phonenumber','admin')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active=True
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','full_name','phonenumber', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]
   </code>
</pre>
<hr>
<h3>admin.py</h3>
<pre>
	<code>
		from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm



User=get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ('email', 'admin','active')
    list_filter = ('admin','active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name','phonenumber')}),
        ('Permissions', {'fields': ('admin','active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','full_name','phonenumber','password1', 'password2')}
        ),
    )
    search_fields = ('email','full_name')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
	</code>
</pre>
