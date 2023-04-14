from django.urls import include, path
from .views import shift
from .views import shiftlist
from .views import template
from .views import available


urlpatterns = [
    path("", shiftlist.home, name="shiftlist_home"),
    # path('history/', views),
    path(
        "shiftlist/",
        include(
            [
                path(
                    "create/",
                    shiftlist.shiftlist_add_normal,
                    name="shiftlist_add_normal",
                ),
                path(
                    "create_template/",
                    shiftlist.shiftlist_add_template,
                    name="shiftlist_add_template",
                ),
                path("<int:shiftlist_id>", shiftlist.shiftlist, name="shiftlist"),
                path(
                    "<int:shiftlist_id>/edit/",
                    shiftlist.shiftlist_edit,
                    name="shiftlist_edit",
                ),
                path(
                    "<int:shiftlist_id>/delete/",
                    shiftlist.shiftlist_delete,
                    name="shiftlist_delete",
                ),
                path(
                    "<int:shiftlist_id>/add_shift/",
                    shift.shift_create,
                    name="shift_create",
                ),
            ]
        ),
    ),
    path(
        "shift/<int:shift_id>/",
        include(
            [
                path("signup", shift.shift_signup, name="shift_signup"),
                path("edit", shift.shift_edit, name="shift_edit"),
                path("delete", shift.shift_delete, name="shift_delete"),
                path(
                    "shifters/",
                    include(
                        [
                            path("", shift.shift_shifters, name="shift_shifters"),
                            path(
                                "edit",
                                shift.shift_edit_shifters,
                                name="shift_edit_shifters",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    path(
        "templates/",
        include(
            [
                path("", template.templates, name="templates"),
                path("<int:template_id>", template.template),
                path("<int:template_id>/edit", template.template_edit),
                path("<int:template_id>/del", template.template_del),
                path("add", template.add_template),
            ]
        ),
    ),
    path(
        "available/",
        include(
            [
                path("", available.available_overview, name="available"),
                path("add", available.available_add),
                path("add-rep", available.available_add_rep),
                path("<int:type>/<int:available_id>/edit", available.available_edit),
                path("<int:type>/<int:available_id>/del", available.available_del),
            ]
        ),
    ),
]
