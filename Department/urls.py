from django.urls import path
from Department import views

urlpatterns = [
    path('',views.home),
    path('modifydepart',views.modifyDepart),
    path('createdepartment',views.createDepartment),
    path('delete/<int:did>',views.Deletedepartment),
    path('edit/<int:did>',views.updateDepartment),
    # Roles
    path('viewrole',views.viewRole),
    path('addrole',views.addRole),
    path('deleterole/<int:rid>',views.Deleterole),
    path('updaterole/<int:rid>',views.Updaterole),
]
