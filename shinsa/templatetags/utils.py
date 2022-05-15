from django import template
register = template.Library()

@register.filter(name="pratical_points")
def pratical_points(score1, score2):
     return score1 + score2
