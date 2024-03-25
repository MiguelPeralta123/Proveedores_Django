"""
URL configuration for proveedores project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# Creando los endpoints para las vistas de inicio de sesión
from iniciar_sesion import views as views_login
# Creamos los endpoints para las vistas de proveedores
from alta_proveedores import views as views_proveedores
# Creamos los endpoints para las vistas de materiales
from alta_materiales import views as views_materiales

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL para admin
    path('admin/', admin.site.urls),

    # URL para home y settings
    path('', views_proveedores.home, name='home'),
    path('settings/', views_proveedores.settings, name='settings'),
    path('settings/permissions', views_proveedores.permissions, name='permissions'),

    # URL para inicio de sesión (login, logout)
    path('signin/', views_login.signin, name='signin'),
    path('signout/', views_login.signout, name='signout'),

    # URL para proveedores (get all, create, detail)
    path('proveedores/', views_proveedores.proveedor, {'tipo': 'proveedores'}, name='proveedor'),
    path('proveedores/crear/', views_proveedores.proveedor_create, {'tipo': 'proveedor'}, name='proveedor_create'),
    path('proveedores/<int:proveedor_id>/', views_proveedores.proveedor_detail, name='proveedor_detail'),

    # URL para clientes (get all, create, detail)
    path('clientes/', views_proveedores.proveedor, {'tipo': 'clientes'}, name='cliente'),
    path('clientes/crear/', views_proveedores.proveedor_create, {'tipo': 'cliente'}, name='cliente_create'),
    path('clientes/<int:cliente_id>/', views_proveedores.proveedor_detail, name='cliente_detail'),

    # URL para materiales
    path('materiales/', views_materiales.material, name='material'),
    path('materiales/crear/', views_materiales.material_create, name='material_create'),
    path('materiales/<int:material_id>/', views_materiales.material_detail, name='material_detail'),
    path('get_all_material_requests/', views_materiales.get_all_material_requests, name='get_all_material_requests'),
    path('create_material_form/', views_materiales.create_material_form, name='create_material_form'),
    path('save_material_form/', views_materiales.save_material_form, name='save_material_form'),
    path('get_request_materials/', views_materiales.get_request_materials, name='get_request_materials'),
    path('get_request_materials/', views_materiales.get_request_materials, name='get_request_materials'),
    path('delete_material/<int:id>/', views_materiales.delete_material, name='delete_material'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)