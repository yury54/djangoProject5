"""djangoProject5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, re_path


from priem import views
from priem.views import date_from_ajax
from django.conf.urls import include, url


urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', views.index),
    path('start.html', views.index),
    path('rec1.html', views.rec1),
    path('rec2.html', views.rec2),
    path('rec3.html', views.rec3),
    path('rec4.html', views.rec4),
    path('stol.html', views.stol),

    url(r'^stol_create/$', views.stol_create, name='stol_create'),
    path('holiday.html', views.holiday),
    url(r'^holiday_create/$', views.holiday_create, name='holiday_create'),
    url(r'^date_from_ajax/$', date_from_ajax, name='date_from_ajax'),
    path('delete/<int:id>/', views.delete, name='edit'),
    path('stol_delete/<int:id>/', views.stol_delete, name='stol_delete'),
    path('holiday_delete/<int:id>/', views.holiday_delete, name='holiday_delete'),
    re_path(r'^record', views.people),
    ]


