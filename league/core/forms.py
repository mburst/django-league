from django.forms import ModelForm

from core.models import Team

class TeamForm(ModelForm):
    
    class Meta:
        model = Team
        fields = ('name', 'tag', 'game', 'url', 'recruiting', 'details')