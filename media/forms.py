__author__ = 'djvol_000'

from django import forms

class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

    types =[('movie','Movie'),
            ('show','TV Show')]
    type = forms.ChoiceField(choices=types, widget=forms.RadioSelect( attrs={ 'class': 'type_select'}), required=False)
    search_text = forms.CharField(label='Search', required=False)
    optional_season = forms.CharField(label='Season', required=False)
    optional_episode = forms.CharField(label='Episode', required=False)

class TorrentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TorrentForm, self).__init__(*args, **kwargs)

    torrent_search_text = forms.CharField(label='Search Torrents', required=False)