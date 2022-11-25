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
        result = cal_points(scoringsheet)

        # final judge
        if result[4]:
            TesteeUpdateView.update_testee_grade(scoringsheet, scoringsheet.testee_id)
        else:
            TesteeUpdateView.undo_testee_grade(scoringsheet, scoringsheet.testee_id)

    return


@register.simple_tag(name="cal_points")
def cal_points(scoringsheet) -> tuple[bool, int, bool, int, bool]:
    """
    return:
        tuple:
            practical exam judgement
            practical exam points
            written exam judgement
            written exam points
            final judgement
    """

    if scoringsheet == '':
        pass
    else:
        # practical exam
        passed: bool = False
        # written exam
        w_passed: bool = False
        # result
        judgement: bool = False

        if scoringsheet.events.marker5:
            p_totalpoints = scoringsheet.score1 + scoringsheet.score2 + scoringsheet.score3 + scoringsheet.score4 + scoringsheet.score5
            if p_totalpoints >= 35:
                passed = True
        elif scoringsheet.events.marker4:
            p_totalpoints = scoringsheet.score1 + scoringsheet.score2 + scoringsheet.score3 + scoringsheet.score4
            if p_totalpoints >= 28:
                passed = True
        else:
            p_totalpoints = scoringsheet.score1 + scoringsheet.score2 + scoringsheet.score3
            if p_totalpoints >= 21:
                passed = True

        # written exam judge
        w_points = scoringsheet.written_points
        if w_points >= 80:
            w_passed = True

        # final judge
        if passed and w_passed:
            judgement = True

        return passed, p_totalpoints, w_passed, w_points, judgement
    return
