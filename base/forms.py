from django import forms
from .models import user

class Usercreation(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class']='form-control my-3'
            i.field.widget.attrs['placeholder']=i.field.label
        self.fields['password'].widget.attrs['placeholder']='Enter your password'
        self.fields['cpassword'].widget.attrs['placeholder']='Confirm your password'
    password=forms.CharField(widget=forms.PasswordInput)
    cpassword=forms.CharField(widget=forms.PasswordInput)
    


    class Meta:
        model=user
        fields='__all__'