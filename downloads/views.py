from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from downloads.models import Songs, UserHistory
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import youtube_dl
import os
from rest_framework import generics
from downloads.serializers import SongsSerializer
from User.models import User

DEVELOPER_KEY = "AIzaSyAauLfeOKokwDqETGYcW7ppEP81JWVq15I"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


opt = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': "mp3",
    'outtmpl': '%(id)s',
    'noplaylist': True
}


def downloadpage(request):
    return render(request, 'download.html')


def download(request):
    lp = "https://www.youtube.com/watch?v="
    if 'dl' in request.GET and request.GET['dl']:
        dl = request.GET['dl']
        lb = dl.split('=')
        if len(lb) == 1:
            dl = lp + dl
        ydl = youtube_dl.YoutubeDL(opt)
        r = None
        url = dl
        cwd = os.getcwd()
        try:
            yl = Songs.objects.get(youtube_link=dl)
            yl.download_count += 1
            yl.save()
            d_link = yl.local_link
            return render(request, 'download_file.html', {'d_link': d_link})
        except Songs.DoesNotExist:
            try:
                os.chdir('/home/kuliza219/django/ENV/MP3/static/Downloaded Songs')
                with ydl:
                    r = ydl.extract_info(url, download = True)
                title = r['title']

                os.rename(r['id'], "%s.mp3" % title)
                d_link = 'Downloaded Songs' + '/' + title + ".mp3"
                p = Songs(youtube_link=dl, local_link=d_link, title=r['title'], uploader=r['uploader'], \
                          view_count=r['view_count'], like_count=r['like_count'], unlike_count=r['dislike_count'], \
                          download_count=1)
                p.save()
                os.chdir(cwd)
                return render(request, 'download_file.html', {'d_link': d_link})
            except Exception:
                return render(request, 'download.html', {'error': True})

    else:
        return render(request, 'download.html', {'error': True})

def userhistory(request):
    songs = []
    user = User.objects.get(id=request.session['m_id'])
    uh, created = UserHistory.objects.get_or_create(user=user)
    if created:
        uh.save()
    if 'down' in request.GET and request.GET['down']:
        hs = Songs.objects.get(id=request.GET['down'])
        uh.song.add(hs)
    songs = uh.song.all()
    return render(request, 'history.html', {'uh': uh, 'songs': songs})




def search(request):
    return render(request, 'search.html')



def youtube_search(request):
    try:
        if 's' in request.GET and request.GET['s']:
            s = request.GET['s']
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

            search_response = youtube.search().list(
                q=s,
                part="id,snippet",
                maxResults=25
            ).execute()

            videos = []
            channels = []
            playlists = []

            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
                elif search_result["id"]["kind"] == "youtube#channel":
                    channels.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["channelId"]))
                elif search_result["id"]["kind"] == "youtube#playlist":
                    playlists.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["playlistId"]))

            # print "Videos:\n", "\n".join(videos), "\n"
            # print "Channels:\n", "\n".join(channels), "\n"
            # print "Playlists:\n", "\n".join(playlists), "\n"
            return render(request, 'search_results.html', {'videos': videos, 'channels': channels, 'playlists': playlists})
        else:
            return render(request, 'search.html', {'error': True})
    except HttpError, e:
        return HttpResponse("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))


class SongList(generics.ListCreateAPIView):
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer