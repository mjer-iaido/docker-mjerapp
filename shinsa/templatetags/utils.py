from django import template
from shinsa.views import TesteeUpdateView

register = template.Library()

@register.filter(name="pratical_points")
def pratical_points(score1, score2):
     return score1 + score2

@register.simple_tag(name="update_profile")
def update_profile(scoringsheet):

    if scoringsheet == '':
        pass
    else:
        passed: bool = False
        if scoringsheet.events.marker5:
            p_totalpoints = scoringsheet.score1 + scoringsheet.score2 + scoringsheet.score3 + scoringsheet.score4 + scoringsheet.score5
            if p_totalpoints >= 35 and scoringsheet.written_points >= 80:
                passed = True
        elif scoringsheet.events.marker4:
            p_totalpoints = scoringsheet.score1 + scoringsheet.score2 + scoringsheet.score3 + scoringsheet.score4
            if p_totalpoints >= 28 and scoringsheet.written_points >= 80:
                passed = True
        else:
            p_totalpoints = scoringsheet.score1 + scoringsheet.score2 + scoringsheet.score3
            if p_totalpoints >= 21 and scoringsheet.written_points >= 80:
                passed = True

        if passed:
            TesteeUpdateView.update_testee_grade(scoringsheet, scoringsheet.testee_id)
        else:
            TesteeUpdateView.undo_testee_grade(scoringsheet, scoringsheet.testee_id)

    return
