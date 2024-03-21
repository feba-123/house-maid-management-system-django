"""
URL configuration for maidservice project.

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
from siteusers import views

from django.conf import settings
from django.conf.urls.static import static
app_name="siteusers"

urlpatterns = [
    path('',views.home,name="home"),
    path('houseresident_registration', views.houseresident_registration, name='houseresident_registration'),
    path('flatresident_registration', views.flatresident_registration, name='flatresident_registration'),
    path('housemaid_registration', views.housemaid_registration, name='housemaid_registration'),
    path('Login_User', views.Login_User, name='Login_User'),
    path('houseresident_home',views.house_resident,name='house_resident'),
    path('flatresident_home',views.flat_resident,name='flat_resident'),
    path('housemaid_home',views.housemaid_home,name='housemaid_home'),
    path('signup',views.signup,name='signup'),
    path('admin_home',views.admin_home,name='admin_home'),
    # path('admin_update_status/<int:housemaid_id>/', views.admin_update_status, name='admin_update_status'),
    path('all_orders', views.Admin_Order, name='Admin_Order'),
    path('Order_detail(<int:pid>)', views.Order_detail, name="Order_detail"),
    path('Order_status(<int:pid>)', views.Order_status, name="Order_status"),
    path('all_housemaid', views.all_housemaid, name='all_housemaid'),
    path('all_users', views.all_users, name='all_users'),
    path('housemaid_detail/<int:housemaid_id>/', views.housemaid_detail, name='housemaid_detail'),
    path('status(<int:pid>)',views.Change_status,name="Change_status"),
    path('Explore_Service/<int:pid>/', views.Explore_Service, name='Explore_Service'),
    path('view_service',views.view_service, name="view_service"),
    path('edit_service(<int:pid>)',views.edit_service,name="edit_service"),
    path('delete_service(<int:pid>)',views.delete_service,name="delete_service"),
    path('add_service',views.add_service,name="add_service"),
    path('all_service_man', views.all_service_man, name="all_service_man"),
    path('new_service_man',views.new_service_man,name="new_service_man"),
    path('all_houseusers',views.all_houseusers,name="all_houseusers"),
    path('all_flatusers',views.all_flatusers,name="all_flatusers"),
    path('approve-booking/<int:order_id>/', views.approval_of_caretaker, name='approval_of_caretaker'),
    path('housecustomer_booking/<int:pid>/', views.housecustomer_booking, name='housecustomer_booking'),
    path('flat_resident_booking/<int:pid>/', views.flat_resident_booking, name='flat_resident_booking'),
    path('Customer_Order/', views.Customer_Order, name='Customer_Order'),
    path('Customer_Order1/', views.Customer_Order1, name='Customer_Order1'),
    path('admin_update_status/<int:order_id>/', views.admin_update_status, name='admin_update_status'),
    path('admin_update_status1/<int:order_id>/', views.admin_update_status1, name='admin_update_status1'),
    path('admin_update_status_2/<int:order_id>/', views.admin_update_status_2, name='admin_update_status_2'),
    path('admin_update_status_21/<int:order_id>/', views.admin_update_status_21, name='admin_update_status_21'),
    path('payment_page/<int:order_id>/', views.payment_page, name='payment_page'),
    path('contact/', views.contact, name="contact"),
    path('logout', views.user_logout, name="logout"),
    path('housemaid_bookings/',views.housemaid_bookings, name='housemaid_bookings'),
    path('services/', views.services, name='services'),
    path('house_resident_profile/',views.house_resident_profile,name="house_resident_profile"),
    path('flat_resident_profile/',views.flat_resident_profile,name="flat_resident_profile"),
    path('housemaid_profile/',views.housemaid_profile,name="housemaid_profile"),
    path('edit_house_resident_profile/',views.edit_house_resident_profile,name="edit_house_resident_profile"),
    path('edit_flat_resident_profile/', views.edit_flat_resident_profile, name="edit_flat_resident_profile"),
    path('edit_housemaid_profile/', views.edit_housemaid_profile, name="edit_housemaid_profile"),
    path('about/', views.about, name='about'),
    path('delete_houseuser/<int:pid>/',views.delete_houseuser, name='delete_houseuser'),
    path('delete_flatuser/<int:pid>/',views.delete_flatuser, name='delete_flatuser'),
    path('delete_service_man/<int:pid>/',views.delete_service_man, name='delete_service_man'),
    path('delete_order/<int:pid>/',views.delete_admin_order, name='delete_admin_order'),
    path('new_message/', views.new_message, name="new_message"),
    path('read_message/', views.read_message, name="read_message"),
    path('confirm_message(<int:pid>)',views.confirm_message, name="confirm_message"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
