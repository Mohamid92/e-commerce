from django import forms
from django.forms import ModelForm
from .models import Account


class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['phone_number', 'password','email','first_name','last_name']
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder']='Enter Email'
        for field_name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )
    