from django.urls import include, path
from . import views

urlpatterns = [
   path('', views.home, name='shiftlist_home'),
   path('shiftlist/', include([
      path('create/', views.shiftlist_add_normal, name='shiftlist_add_normal'),
      path('create_template/', views.shiftlist_add_template, name='shiftlist_add_template'),
      path('<int:shiftlist_id>', views.shiftlist, name='shiftlist'),
      path('<int:shiftlist_id>/edit/', views.shiftlist_edit, name='shiftlist_edit'),
      path('<int:shiftlist_id>/delete/', views.shiftlist_delete, name='shiftlist_delete'),
      # path('<int:template_id>/del', views.template_del),
      # path('add', views.add_template),
   ])),
   path('shift/<int:shift_id>/', include([
      path('signup', views.shift_signup, name="shift_signup")
   ])),
   path('ajax', views.ajax_shift_list),
   path('<int:list_id>/ajax', views.ajax_shifts),
   path('signup_shift', views.signup_shift, name='signup_shift'),
   path('manage_shift', views.manage_shift),
   path('manage_shiftlist', views.manage_shiftlist),
   path('create_shift', views.create_shift),
   path('create_shiftlist', views.create_shiftlist),
   path('templates/', include([
      path('', views.templates, name='templates'),
      path('<int:template_id>', views.template),
      path('<int:template_id>/edit', views.template_edit),
      path('<int:template_id>/del', views.template_del),
      path('add', views.add_template),
   ])),
   path('available/', include([
      path('', views.available_overview, name='available'),
      path('add', views.available_add),
      path('add-rep', views.available_add_rep),
      path('<int:type>/<int:available_id>/edit', views.available_edit),
      path('<int:type>/<int:available_id>/del', views.available_del),
   ])),
]

