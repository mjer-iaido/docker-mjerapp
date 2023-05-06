from django.shortcuts import render, redirect
#from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views import generic
from django.urls import reverse_lazy
from urllib.parse import urlencode
from django.db.models import F
from django.db.models import Q
# from django.utils import get_grade

from .models import Events, Grade, Testee, Scoringsheet, Dojos, Country, Status, Embuscoringsheet
from .forms import ScoringsheetForm

#weasyprint --staticstart--
from django.template.loader import render_to_string
# from weasyprint import HTML, CSS

# from django_weasyprint import WeasyTemplateResponseMixin
# from django_weasyprint.views import WeasyTemplateResponse
from weasyprint import HTML, CSS

import tempfile
import datetime

# Create your views here.

def index(request):
    return render(request, 'shinsa/index.html', {})

# your_profile
def your_profile(request):
    return render(request, 'shinsa/your_profile.html', {})

# weasyprint --start--
def exportpdf_shinsa(request):
    from django.template.loader import get_template
    html_template = get_template('shinsa/scoringsheet_list.html')
    html_str = html_template.render({
                #    'Scoringsheet': Scoringsheet,
                },request)  # ここでrequestを渡してあげないと、Template側で必要な変数やプリセットなどが取得できずエラーになる場合がある

    pdf_file = HTML(request.GET.get('path')).write_pdf(
        stylesheets=[
            CSS(string='body { font-family: "M PLUS 1p", sans-serif; !important }'),
        ]
    )
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="shinsa_scoringsheet.pdf"'
    return response
# weasyprint --end--

class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    login_url = '/login/'

class DojosListView(LoginRequiredMixin, ListView):
    model = Dojos
    login_url = '/login/'

    def get_queryset(self):
        countryparam = self.request.GET.get('country')
        object_list = Dojos.objects.filter(
                        Q(country__id=countryparam))
        return object_list

class EventsListView(LoginRequiredMixin, ListView):
    model = Events
    login_url = '/login/'

class EventsDetailView(LoginRequiredMixin, DetailView):
    model = Events
    login_url = '/login/'

class TesteeListView(LoginRequiredMixin, ListView):
    model = Testee

    def get_queryset(self):
        dojoparam = self.request.GET.get('dojo')
        object_list = Testee.objects.filter(
                        Q(dojo__id=dojoparam))
        return object_list

    login_url = '/login/'

class TesteeprofileListView(LoginRequiredMixin, ListView):
    model = Testee
    template_name = 'shinsa/your_profile.html'

    def get_queryset(self):
        userparam = self.request.user
        object_list = Testee.objects.filter(
                        Q(membership_number=userparam))
        return object_list

    login_url = '/login/'

class TesteeDetailView(DetailView):
    model = Testee

class TesteeUpdateView(LoginRequiredMixin, UpdateView):
    model = Testee
    fields = [
        "status",
        "dojo",
        "first_grade",
        "second_grade",
        "third_grade",
        "fourth_grade",
        "fifth_grade",
        "sixth_grade",
        "renshi",
        "seventh_grade",
        "kyoshi",
        "eighth_grade",
        "hanshi"
        ]
#    success_url = reverse_lazy("scoringsheet")
    def get_success_url(self):
        return "".join([reverse('testee'),'?', urlencode(dict(dojo=self.request.GET.get('dojo')))])

    login_url = '/login/'

    def update_testee_grade(scoringsheet, pk):
        day = scoringsheet.events.event_date
        grade = TesteeUpdateView.get_grade(scoringsheet)
        Testee.objects.update_or_create(pk=pk, defaults={grade: day.strftime('%Y''-''%m''-''%d')})
        return  

    def undo_testee_grade(scoringsheet, pk):
        today = datetime.date.today()
        grade = TesteeUpdateView.get_grade(scoringsheet)
        Testee.objects.update_or_create(pk=pk, defaults={grade: None})
        return  

    def get_grade(scoringsheet):
        # scoringsheet.grade_id == 1 is 無段
        if scoringsheet.grade_id == 2:
            grade: str = "first_grade"
        elif scoringsheet.grade_id == 3:
            grade: str = "second_grade"
        elif scoringsheet.grade_id == 4:
            grade: str = "third_grade"
        elif scoringsheet.grade_id == 5:
            grade: str = "fourth_grade"
        elif scoringsheet.grade_id == 6:
            grade: str = "fifth_grade"
        elif scoringsheet.grade_id == 7:
            grade: str = "sixth_grade"
        elif scoringsheet.grade_id == 8:
            grade: str = "renshi"
        elif scoringsheet.grade_id == 9:
            grade: str = "seventh_grade"
        elif scoringsheet.grade_id == 10:
            grade: str = "kyoshi"
        elif scoringsheet.grade_id == 11:
            grade: str = "eighth_grade"
        else:
            grade: str = "hanshi"
        return grade


class TesteeCreateView(LoginRequiredMixin, CreateView):
    model = Testee
    fields = [
        "membership_number",
        "testee_name",
        "testee_name_eng",
        "status",
        "dojo"
        ]
    def get_success_url(self):
        return "".join([reverse('testee'),'?', urlencode(dict(dojo=self.request.GET.get('dojo')))])

    login_url = '/login/'

    def get_initial(self):
        initial = super().get_initial()
        initial["dojo"] = self.request.GET.get('dojo')
        initial["membership_number"] = self.kwargs.get('dojo_number')
        return initial

class ScoringsheetListView(ListView):
    model = Scoringsheet

    def get_queryset(self):
        eventparam = self.request.GET.get('event')
        object_list = Scoringsheet.objects.filter(
                        Q(events__id=eventparam)).order_by('id')
        return object_list

