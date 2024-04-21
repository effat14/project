"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ecom import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),

    # customer
    path('customersignup', views.customer_signup_view, name='customer_signup'),
    path('customerlogin', LoginView.as_view(template_name='ecom/customer_login.html'), name='customerlogin'),
    path('logout', LogoutView.as_view(template_name='ecom/logout.html'), name='logout'),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('my-profile', views.my_profile_view, name='my-profile'),
    path('edit-profile', views.edit_profile_view, name='edit-profile'),
    path('customer-home', views.customer_home_view, name='customer-home'),
    path('aboutus', views.aboutus_view),

    path('add-to-cart/<int:product_id>', views.add_to_cart_view, name='cart_add'),
    path('product-details/<int:id>/', views.product_detail, name='product_detail'),
    path('cart-details/', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),

    path('checkout/', views.order_create, name='order_create'),
    path('my-order/', views.order_view, name='order_view'),
    path('my-order-details/<int:order_id>/', views.order_details, name='order_details'),

    path('search', views.search_view, name='search'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'E-Medicine store'
admin.site.site_title = 'E-Medicine store'
admin.site.index_title = 'E-Medicine store'
