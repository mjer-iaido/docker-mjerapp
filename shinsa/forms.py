from django import forms
from .models import Testee, Scoringsheet, Grade, Dojos, Events, Embuscoringsheet


class ScoringsheetForm(forms.ModelForm):
    class Meta:
        model = Scoringsheet
        fields = '__all__'

        field_order = ('scoringsheet_id')

class EmbuscoringsheetForm(forms.ModelForm):
    class Meta:
        model = Embuscoringsheet
        fields = '__all__'

        field_order = ('embuscoringsheet_id')
