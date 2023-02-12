import json

from django import template

register = template.Library()

@register.filter
def pretty_json(value, arg=4):
    return json.dumps(value, indent=arg)

@register.filter
def nr_of_empty_shiftslots(shift):
    return list(range(shift.max_shifters - shift.shifters.all().count()))