from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Zing_It_App.forms import SignUpForm, LoginForm, SongModelForm
from Zing_It_App.models import CustomUser, Song, Playlist


my_playlists=[
    {"id":1,"name":"Car Playlist","numberOfSongs":4},
    {"id":2,"name":"Coding Playlist","numberOfSongs":2}
]

my_songs = [
    {"id": 1, "Track": "thank u, next", "Artist": "Ariana Grande", "Album": "thank u, next", "Length": "3:27","playlist_id": 1},
    {"id": 2, "Track": "One Kiss, next", "Artist": "Dua Lipa, Calvin Harris", "Album": "One Kiss", "Length": "3:34","playlist_id": 1},
    {"id": 3, "Track": "Better Now", "Artist": "Post Malone", "Album": "beerbongs & bentleys", "Length": "3:51","playlist_id": 1},
    {"id": 4, "Track": "The Middle", "Artist": "Grey,Marren Morris, ZEDD", "Album": "The Middle", "Length": "3:04","playlist_id": 1},
    {"id": 5, "Track": "Love Lies", "Artist": "Normani, Khalid", "Album": "Love Lies", "Length": "3:21","playlist_id": 2},
    {"id": 6, "Track": "Rise", "Artist": "Jack & Jack, Jonas Blue", "Album": "Blue", "Length": "3:14","playlist_id": 2},
]


def logout_view(request):
    logout(request)
    return redirect(reverse('login'), permanent=True)


@login_required(redirect_field_name=None)
def index(request):
    my_playlists = Playlist.objects.all()
    song_counters = [Song.objects.filter(playlist_id=playlist.id).count() for playlist in my_playlists]
    return render(request, 'zing_it/home.html', context={"context":zip(my_playlists, song_counters)})


def signup(request):
    status = ' '
    signup_form = SignUpForm(request.POST or None) 

    if signup_form.is_valid():
        email = signup_form.cleaned_data['email']
        password = signup_form.cleaned_data['password']
        confirm_password = signup_form.cleaned_data['confirm_password']

        try:
            CustomUser.objects.get(email=email)
            status = 'Email already registered, please login.'
        except:
            if password != confirm_password:
                status = 'Password confirmation does not match, please try again.'
            else:
                new_user = CustomUser.objects.create_user(
                    email=email,
                    password = password, 
                    full_name=signup_form.cleaned_data['full_name']
                )
                new_user.save()
                return redirect(reverse('index'))
        
    return render(request, 'zing_it/signup.html', context= {"form":signup_form, "status":status})


def login_page(request):
    status = ' '
    form = LoginForm(request.POST or None)
        
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user, backend='Zing_It_App.auth_backend.EmailBackend')
            return redirect(reverse('index'))
        else:
            status='Please check your credentials and try again.'

    return render(request, 'zing_it/login.html', context={'form':form, 'status':status})


@login_required(redirect_field_name=None)
def playlist(request, n):
    playlist = Playlist.objects.get(id=n)
    songs = Song.objects.filter(playlist_id=n)
    if len(songs)==0:
        raise Http404("No songs in playlist")
    return render(request, 'zing_it/songs.html', context={'songs':songs, 'playlist':playlist})


@login_required(redirect_field_name=None)
def edit(request, id):
    song = Song.objects.get(song_id=id)
    form = SongModelForm(request.POST or None, instance=song)

    if form.is_valid():
        form.save()
        return redirect(reverse('index'))
    
    return render(request, 'zing_it/edit.html', context={'form':form})
