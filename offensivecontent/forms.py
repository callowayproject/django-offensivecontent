from django import forms
from offensivecontent.models import OffensiveContentData

class MarkForm(forms.ModelForm):
    class Meta:
        model = OffensiveContentData
        exclude = ('user', 'offensive_content', 'pub_date')