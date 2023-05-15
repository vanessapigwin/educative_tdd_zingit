from django import forms
from django.db.models.base import Model
from Zing_It_App.models import Song, Playlist


class CustomMMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, playlist_id):
        return f"{playlist_id.name}"

class SignUpForm(forms.Form):
    full_name = forms.CharField(label='Full name', max_length=100)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label = 'Confirm password', required=True, widget=forms.PasswordInput())

    def verify_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password confirmation does not match, please try again.')
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class SongModelForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['track', 'artist', 'album', 'length', 'playlist_id']

        playlist_id = CustomMMMCF(
            queryset=Playlist.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )