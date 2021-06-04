from django import forms

from guiadomilico.apps.blog.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text']

        labels = {
            'title':'Titulo da postagem',
            'text': 'Digite o conteúdo'
        }

        widgets = {
            'text': forms.Textarea(attrs={'hidden': 'hidden', '':'text'}),
        }