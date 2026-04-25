from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'occasion', 'genre', 'voice_type', 'mood', 'story']
        
        labels = {
            'story': 'Additional Details / Prompt',
        }
        
        widgets = {
            'story': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us more about this song...'}),
        }
