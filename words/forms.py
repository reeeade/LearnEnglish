from django.forms import ModelForm

from words.models import UserDict


class ArticleForm(ModelForm):
    class Meta:
        model = UserDict
        fields = ['word', 'translation', 'transcription', 'transliteration']


class PartialArticleForm(ModelForm):
    class Meta:
        model = UserDict
        exclude = ['user']
