from django import forms
from .models import Testee, Scoringsheet, Grade, Dojos, Events, Embuscoringsheet


class ScoringsheetForm(forms.ModelForm):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dojo_list'] = Dojos.objects.all()
        return context
    
    # 親カテゴリの選択欄がないと絞り込めないので、定義する。
    Dojo = forms.ModelChoiceField(
        label='Dojo name',
        queryset=Dojos.objects,
        required=False
    )
    
    class Meta:
        model = Scoringsheet
        fields = '__all__'

        field_order = ('testee_name')

class EmbuscoringsheetForm(forms.ModelForm):
    class Meta:
        model = Embuscoringsheet
        fields = '__all__'

        field_order = ('embuscoringsheet_id')
