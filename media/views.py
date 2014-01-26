# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from media.plex_funcs import *
from media.forms import *
from django.core.context_processors import csrf

def home(request):
    page_title = "media automater"
    media_header_title = "current media"
    torrent_header_title = "torrent search"
    files_header_title = "finished files"
    movie_list = list_movies()
    show_list = list_shows()
    template = loader.get_template('index.html')
    content = Context({
	    'page_title': page_title,
	    'media_header_title': media_header_title,
        'torrent_header_title': torrent_header_title,
        'files_header_title': files_header_title,
        'movie_list': sorted(movie_list),
        'show_list': show_list,
        'search_form': SearchForm(),
        'torrent_form': TorrentForm(),
	})
    content.update(csrf(request))
    return HttpResponse(template.render(content))
