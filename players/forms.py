from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from players.models import Player

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': _("Nickname"),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class PlayerForm(ModelForm):
	class Meta:
		model = Player
		fields = ['gender', 'age', 'country', 'education']
