from django import template
from django.urls import resolve
from django.http import Http404

register = template.Library()


@register.simple_tag(takes_context=True)
def breadcrumbs(context):
    url = context["request"].path_info.split("/")
    crumbs = list(filter(None, url))
    out = []
    for i, c in enumerate(crumbs):
        dest = "/" + "/".join(crumbs[: i + 1])
        try:
            resolve(dest + "/")
        except Http404:
            dest = ""
        out.append([c, dest])
    return out
