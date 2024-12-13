"""
URL configuration for weapon_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include
from app00_Reg_Log import views as Reg_Log
from app01_admin import views as admin
from app02_user import views as user


urlpatterns = [
    # app00
    path("", Reg_Log.login),
    path("register", Reg_Log.register),
    # app02 user
    path("user/market", user.market, name='user_market'),
    path("user/orders", user.orders, name='user_orders'),
    # app03 admin
    path("admin/warehouse", admin.warehouse, name='admin_warehouse'),
    path("admin/orders", admin.orders, name='admin_orders')
]
