from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import events_view
from .views import organizer_detail_view,all_organizers_view
from .views import contact_organizer_view,event_request_view,organizer_profile_view

from .views import contact_view
from pages.views import about_view  # استيراد العرض من pages

urlpatterns = [
    path('all/', views.services_list_view, name='services_list'),
    path('category/<int:category_id>/', views.subcategories_view, name='subcategories'),
    path('subcategory/<int:subcategory_id>/', views.subcategory_services_view, name='subcategory_services'),
    path('service/<int:service_id>/', views.service_detail_view, name='service_detail'),
    path('add-to-cart/<int:service_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation_view, name='order_confirmation'),
    path('my-account/', views.my_account_view, name='my_account'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/update-order-status/<int:order_id>/', views.update_order_status_view, name='update_order_status'),
    path('admin/order/<int:order_id>/', views.order_detail_view, name='order_detail'),
    # path('about/', views.about_us_view, name='about'),
    path('events/', events_view, name='events'),
    path('organizer/<int:organizer_id>/', organizer_detail_view, name='organizer_detail'),
    path('organizer/<int:organizer_id>/contact/', contact_organizer_view, name='contact_organizer'),
    path('events/request/', event_request_view, name='event_request'),
    path('organizers/<int:organizer_id>/', organizer_profile_view, name='organizer_profile'),
    path('organizers/', all_organizers_view, name='all_organizers'),
    path('account/update/', views.update_account, name='update_account'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('search/', views.search_services, name='search_services'),
    path('', views.home, name='home'),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='services-about'), 




]











