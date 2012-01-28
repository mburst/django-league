from django.forms import ModelForm, BooleanField

from core.models import Team, TeamInvitation

class TeamForm(ModelForm):
    
    class Meta:
        model = Team
        fields = ('name', 'tag', 'url', 'recruiting', 'details')
        
class TeamInvitationForm(ModelForm):
    accept = BooleanField()
    
    class Meta:
        model = TeamInvitation
        fields = ('team', 'accept')