from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from Zing_It_App.test_helpers import mock_playlist_and_songs, register_new_user, test_password, test_email


class TestLoggedOut(SimpleTestCase):

    def test_access_fail_home(self):
        self.response = self.client.get(reverse('index'))
        self.assertNotEqual(self.response.status_code, 200)

    def test_access_fail_playlist(self):
        self.response = self.client.get(reverse('playlist', kwargs={'n':1}))
        self.assertNotEqual(self.response.status_code, 200)


class TestHomePage(TestCase):
    """
        Test home page's url, template load, and view function load.
    """
    def setUp(self):
        register_new_user()
        self.client.login(username=test_email, password=test_password)
        self.response = self.client.get(reverse('index'))

    def test_index_url_name_and_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'zing_it/home.html')
        self.assertContains(self.response, "Zing It")


class TestPlaylistPage(TestCase):
    """
        Test playlist page's url, template load and view function load.
    """
    def setUp(self):
        register_new_user()
        self.playlist, self.song = mock_playlist_and_songs()
        self.client.login(username=test_email, password=test_password)
        self.response = self.client.get(reverse('playlist', kwargs={'n':self.playlist.id}))

    def test_playlist_url_name(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_playlist_template(self):    
        self.assertTemplateUsed(self.response, "zing_it/songs.html")

    def test_playlistname_content(self):
        self.assertContains(self.response, self.playlist.name)

    def test_song_loaded(self):
        self.assertContains(self.response, self.song.artist)


class TestSignupPage(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('signup'))

    def test_signup_page_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_template_used(self):
        self.assertTemplateUsed(self.response, 'zing_it/signup.html')


class TestLoginPage(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('login'))

    def test_login_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_login_template_used(self):
        self.assertTemplateUsed(self.response, 'zing_it/login.html')


class TestLogoutPage(TestCase):

    def setUp(self):
        user = register_new_user()
        self.client.login(username=test_email, password=test_password)

    def test_logout_link_home(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Log out')

    def test_logout_link_songs(self):
        self.playlist, self.song = mock_playlist_and_songs()
        response = self.client.get(reverse('playlist', kwargs={'n':self.playlist.id}))
        self.assertContains(response, 'Log out')

    def test_logout_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=True)

        
class TestEditSongPage(TestCase):

    def setUp(self):
        user = register_new_user()
        self.playlist, self.song = mock_playlist_and_songs()
        self.client.login(username=test_email, password=test_password)
        self.response = self.client.get(reverse('edit', kwargs={'id':self.playlist.id}))

    def test_edit_url_and_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'zing_it/edit.html')

    def test_edit_has_contents(self):
        self.assertContains(self.response, self.song.artist)
