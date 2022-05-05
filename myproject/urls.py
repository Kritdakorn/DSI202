"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from myapp.views import *
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('createpro/', Create_product.as_view(),name='image_create'),
    path('detail/<str:pk>/', views.product_detail, name='photo'),
    path('', Home.as_view(),name='home'),
    path('promotions', Promotions.as_view(),name='promotions'),
    path('type', views.type_view,name='type'),
    path('help', Report.as_view(),name='help'),
    path('logout/',customerlogoutView.as_view(),name='customerlogout'),
    path('login', customerloginView.as_view(), name="customerlogin"),
    path('profile/',views.profile, name='profile'),
    path('cart/',views.cart, name='cart'),

    path('add/',views.add_to_cart, name='add'),
    path('addon/',views.add_cart, name='addon'),
    path('removeon/',views.remove_cart, name='removeon'),

    path('createprofile/',CreateProfile.as_view(), name='createprofile'),

    path('transaction', views.transactionview, name='transaction'),
    path('detail_transaction/<tran>', views.detail_transaction, name='detail_transaction'),

    path('qr_mobile/<mobile>/<amount>/qr.png', views.get_qr, name='qr'),
    path('qr_nid/<nid>/<amount>/', views.get_qr, name='qr'),
    path('ct', views.createTransaction, name='ct'),

    path('accounts/', include('allauth.urls')),
    path('register/', customerregistrationView.as_view(), name="customerregistration")
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)