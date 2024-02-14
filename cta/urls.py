"""
URL configuration for cta project.

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
from django.urls import path, include, re_path
from django.views.static import serve
from . import views
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ms_identity_web.django.msal_views_and_urls import MsalViews

msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()

#mapping the html files to the functions in the backend
urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in_status', views.index, name='status'),
    path('name_details', views.name_details, name='name_details'),
    path('token_details', views.token_details, name='token_details'),
    path('call_ms_graph', views.call_ms_graph, name='call_ms_graph'),
    path('get_entities', views.get_entities, name='get_entities'),
    path('get_tables', views.get_tables, name='get_tables'),
    path('auth/search', views.get_tables, name='get_tables'),
    path('auth/get_bulk', views.get_bulk, name='get_bulk'),
    path('auth/add', views.add_record, name='add_record'),
    path('get_dropdowns_journey', views.get_dropdowns_journey, name='get_dropdowns_journey'),
    path('auth/add_journey', views.add_journey, name='add_journey'),
    path('add_journey', views.add_journey, name='add_journey'),
    path('get_bulk', views.get_bulk, name='get_bulk'),
    path('auth/journey', views.get_journey, name='get_journey'),
    path('auth/update_journey', views.update_journey, name='update_journey'),
    path('update_journey', views.update_journey, name='update_journey'),
    path('get_journey', views.get_journey, name='get_journey'),
    path('get_dropdowns', views.get_dropdowns, name='get_dropdowns'),
    path('get_dropdowns_update', views.get_dropdowns_update, name='get_dropdowns_update'),
    path('get_dropdowns_journey_update', views.get_dropdowns_journey_update, name='get_dropdowns_journey_update'),
    path('auth/update', views.update_project, name='update_project'),
    path('get_token', views.get_token, name='get_token'),
    path('auth/audit', views.get_audit, name='get_audit'),
    path('get_usecases', views.get_usecases, name='get_usecases'),
    path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)), # our pre-configured msal URLs
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})  # for static files
]
