from django.contrib import admin
from .models import User, Subscription, Contact, Staff, Classes

admin.site.register(User)
admin.site.register(Subscription)
admin.site.register(Contact)
admin.site.register(Staff)
admin.site.register(Classes)
