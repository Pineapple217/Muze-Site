from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def breadcrumbs(context):
    url = context['request'].path_info.split("/")
    crumbs = list(filter(None, url))
    out = []
    for i, c in enumerate(crumbs):
        dest = "/" + "/".join(crumbs[:i+1])
        out.append([c, dest])
    return out