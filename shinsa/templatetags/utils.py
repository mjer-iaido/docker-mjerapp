from django import template
from shinsa.views import TesteeUpdateView

register = template.Library()

@register.simple_tag(name="cal_points")
def cal_points(scoringsheet) -> tuple[bool, int, bool, int, bool]:
    """
    return:
        tuple:
            0:practical exam judgement
            1:practical exam points
            2:written exam judgement
            3:written exam points
            4:final judgement
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
            # profile update
            TesteeUpdateView.update_testee_grade(scoringsheet, scoringsheet.testee_id)
        else:
            TesteeUpdateView.undo_testee_grade(scoringsheet, scoringsheet.testee_id)

        return passed, p_totalpoints, w_passed, w_points, judgement
    return

@register.simple_tag(name="embu_cal_points")
def embu_cal_points(embuscoringsheet) -> tuple[int, int, int, bool, bool, bool]:
    """
    return:
        tuple:
            0:max point
            1:min point
            2:pints
            3:pass_70
            4:pass_80
            5:pass_90
    """
    if embuscoringsheet == '':
        pass
    else:
        pass_70: bool = False
        pass_80: bool = False
        pass_90: bool = False

        if embuscoringsheet.events.marker5:
            total = embuscoringsheet.score1 + embuscoringsheet.score2 + embuscoringsheet.score3 + embuscoringsheet.score4 + embuscoringsheet.score5
            max_point = max(embuscoringsheet.score1, embuscoringsheet.score2, embuscoringsheet.score3, embuscoringsheet.score4, embuscoringsheet.score5)
            min_point = min(embuscoringsheet.score1, embuscoringsheet.score2, embuscoringsheet.score3, embuscoringsheet.score4, embuscoringsheet.score5)
            points = total - max_point - min_point
            if points >= 21:
                pass_70 = True
            if points >= 24:
                pass_80 = True
            if points >= 27:
                pass_90 = True

        elif embuscoringsheet.events.marker4 and embuscoringsheet.events.marker3:
            total = embuscoringsheet.score1 + embuscoringsheet.score2 + embuscoringsheet.score3 + embuscoringsheet.score4
            max_point = max(embuscoringsheet.score1, embuscoringsheet.score2, embuscoringsheet.score3, embuscoringsheet.score4)
            min_point = min(embuscoringsheet.score1, embuscoringsheet.score2, embuscoringsheet.score3, embuscoringsheet.score4)
            points = total - max_point - min_point
            if points >= 14:
                pass_70 = True
            if points >= 16:
                pass_80 = True
            if points >= 18:
                pass_90 = True

        elif embuscoringsheet.events.marker3:
            total = embuscoringsheet.score1 + embuscoringsheet.score2 + embuscoringsheet.score3
            max_point = max(embuscoringsheet.score1, embuscoringsheet.score2, embuscoringsheet.score3)
            min_point = min(embuscoringsheet.score1, embuscoringsheet.score2, embuscoringsheet.score3)
            points = total - max_point - min_point
            if points >= 7:
                pass_70 = True
            if points >= 8:
                pass_80 = True
            if points >= 9:
                pass_90 = True

        return max_point, min_point, points, pass_70, pass_80, pass_90
    return