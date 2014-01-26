__author__ = 'djvol_000'

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('search', 'Search', onclick="search_media(); return false;", onsubmit="search_media(); return false;"))
        self.helper.form_id = 'search_form'

    types =[('movie', 'Movie'), ('show', 'TV Show')]
    type = forms.ChoiceField(choices=types, widget=forms.RadioSelect(attrs={'class': 'type_select'}), required=False, label="", initial=types[0][0])
    search_text = forms.CharField(label='Search', required=False)
    optional_season = forms.CharField(label='Season', required=False)
    optional_episode = forms.CharField(label='Episode', required=False)


class TorrentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TorrentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('search', 'Search', onclick="search_torrents(); return false;", onsubmit="search_torrents(); return false;"))
        self.helper.form_id = 'torrent_form'

    torrent_search_text = forms.CharField(label='Search Torrents', required=False)