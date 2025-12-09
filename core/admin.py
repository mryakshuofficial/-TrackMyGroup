from django.contrib import admin
from .models import Users,Group, GroupMember, StudentLocation
# Register your models here.

admin.site.register(Users)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(StudentLocation)