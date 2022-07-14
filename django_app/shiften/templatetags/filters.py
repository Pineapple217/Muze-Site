import json

from django import template

register = template.Library()

@register.filter
def pretty_json(value, arg=4):
    return json.dumps(value, indent=arg)