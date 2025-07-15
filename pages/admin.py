from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import TeamMember, Partner

admin.site.register(TeamMember)
admin.site.register(Partner)




