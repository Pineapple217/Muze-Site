from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from shiften.forms import (
    ShiftAddForm,
    ShiftEditForm,
    ShiftEditShiftersFrom,
    TemplateForm,
)
from shiften.models import Shift, Shiftlijst, Template
from django.utils.translation import gettext as _


@login_required()
@permission_required("shiften.view_shift")
def shift_signup(request, shift_id):
    context = {}
    shift = get_object_or_404(Shift, id=shift_id)
    context["shift"] = shift
    if request.method == "POST":
        user_lid = request.user.lid
        if shift.shifters.contains(user_lid):  # zit er all in
            shift.shifters.remove(user_lid)
        elif (
            shift.shifters.count() < shift.max_shifters
        ):  # vrije plaats en zit er nog niet in
            shift.shifters.add(user_lid)
        else:  # voll
            print("shift voll")

    return render(request, "shiften/shiftlist/shifters_replace_wrapper.html", context)


@login_required()
@permission_required("shiften.add_shift")
def shift_create(request, shiftlist_id):
    context = {}
    shiftlist = get_object_or_404(Shiftlijst, id=shiftlist_id)
    form = ShiftAddForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            shift = form.save(commit=False)
            shift.shift_list = shiftlist
            shift.save()
            context["new_shift"] = True

            form = ShiftAddForm()
            context["shifts"] = shiftlist.shift_set.all().order_by("date", "start")

    context["shiftlist"] = shiftlist
    context["form_shift"] = form
    return render(request, "shiften/shiftlist/shift_create.html", context)


@login_required()
@permission_required("shiften.change_shift")
def shift_edit(request, shift_id):
    context = {}
    shift = get_object_or_404(Shift, id=shift_id)
    form = ShiftEditForm(request.POST or None, instance=shift)
    if request.method == "POST":
        if form.is_valid():
            shift = form.save()
            context["shifts"] = shift.shift_list.shift_set.all().order_by(
                "date", "start"
            )
            form = ShiftEditForm(instance=shift)

    context["shift"] = shift
    context["form_edit_shift"] = form
    return render(request, "shiften/shiftlist/shift_edit.html", context)


@login_required
@permission_required("shiften.delete_shift")
def shift_delete(request, shift_id):
    context = {}
    if request.method == "DELETE":
        shift = get_object_or_404(Shift, id=shift_id)
        shift.delete()
        context["shifts"] = shift.shift_list.shift_set.all().order_by("date", "start")
        return render(request, "shiften/shiftlist/shift_delete.html", context)


@login_required
@permission_required("shiften.change_shift")
def shift_edit_shifters(request, shift_id):
    context = {}
    shift = get_object_or_404(Shift, id=shift_id)
    shiftlist = get_object_or_404(Shiftlijst, id=shift.shift_list.id)
    form = ShiftEditShiftersFrom(request.POST or None, instance=shift)
    context["shift"] = shift
    context["form_edit_shifters"] = form
    if request.method == "POST":
        if form.is_valid():
            form.clean()
            form.save()
            return render(request, "shiften/shiftlist/shifters.html", context)
    # pprint(get_aviable_shifters(shiftlist))
    return render(request, "shiften/shiftlist/shift_edit_shifters.html", context)


@login_required
@permission_required("shiften.view_shift")
def shift_shifters(request, shift_id):
    context = {}
    shift = get_object_or_404(Shift, id=shift_id)
    context["shift"] = shift
    return render(request, "shiften/shiftlist/shifters_replace_wrapper.html", context)
