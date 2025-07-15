# from django.contrib import admin
# from .models import ServiceCategory, Service

# admin.site.register(ServiceCategory)
# admin.site.register(Service)

# from .models import SubCategory

# admin.site.register(SubCategory)


# from .models import ServiceProvider

# admin.site.register(ServiceProvider)

# from django.contrib import admin
# from .models import Order, OrderItem

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'status', 'created_at')
#     list_filter = ('status', 'created_at')
#     fields = ('user', 'status')  # ← هنا نحدد صراحة عرض الحقول
#     inlines = [OrderItemInline]


# admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)



# from .models import Organizer, Event

# admin.site.register(Organizer)
# admin.site.register(Event)

# # services/admin.py

# from django.contrib import admin
# from .models import EventRequest

# admin.site.register(EventRequest)


# from django.contrib import admin
# from .models import ContactMessage

# admin.site.register(ContactMessage)


from .models import ContactMessage
from django.contrib import admin
from .models import (
    ServiceCategory, Service, SubCategory,
    ServiceProvider, Order, OrderItem,
    Organizer, OrganizerWork, Event,
    EventRequest, ContactMessage
)

# تسجيل التصنيفات والخدمات
admin.site.register(ServiceCategory)
# admin.site.register(Service)
admin.site.register(SubCategory)
admin.site.register(ServiceProvider)

# إدارة الطلبات
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    fields = ('user', 'status')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)

# إدارة المنظمين والأعمال السابقة
class OrganizerWorkInline(admin.TabularInline):
    model = OrganizerWork
    extra = 1

class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [OrganizerWorkInline]

admin.site.register(Organizer, OrganizerAdmin)

# الفعاليات
admin.site.register(Event)

# نماذج طلبات تنظيم الفعاليات
admin.site.register(EventRequest)

# رسائل التواصل مع المنظمين
admin.site.register(ContactMessage)







from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'provider', 'category', 'price', 'created_at']
    list_filter = ['category', 'provider']
    search_fields = ['title', 'description']



