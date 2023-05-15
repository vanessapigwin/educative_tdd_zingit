from django.test import TestCase
from django.urls import reverse
from Zing_It_App.forms import LoginForm, SignUpForm, SongModelForm
from Zing_It_App.test_helpers import register_new_user, test_email, test_password, mock_playlist_and_songs

class TestLoginForm(TestCase):       
    
    def test_form_instance(self):
        response = self.client.get(reverse('login'))
        form = response.context.get('form')
        self.assertIsInstance(form, LoginForm)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_login_successful(self):
        # correct credentials in login form will redirect to home
        registered_user = register_new_user()

        response = self.client.post(reverse('login'), data={'email':test_email, 'password':test_password})
        self.assertRedirects(response, reverse('index'), fetch_redirect_response=True)

    def test_login_fail(self):
        response = self.client.post(reverse('login'), data={'email':'wrong@test.com', 'password':'wrong password'})
        self.assertContains(response, "try again")

    def test_form_validators(self):
        empty_form = LoginForm(data={
            'email':'',
            'password':''
        })
        self.assertFalse(empty_form.is_valid())

    def test_invalid_email(self):
        invalid_form = LoginForm(
            data = {
                'email':'huehue',
                'password':''
            }
        )
        self.assertFalse(invalid_form.is_valid())


class TestSignUpForm(TestCase):

    def test_signup_form_instance(self):
        response = self.client.get(reverse('signup'))
        form = response.context.get('form')
        self.assertIsInstance(form, SignUpForm)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_empty_signup_form(self):
        empty_form = SignUpForm(data={
            'full_name':'',
            'email':'',
            'password':'',
            'confirm_password':''
        })
        self.assertFalse(empty_form.is_valid())
    
    def test_signup_different_passwords(self):

        response = self.client.post(reverse('signup'),data={
            'full_name':'winwin chicken',
            'email':'fatboi@mail.com',
            'password':'intendedpassword',
            'confirm_password':'misspelledpassword'
        })

        self.assertContains(response, 'Password confirmation does not match, please try again.')
    
    def test_signup_email_already_used(self):
        registered_user = register_new_user()

        response = self.client.post(reverse('signup'), data={
            'full_name':'winwin chicken',
            'email':registered_user.email,
            'password':'intendedpassword',
            'confirm_password':'intendedpassword'
        })
        form = response.context.get('form')

        self.assertTrue(form.is_valid())
        self.assertContains(response, 'Email already registered, please login.')


class Test_Edit_Form(TestCase):

    def setUp(self):
        register_new_user()
        self.client.login(username=test_email, password=test_password)

        self.playlist, self.song = mock_playlist_and_songs()
        self.response = self.client.get(reverse('edit', kwargs={'id':self.playlist.id}))

    def test_form_instance(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        form = self.response.context.get('form')
        self.assertIsInstance(form, SongModelForm)

    def test_form_contents(self):
        self.assertContains(self.response, self.song.artist)

    def test_update_entry_reflected(self):
        form_data = SongModelForm(instance=self.song).initial
        form_data['artist'] = 'winwin'
        response = self.client.post(reverse('edit', kwargs={'id':self.playlist.id}), data=form_data)
        form = response.context.get('form')

        self.assertEqual(form['artist'].value(), 'winwin')
