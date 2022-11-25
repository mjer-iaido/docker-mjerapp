from django import template
register = template.Library()

# # Shinsa scoringsheet
# @register.simple_tag
# def points5(value1, value2, value3, value4, value5):
#     return value1 + value2 + value3 + value4 + value5

# @register.simple_tag
# def points4(value1, value2, value3, value4):
#     return value1 + value2 + value3 + value4

# @register.simple_tag
# def points3(value1, value2, value3):
#     return value1 + value2 + value3

# @register.simple_tag
# def success():
#     return "success"

# @register.simple_tag
# def failure():
#     return "failure"

# Embu scoringsheet
# 5testers
@register.simple_tag
def maxpoint5(value1, value2, value3, value4, value5):
    return max(value1, value2, value3, value4, value5)

@register.simple_tag
def minpoint5(value1, value2, value3, value4, value5):
    return min(value1, value2, value3, value4, value5)

@register.simple_tag
def embupoint5(value1, value2, value3, value4, value5, value6, value7):
    return value1 + value2 + value3 + value4 + value5 - value6 - value7

# 4testers
@register.simple_tag
def maxpoint4(value1, value2, value3, value4):
    return max(value1, value2, value3, value4)

@register.simple_tag
def minpoint4(value1, value2, value3, value4):
    return min(value1, value2, value3, value4)

@register.simple_tag
def embupoint4(value1, value2, value3, value4, value5, value6):
    return value1 + value2 + value3 + value4 - value5 - value6

# 3testers
@register.simple_tag
def maxpoint3(value1, value2, value3):
    return max(value1, value2, value3)

@register.simple_tag
def minpoint3(value1, value2, value3):
    return min(value1, value2, value3)

@register.simple_tag
def embupoint3(value1, value2, value3, value4, value5):
    return value1 + value2 + value3 - value4 - value5
