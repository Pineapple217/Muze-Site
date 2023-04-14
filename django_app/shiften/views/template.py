from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from shiften.forms import (
    TemplateForm,
)
from shiften.models import Template
from django.utils.translation import gettext as _


@login_required
@permission_required("shiften.view_template")
def templates(request):
    templates = Template.objects.all()
    context = {
        "templates": templates,
    }
    return render(request, "shiften/templates.html", context=context)


@login_required
@permission_required("shiften.view_template")
def template(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    context = {
        "template": template,
    }

    return render(request, "shiften/template.html", context=context)


@login_required
@permission_required("shiften.change_template")
def template_edit(request, template_id):

    template = get_object_or_404(Template, id=template_id)
    if request.method == "POST":
        template_form = TemplateForm(request.POST, instance=template)
        if template_form.is_valid():
            template_form.save()
            messages.success(request, _("Template updated successfully"))
            url = "/".join(request.path.split("/")[:-1])
            return redirect(url)
    else:
        template_form = TemplateForm(instance=template)
    return render(request, "shiften/template_edit.html", {"form": (template_form)})


@login_required
@permission_required("shiften.add_template")
def add_template(request):
    if request.method == "POST":
        template_form = TemplateForm(request.POST)
        if template_form.is_valid():
            template_form.save()
            messages.success(request, _("Template updated successfully"))
            return redirect(to="templates")
    else:
        template_form = TemplateForm()

    return render(request, "shiften/template_create.html", {"form": (template_form)})


@login_required
@permission_required("shiften.delete_template")
def template_del(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    template.delete()

    return redirect("templates")
