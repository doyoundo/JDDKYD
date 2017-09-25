"""projectr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from projectr import views
from projectr import api_endpoints
from django.conf import settings
from django.conf.urls.static import static

# view endpoints
urlpatterns = [
    url(r'^client/', views.client),
    url(r'^instructor/', views.instructor),
    url(r'^student/', views.student),
    url(r'^login/', views.login_view),
    url(r'^logout/', views.logout_view),
    url(r'^register/', views.register),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', views.profile),
    url(r'^$', views.index),
    url(r'^projects/', views.projects),
    url(r'^project/(\d+)', views.project_view),
    url(r'^messages/', views.messages_internal),
    url(r'^joinsection/(\d*)', views.join_a_section),
    url(r'^managesection/', views.manage_sections),
    url(r'^editsection/(?P<section_id>\d+)/$', views.edit_a_section),
    url(r'^sendmessage/', views.send_message)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# api endpoints
urlpatterns += [
    url(r'^awardbid/(\d+)', api_endpoints.award_bid),
    url(r'^rejectbid/(\d+)', api_endpoints.reject_bid),
    url(r'^approveproject/(\d+)', api_endpoints.approve_project),
    url(r'^rejectproject/(\d+)', api_endpoints.reject_project),
    url(r'^askquestion/(\d+)', api_endpoints.ask_question),
    url(r'^deletesection/(\d+)', api_endpoints.delete_a_section),
    url(r'^replytoquestion/(\d+)', api_endpoints.reply_to_question)
]
