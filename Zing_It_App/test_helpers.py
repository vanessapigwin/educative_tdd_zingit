from Zing_It_App.models import CustomUser
from Zing_It_App.models import Playlist, Song
from Zing_It_App.views import my_playlists, my_songs

test_email = 'test@test.com'
test_password = 'asdasfasgf6!'

def register_new_user():
    # dummy user is created
    user = CustomUser.objects.create_user(
        username='test',
        email=test_email,
        password = test_password, 
        first_name='winwin',
        last_name='tan cardoso',
        full_name='winwin tan cardoso'
    )

    registered_user = CustomUser.objects.first()
    assert isinstance(registered_user, CustomUser)
    return registered_user


def mock_playlist_and_songs():
    # make playlist
    Playlist.objects.bulk_create(
        [Playlist(
            id=playlist['id'], 
            name=playlist['name']
        ) for playlist in my_playlists]
    )

    # make songs
    Song.objects.bulk_create([Song(
        song_id =song['id'],
        track = song['Track'],
        artist = song['Artist'],
        album = song['Album'],
        length = song['Length'],
    ) for song in my_songs])

    # create match table between Song and playlist
    ThroughModel = Song.playlist_id.through
    ThroughModel.objects.bulk_create(
        [ThroughModel(
            song_id=song['id'], 
            playlist_id=song['playlist_id']
        ) for song in my_songs]
    )

    # get playlist and a song to search
    playlist = Playlist.objects.get(id=1)
    song = Song.objects.get(song_id=1)

    return playlist, song