class ScoringsheetCreateView(LoginRequiredMixin, CreateView):
    model = Scoringsheet
    template_name = 'shinsa/scoringsheet_form.html'
    fields = [
        "testee",
        "grade",
        "events"
        ]
    success_url = reverse_lazy("scoringsheet_form")

    login_url = '/login/'

    def get_initial(self):
        initial = super().get_initial()
        initial["events"] = self.request.GET.get('event')
        return initial

class ScoringsheetDetailView(DetailView):
    model = Scoringsheet
    template_name = 'shinsa/scoringsheet_detail.html'

class Scoringsheet5UpdateView(LoginRequiredMixin, UpdateView):
    model = Scoringsheet
    fields = [
        "score1",
        "score2",
        "score3",
        "score4",
        "score5",
        "written_points",
        ]
    def get_success_url(self):
        return "".join([reverse('scoringsheet'),'?', urlencode(dict(event=self.request.GET.get('event')))])

    login_url = '/login/'

    def get_form(self):
        form = super(Scoringsheet5UpdateView, self).get_form()
        form.fields['score1'].label = self.kwargs.get('marker1')
        form.fields['score2'].label = self.kwargs.get('marker2')
        form.fields['score3'].label = self.kwargs.get('marker3')
        form.fields['score4'].label = self.kwargs.get('marker4')
        form.fields['score5'].label = self.kwargs.get('marker5')
        return form

class Scoringsheet4UpdateView(LoginRequiredMixin, UpdateView):
    model = Scoringsheet
    fields = [
        "score1",
        "score2",
        "score3",
        "score4",
        "written_points",
        ]
    def get_success_url(self):
        return "".join([reverse('scoringsheet'),'?', urlencode(dict(event=self.request.GET.get('event')))])

    login_url = '/login/'

    def get_form(self):
        form = super(Scoringsheet4UpdateView, self).get_form()
        form.fields['score1'].label = self.kwargs.get('marker1')
        form.fields['score2'].label = self.kwargs.get('marker2')
        form.fields['score3'].label = self.kwargs.get('marker3')
        form.fields['score4'].label = self.kwargs.get('marker4')
        return form

class Scoringsheet3UpdateView(LoginRequiredMixin, UpdateView):
    model = Scoringsheet
    fields = [
        "score1",
        "score2",
        "score3",
        "written_points",
        ]
    def get_success_url(self):
        return "".join([reverse('scoringsheet'),'?', urlencode(dict(event=self.request.GET.get('event')))])

    login_url = '/login/'

    def get_form(self):
        form = super(Scoringsheet3UpdateView, self).get_form()
        form.fields['score1'].label = self.kwargs.get('marker1')
        form.fields['score2'].label = self.kwargs.get('marker2')
        form.fields['score3'].label = self.kwargs.get('marker3')
        return form

class EmbuscoringsheetListView(ListView):
    model = Embuscoringsheet

    def get_queryset(self):
        eventparam = self.request.GET.get('event')
        object_list = Embuscoringsheet.objects.filter(
                        Q(events__id=eventparam)).order_by('id')
        return object_list

class EmbuscoringsheetCreateView(LoginRequiredMixin, CreateView):
    model = Embuscoringsheet
    template_name = 'shinsa/embuscoringsheet_form.html'
    fields = [
        "testee",
        "grade",
        "events"
        ]
    success_url = reverse_lazy("embuscoringsheet_form")

    login_url = '/login/'

    def get_initial(self):
        initial = super().get_initial()
        initial["events"] = self.request.GET.get('event')
        return initial

class Embuscoringsheet5UpdateView(LoginRequiredMixin, UpdateView):
    model = Embuscoringsheet
    fields = [
        "score1",
        "score2",
        "score3",
        "score4",
        "score5",
        ]
    def get_success_url(self):
        return "".join([reverse('embuscoringsheet'),'?', urlencode(dict(event=self.request.GET.get('event')))])

    login_url = '/login/'

    def get_form(self):
        form = super(Embuscoringsheet5UpdateView, self).get_form()
        form.fields['score1'].label = self.kwargs.get('marker1')
        form.fields['score2'].label = self.kwargs.get('marker2')
        form.fields['score3'].label = self.kwargs.get('marker3')
        form.fields['score4'].label = self.kwargs.get('marker4')
        form.fields['score5'].label = self.kwargs.get('marker5')
        return form

class Embuscoringsheet4UpdateView(LoginRequiredMixin, UpdateView):
    model = Embuscoringsheet
    fields = [
        "score1",
        "score2",
        "score3",
        "score4",
        ]
    def get_success_url(self):
        return "".join([reverse('embuscoringsheet'),'?', urlencode(dict(event=self.request.GET.get('event')))])

    login_url = '/login/'

    def get_form(self):
        form = super(Embuscoringsheet4UpdateView, self).get_form()
        form.fields['score1'].label = self.kwargs.get('marker1')
        form.fields['score2'].label = self.kwargs.get('marker2')
        form.fields['score3'].label = self.kwargs.get('marker3')
        form.fields['score4'].label = self.kwargs.get('marker4')
        return form

class Embuscoringsheet3UpdateView(LoginRequiredMixin, UpdateView):
    model = Embuscoringsheet
    fields = [
        "score1",
        "score2",
        "score3",
        ]
    def get_success_url(self):
        return "".join([reverse('embuscoringsheet'),'?', urlencode(dict(event=self.request.GET.get('event')))])

    login_url = '/login/'

    def get_form(self):
        form = super(Embuscoringsheet3UpdateView, self).get_form()
        form.fields['score1'].label = self.kwargs.get('marker1')
        form.fields['score2'].label = self.kwargs.get('marker2')
        form.fields['score3'].label = self.kwargs.get('marker3')
        return form
