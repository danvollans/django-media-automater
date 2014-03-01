# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from media.plex_funcs import *
from media.forms import *
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from media_automater.config import TRANSMISSION_DOWNLOAD


@login_required()
def home(request):
    page_title = "media automater"
    media_header_title = "plex media"
    torrent_header_title = "torrent search"
    files_header_title = "torrent management"
    template = loader.get_template('javascript.html')
    content = Context({
	    'page_title': page_title,
	    'media_header_title': media_header_title,
        'torrent_header_title': torrent_header_title,
        'files_header_title': files_header_title,
        'search_form': SearchForm(),
        'torrent_form': TorrentForm(),
        'download_url': TRANSMISSION_DOWNLOAD
	})
    content.update(csrf(request))
    return HttpResponse(template.render(content))
