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
      path('<int:shiftlist_id>/add_shift/', views.shift_create, name='shift_create'),
      # path('<int:template_id>/del', views.template_del),
      # path('add', views.add_template),
   ])),
   path('shift/<int:shift_id>/', include([
      path('signup', views.shift_signup, name='shift_signup'),
      path('edit', views.shift_edit, name='shift_edit'),
      path('delete', views.shift_delete, name='shift_delete'),
      path('shifters/', include([
         path('', views.shift_shifters, name='shift_shifters'),
         path('edit', views.shift_edit_shifters, name='shift_edit_shifters'),
      ]))
   ])),
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

