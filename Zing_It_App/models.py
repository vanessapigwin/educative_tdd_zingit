from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100,null=True)


class Playlist(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class Song(models.Model):
    song_id = models.IntegerField(unique=True, primary_key=True)
    track = models.CharField(max_length=200)
    artist = models.CharField(unique=True, max_length=70)
    album = models.CharField(max_length=70)
    length = models.TimeField()
    playlist_id = models.ManyToManyField('Playlist')

    def __str__(self):
        return self.track


# from Zing_It_App.views import my_playlists, my_songs

# try:
#     # make playlist
#     Playlist.objects.bulk_create(
#         [Playlist(
#             id=playlist['id'], 
#             name=playlist['name']
#         ) for playlist in my_playlists]
#     )

#     # make songs
#     Song.objects.bulk_create([Song(
#         song_id =song['id'],
#         track = song['Track'],
#         artist = song['Artist'],
#         album = song['Album'],
#         length = song['Length'],
#     ) for song in my_songs])

#     # create match table between Song and playlist
#     ThroughModel = Song.playlist_id.through
#     ThroughModel.objects.bulk_create(
#         [ThroughModel(
#             song_id=song['id'], 
#             playlist_id=song['playlist_id']
#         ) for song in my_songs]
#     )
#     print('TRANSFER DONE')
# except:
#     print('Data already imported')