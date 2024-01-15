from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account,Comment

class UserAccountForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Account.objects.create(user=user, phone=self.cleaned_data['phone'])
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.capitalize(),
            })

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
