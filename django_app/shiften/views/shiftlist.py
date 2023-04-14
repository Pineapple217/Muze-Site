from pprint import pprint
from django.http import (
    HttpResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from shiften.forms import (
    ShiftAddForm,
    ShiftlistCreateForm,
    ShiftlistCreateWithTemplateForm,
    ShiftlistEditForm,
)
from shiften.functions import create_month_shiftlist
from shiften.models import Shiftlijst, Template
from django.utils.translation import gettext as _


@login_required()
@permission_required("shiften.view_shiftlijst")
def home(request):
    if request.user.has_perm("shiften.change_shiftlijst"):
        shiftlists = Shiftlijst.objects.all()
    else:
        shiftlists = Shiftlijst.objects.filter(is_active=True)
    shiftlists = shiftlists.order_by("date")

    context = {}
    context["form_normal"] = ShiftlistCreateForm()
    context["form_template"] = ShiftlistCreateWithTemplateForm()
    context["shiftlists"] = shiftlists

    return render(request, "shiften/home/index.html", context=context)


@login_required()
@permission_required("shiften.add_shiftlijst")
def shiftlist_add_normal(request):
    context = {}
    form = ShiftlistCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            shiftlist = form.save()

            context["list"] = shiftlist
            form = ShiftlistCreateForm()

    context["form_normal"] = form
    return render(request, "shiften/home/add_shiftlist_normal.html", context)


@login_required()
@permission_required("shiften.add_shiftlijst")
def shiftlist_add_template(request):
    context = {}
    form = ShiftlistCreateWithTemplateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            template_id = form.cleaned_data["template"]
            date = form.cleaned_data["date"]

            template = Template.objects.get(id=template_id)
            shiftlist = create_month_shiftlist(template, date)
            context["list"] = shiftlist
            form = ShiftlistCreateWithTemplateForm()

    context["form_template"] = form
    return render(request, "shiften/home/add_shiftlist_template.html", context)


@login_required()
@permission_required("shiften.view_shiftlijst")
@permission_required("shiften.view_shift")
def shiftlist(request, shiftlist_id):
    context = {}
    shiftlist = get_object_or_404(Shiftlijst, id=shiftlist_id)
    context["shiftlist"] = shiftlist
    context["shifts"] = shiftlist.shift_set.all().order_by("date", "start")
    context["form_edit"] = ShiftlistEditForm(instance=shiftlist)
    context["form_shift"] = ShiftAddForm()
    return render(request, "shiften/shiftlist/index.html", context=context)


@login_required
@permission_required("shiften.change_shiftlijst")
def shiftlist_edit(request, shiftlist_id):
    context = {}
    shiftlist = get_object_or_404(Shiftlijst, id=shiftlist_id)
    form = ShiftlistEditForm(request.POST or None, instance=shiftlist)
    if request.method == "POST":
        if form.is_valid():
            shiftlist = form.save()
            context["shiftlist_edited"] = True
            form = ShiftlistEditForm(instance=shiftlist)

    context["shiftlist"] = shiftlist
    context["form_edit"] = form
    return render(request, "shiften/shiftlist/edit_shiftlist.html", context)


@login_required
@permission_required("shiften.delete_shiftlijst")
def shiftlist_delete(request, shiftlist_id):
    shiftlist = get_object_or_404(Shiftlijst, id=shiftlist_id)
    shiftlist.delete()
    response = HttpResponse()
    response.headers["HX-Redirect"] = reverse("shiftlist_home")
    return response
