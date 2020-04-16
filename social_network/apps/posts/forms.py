from django.forms import ModelForm, Textarea
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('post_title', 'post_text', 'post_image')
        widgets = {
            'post_text': Textarea(attrs={'rows': 3}),
        }
